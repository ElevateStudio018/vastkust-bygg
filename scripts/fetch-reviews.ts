// Runs before every build (npm prebuild): updates content/reviews.json, the customers' real reviews from ServiceFinder
// and Google. The site shows these instead of the reviews typed into the admin. The deploy workflow builds on a
// schedule and commits the file back when it changed, so new reviews appear by themselves and the list grows: each
// fetch adds the new reviews to the ones already in the file. A source that cannot be fetched keeps its reviews and
// rating from last time, and the build never fails because of it.
//
// ServiceFinder: the company's public page, which lists the overall rating and the three latest reviews.
// Google: the Places API, when GOOGLE_PLACES_API_KEY and GOOGLE_PLACE_ID are set (up to five reviews, Google's pick).
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { reviewsFileSchema, type ReviewSource, type ReviewsFile, type SourcedReview } from "../lib/site/reviews.ts";

const out = "content/reviews.json";
/** The most reviews kept per source, newest first. */
const KEEP = 30;
const SERVICEFINDER_URL = process.env.SERVICEFINDER_URL ?? "https://servicefinder.se/foretag/6845744";
const GOOGLE_KEY = process.env.GOOGLE_PLACES_API_KEY;
const GOOGLE_PLACE = process.env.GOOGLE_PLACE_ID;

interface Fetched {
  source: ReviewSource;
  reviews: SourcedReview[];
}

async function get(url: string, init?: RequestInit): Promise<Response> {
  const response = await fetch(url, { ...init, signal: AbortSignal.timeout(20_000) });
  if (!response.ok) throw new Error(`HTTP ${response.status} from ${new URL(url).host}`);
  return response;
}

const text = (value: unknown) => (typeof value === "string" ? value.replace(/\s+/g, " ").trim() : "");
const stars = (value: unknown) => Math.max(0, Math.min(5, Math.round(Number(value) || 0)));

async function fromServiceFinder(): Promise<Fetched> {
  const html = await (await get(SERVICEFINDER_URL, { headers: { "User-Agent": "Mozilla/5.0 (compatible; vastkust-bygg reviews)" } })).text();
  const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map((m) => JSON.parse(m[1]));
  const business = blocks.flat().find((block) => block?.aggregateRating);
  if (!business) throw new Error("no rating on the ServiceFinder page");
  const reviews = (business.review ?? [])
    .map((r: Record<string, any>): SourcedReview => ({
      id: `servicefinder-${text(r.datePublished)}-${text(r.author?.name)}`.toLowerCase().replace(/[^a-z0-9-]+/g, "-"),
      source: "servicefinder",
      title: text(r.name),
      quote: text(r.reviewBody),
      name: text(r.author?.name),
      date: text(r.datePublished).slice(0, 10),
      rating: stars(r.reviewRating?.ratingValue),
      url: SERVICEFINDER_URL,
    }))
    .filter((r: SourcedReview) => r.name && (r.quote || r.title));
  return {
    source: {
      id: "servicefinder",
      name: "ServiceFinder",
      rating: Number(business.aggregateRating.ratingValue) || 0,
      count: Number(business.aggregateRating.reviewCount) || 0,
      url: SERVICEFINDER_URL,
    },
    reviews,
  };
}

async function fromGoogle(): Promise<Fetched> {
  const response = await get(`https://places.googleapis.com/v1/places/${encodeURIComponent(GOOGLE_PLACE!)}?languageCode=sv`, {
    headers: { "X-Goog-Api-Key": GOOGLE_KEY!, "X-Goog-FieldMask": "rating,userRatingCount,googleMapsUri,reviews" },
  });
  const place = (await response.json()) as Record<string, any>;
  const reviews = (place.reviews ?? [])
    .map((r: Record<string, any>): SourcedReview => ({
      id: `google-${text(r.publishTime).slice(0, 19)}-${text(r.authorAttribution?.displayName)}`.toLowerCase().replace(/[^a-z0-9-]+/g, "-"),
      source: "google",
      title: "",
      quote: text(r.originalText?.text) || text(r.text?.text),
      name: text(r.authorAttribution?.displayName),
      date: text(r.publishTime).slice(0, 10),
      rating: stars(r.rating),
      url: text(r.googleMapsUri) || text(place.googleMapsUri),
    }))
    .filter((r: SourcedReview) => r.quote && r.name);
  return {
    source: { id: "google", name: "Google", rating: Number(place.rating) || 0, count: Number(place.userRatingCount) || 0, url: text(place.googleMapsUri) },
    reviews,
  };
}

function previous(): ReviewsFile {
  if (!existsSync(out)) return { fetchedAt: "", sources: [], reviews: [] };
  const parsed = reviewsFileSchema.safeParse(JSON.parse(readFileSync(out, "utf8")));
  return parsed.success ? parsed.data : { fetchedAt: "", sources: [], reviews: [] };
}

async function main() {
  const last = previous();
  const jobs: [ReviewSource["id"], () => Promise<Fetched>][] = [["servicefinder", fromServiceFinder]];
  if (GOOGLE_KEY && GOOGLE_PLACE) jobs.push(["google", fromGoogle]);

  const sources: ReviewSource[] = [];
  const reviews: SourcedReview[] = [];
  for (const [id, job] of jobs) {
    try {
      const fetched = await job();
      sources.push(fetched.source);
      const fresh = new Set(fetched.reviews.map((r) => r.id));
      const kept = [...fetched.reviews, ...last.reviews.filter((r) => r.source === id && !fresh.has(r.id))];
      reviews.push(...kept.sort((a, b) => b.date.localeCompare(a.date)).slice(0, KEEP));
      console.log(`reviews: ${fetched.reviews.length} from ${fetched.source.name} (${fetched.source.rating} of 5, ${fetched.source.count} in all)`);
    } catch (error) {
      // Keep what this source had last time rather than dropping its reviews from the site.
      sources.push(...last.sources.filter((s) => s.id === id));
      reviews.push(...last.reviews.filter((r) => r.source === id));
      console.warn(`reviews: could not fetch ${id}, keeping the previous ones:`, error instanceof Error ? error.message : error);
    }
  }

  // A source not fetched in this run (Google without its key) keeps what it had.
  const fetchedIds = new Set(jobs.map(([id]) => id));
  sources.push(...last.sources.filter((s) => !fetchedIds.has(s.id)));
  reviews.push(...last.reviews.filter((r) => !fetchedIds.has(r.source)));

  reviews.sort((a, b) => b.date.localeCompare(a.date));
  const unchanged = JSON.stringify({ sources, reviews }) === JSON.stringify({ sources: last.sources, reviews: last.reviews });
  // The time only moves when something changed, so the workflow commits the file only when there is news.
  const file = reviewsFileSchema.parse({ fetchedAt: unchanged ? last.fetchedAt : new Date().toISOString(), sources, reviews });
  writeFileSync(out, JSON.stringify(file, null, 2) + "\n");
}

main().catch((error) => {
  console.warn("reviews: skipped:", error);
});
