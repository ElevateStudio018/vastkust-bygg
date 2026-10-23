import type { Metadata } from "next";
import { ReviewsPageView } from "@/components/site/ReviewsPageView";
import { getSite } from "@/lib/site/data.ts";

export function generateMetadata(): Metadata {
  const site = getSite();
  const title = "Omdömen";
  const description = `Vad kunderna säger om ${site.company.legalName} – omdömen från Google och ServiceFinder.`;
  return {
    title,
    description,
    alternates: { canonical: "/omdomen" },
    openGraph: { title: `${title} | ${site.settings.siteName}`, description, url: `${site.settings.siteUrl}/omdomen`, type: "website" },
  };
}

export default function ReviewsPage() {
  return <ReviewsPageView site={getSite()} />;
}
