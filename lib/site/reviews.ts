// The customers' real reviews, fetched from ServiceFinder and Google before every build (scripts/fetch-reviews.ts).
// When there are any, the site shows them instead of the reviews typed into the admin.
import { z } from "zod";
import data from "../../content/reviews.json";

const sourceId = z.enum(["servicefinder", "google"]);

export const reviewSourceSchema = z.object({
  id: sourceId,
  name: z.string(),
  /** The overall rating on that site, 0–5. */
  rating: z.number().min(0).max(5),
  /** How many reviews the company has there in all. */
  count: z.number().int().min(0),
  url: z.string(),
});

export const sourcedReviewSchema = z.object({
  id: z.string(),
  source: sourceId,
  title: z.string(),
  quote: z.string(),
  name: z.string(),
  /** YYYY-MM-DD. */
  date: z.string(),
  rating: z.number().int().min(0).max(5),
});

export const reviewsFileSchema = z.object({
  fetchedAt: z.string(),
  sources: z.array(reviewSourceSchema),
  reviews: z.array(sourcedReviewSchema),
});

export type ReviewSource = z.infer<typeof reviewSourceSchema>;
export type SourcedReview = z.infer<typeof sourcedReviewSchema>;
export type ReviewsFile = z.infer<typeof reviewsFileSchema>;

let cached: ReviewsFile | undefined;

/** The fetched reviews; empty when nothing could be fetched (the admin's own reviews are shown then). */
export function getFetchedReviews(): ReviewsFile {
  cached ??= reviewsFileSchema.safeParse(data).data ?? { fetchedAt: "", sources: [], reviews: [] };
  return cached;
}

/** "okt 2025" */
export function reviewMonth(date: string): string {
  const parsed = new Date(`${date}T12:00:00Z`);
  return Number.isNaN(parsed.getTime()) ? "" : parsed.toLocaleDateString("sv-SE", { month: "short", year: "numeric" }).replace(".", "");
}
