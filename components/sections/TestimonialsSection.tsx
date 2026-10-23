import Link from "next/link";
import { Eyebrow, Stars } from "../vk/parts";
import { Icon } from "../Icon";
import { ReviewSlider } from "../vk/ReviewSlider";
import { SourceLogo } from "../vk/SourceLogo";
import { list } from "@/lib/site/collection.ts";
import { getFetchedReviews, reviewMonth, type ReviewSource } from "@/lib/site/reviews.ts";
import type { SiteData } from "@/lib/site/schema.ts";
import type { SectionProps } from "./types";

export interface Review {
  id: string;
  title: string;
  quote: string;
  name: string;
  detail: string;
  rating: number;
  /** For fetched reviews: the site it came from (its name and logo on the card) and the link to read it there. */
  sourceId?: string;
  sourceName?: string;
  url?: string;
}

export function ReviewCard({ review, ratingLabel }: { review: Review; ratingLabel: string }) {
  const card = (
    <figure className="rev">
      <div className="rev-top">
        <Stars n={review.rating} label={ratingLabel} />
        {review.sourceName && (
          <span className="rev-src">
            <SourceLogo source={review.sourceId ?? ""} />
            {review.sourceName}
          </span>
        )}
      </div>
      {review.title && <p className="rev-job">{review.title}</p>}
      {review.quote && (
        <blockquote>
          <p>”{review.quote}”</p>
        </blockquote>
      )}
      <figcaption>
        <span className="av" aria-hidden="true">
          {review.name.slice(0, 1)}
        </span>
        <span>
          <b>{review.name}</b>
          {review.detail && <small>{review.detail}</small>}
        </span>
      </figcaption>
    </figure>
  );
  if (!review.url) return card;
  return (
    <a className="rev-a" href={review.url} target="_blank" rel="noopener noreferrer" aria-label={`${review.name}s omdöme på ${review.sourceName}`}>
      {card}
    </a>
  );
}

/** The reviews fetched from ServiceFinder and Google, with the sites they came from; null while there are none. */
function fetchedReviews(): { reviews: Review[]; sources: ReviewSource[] } | null {
  const { reviews, sources } = getFetchedReviews();
  if (!reviews.length) return null;
  return {
    sources: sources.filter((s) => s.count > 0),
    reviews: reviews.map((r) => {
      const source = sources.find((s) => s.id === r.source);
      return { ...r, detail: reviewMonth(r.date), sourceId: r.source, sourceName: source?.name ?? "", url: r.url || source?.url || "" };
    }),
  };
}

/** The reviews the site shows: the fetched ones, or else the given ones (typed into the admin). */
export function shownReviews(own: Review[]): { reviews: Review[]; sources: ReviewSource[] } {
  return fetchedReviews() ?? { reviews: own, sources: [] };
}

const score = (n: number) => n.toLocaleString("sv-SE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

/** All reviews in a row to page through, with the overall rating beside the heading. */
export function Reviews({ eyebrow, heading, text, reviews: own, site, tint = true }: { eyebrow: string; heading: string; text: string; reviews: Review[]; site: SiteData; tint?: boolean }) {
  const { reviews, sources } = shownReviews(own);
  const rated = reviews.filter((r) => r.rating > 0);
  const average = rated.length ? rated.reduce((sum, r) => sum + r.rating, 0) / rated.length : 0;
  const head = (
    <div>
      <Eyebrow text={eyebrow} />
      {heading && <h2>{heading}</h2>}
    </div>
  );
  const rating = sources.length ? (
    <span className="rating-list">
      {sources.map((source) => (
        <a key={source.id} className="rating" href={source.url} target="_blank" rel="noopener noreferrer">
          <SourceLogo source={source.id} />
          <Stars n={Math.round(source.rating)} label={site.ui.ratingLabel} />
          <span>
            <b>{`${score(source.rating)} av 5`}</b>
            {` · ${source.count} omdömen på ${source.name}`}
          </span>
        </a>
      ))}
      <Link href="/omdomen" className="more">
        Visa alla omdömen <Icon name="ArrowRight" className="ic" />
      </Link>
    </span>
  ) : average > 0 ? (
    <p className="rating">
      <Stars n={Math.round(average)} label={site.ui.ratingLabel} />
      <span>
        <b>{`${average.toLocaleString("sv-SE", { maximumFractionDigits: 1 })} av 5`}</b>
        {text ? ` ${text}` : ""}
      </span>
    </p>
  ) : undefined;
  return (
    <section className={`sec${tint ? " tint" : ""}`}>
      <div className="wrap">
        <ReviewSlider head={head} aside={rating} labels={{ previous: site.ui.carouselPrevious, next: site.ui.carouselNext }}>
          {reviews.map((review) => (
            <li key={review.id}>
              <ReviewCard review={review} ratingLabel={site.ui.ratingLabel} />
            </li>
          ))}
        </ReviewSlider>
      </div>
    </section>
  );
}

export function TestimonialsSection({ section, ctx }: SectionProps<"testimonials">) {
  return (
    <div id={section.anchor || undefined}>
      <Reviews eyebrow={section.eyebrow} heading={section.heading} text={section.text} reviews={list(section.items)} site={ctx.site} />
    </div>
  );
}
