// The content the site is built from: content/snapshot.json, which scripts/fetch-snapshot.ts writes before every build
// (the published content from Supabase, or the original content while the site is not connected to one).
import snapshot from "@/content/snapshot.json";
import fonts from "@/content/fonts.json";
import { siteDataSchema, type SiteData } from "./schema.ts";
import { withBasePath } from "./images.ts";

let site: SiteData | undefined;

export function getSite(): SiteData {
  if (!site) {
    site = siteDataSchema.parse(snapshot);
    // On the site's own domain the links point there, whatever address the content was published with.
    const ownUrl = process.env.NEXT_PUBLIC_SITE_URL;
    if (ownUrl) site = { ...site, settings: { ...site.settings, siteUrl: ownUrl } };
  }
  return site;
}

/** @font-face rules for the fonts the build downloaded (scripts/fonts.ts); empty while the site uses only Figtree. */
export function fontFaceCss(): string {
  return (fonts as { family: string; style: string; weight: string; src: string; unicodeRange: string }[])
    .map(
      (face) =>
        `@font-face{font-family:"${face.family}";font-style:${face.style};font-weight:${face.weight};font-display:swap;src:url("${withBasePath(face.src)}") format("woff2");${
          face.unicodeRange ? `unicode-range:${face.unicodeRange};` : ""
        }}`
    )
    .join("");
}
