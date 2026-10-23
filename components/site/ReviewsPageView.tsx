import { HeroCrumbs } from "../sections/PageHeroSection";
import { ReviewCard, shownReviews } from "../sections/TestimonialsSection";
import { SourceLogo } from "../vk/SourceLogo";
import { Btn, CallBtn, Eyebrow, Stars } from "../vk/parts";
import { list } from "@/lib/site/collection.ts";
import { focusStyle, imageProps } from "@/lib/site/images.ts";
import { QUOTE_HREF } from "@/lib/site/links.ts";
import { homePage } from "@/lib/site/pages.ts";
import type { SiteData } from "@/lib/site/schema.ts";

/** The reviews typed into the admin: those of the first reviews section on the site, shown if none were fetched. */
function ownReviews(site: SiteData) {
  for (const page of list(site.pages)) {
    for (const section of list(page.sections)) {
      if (section.type === "testimonials" && !section.hidden) return list(section.items);
    }
  }
  return [];
}

const score = (n: number) => n.toLocaleString("sv-SE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

/** /omdomen: every review the site has, with the rating on each site and a link to read them all there. */
export function ReviewsPageView({ site }: { site: SiteData }) {
  const { reviews, sources } = shownReviews(ownReviews(site));
  const { ui, company } = site;
  const hero = list(homePage(site).sections).find((section) => section.type === "hero");
  const image = hero?.type === "hero" ? hero.image : null;

  return (
    <>
      <section className="hero">
        {image && (
          <div className="hero-bg">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img {...imageProps(image, "100vw")} alt="" style={focusStyle(image)} fetchPriority="high" />
          </div>
        )}
        <div className="wrap hero-in">
          <HeroCrumbs label={ui.breadcrumbsLabel} items={[{ label: ui.breadcrumbHome, href: "/" }, { label: "Omdömen" }]} />
          <Eyebrow text="Omdömen" />
          <h1>Vad kunderna säger</h1>
          <p className="hero-lead">Omdömen från våra kunder på Google och ServiceFinder. Nya omdömen kommer upp här av sig själva.</p>
        </div>
      </section>

      <section className="sec">
        <div className="wrap">
          {sources.length > 0 && (
            <ul className="src-cards">
              {sources.map((source) => (
                <li key={source.id}>
                  <a href={source.url} target="_blank" rel="noopener noreferrer">
                    <SourceLogo source={source.id} />
                    <span>
                      <b>{source.name}</b>
                      <span className="src-score">
                        <Stars n={Math.round(source.rating)} label={ui.ratingLabel} />
                        <b>{score(source.rating)}</b> av 5 · {source.count} omdömen
                      </span>
                    </span>
                    <small>Läs alla på {source.name} ↗</small>
                  </a>
                </li>
              ))}
            </ul>
          )}
          <ul className="revs revs-all">
            {reviews.map((review) => (
              <li key={review.id}>
                <ReviewCard review={review} ratingLabel={ui.ratingLabel} />
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="sec tint">
        <div className="wrap revs-cta">
          <h2>Vill du också bli en nöjd kund?</h2>
          <div className="btns">
            <Btn link={{ label: site.navigation.menuButton || "Begär offert", href: QUOTE_HREF }} kind="blue" arrow />
            <CallBtn phone={company.phone} prefix={ui.callPrefix} kind="ghost" />
          </div>
        </div>
      </section>
    </>
  );
}
