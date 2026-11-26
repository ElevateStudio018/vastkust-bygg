// Runs before every build and dev start (npm prebuild/predev): writes content/snapshot.json, the content the site is
// built from. That is content/site.json, which is edited in Pages CMS (.pages.yml) and committed to the repository;
// without it the published snapshot in Supabase when the site is connected to one, else the original content
// (content/baseline.json). A build that cannot read or validate its content fails rather than publishing anything
// else, so the live site keeps its last good version.
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { siteDataSchema, type SiteData } from "../lib/site/schema.ts";
import { downloadFonts } from "./fonts.ts";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const out = "content/snapshot.json";
const fontsOut = "content/fonts.json";

/** The theme's own fonts, downloaded for the site to serve itself (see scripts/fonts.ts). */
async function writeFonts(site: SiteData) {
  writeFileSync(fontsOut, JSON.stringify(await downloadFonts(site)));
}

async function fetchPublished(): Promise<{ version: number; data: unknown }> {
  let lastError: unknown;
  for (let attempt = 1; attempt <= 4; attempt++) {
    try {
      const response = await fetch(`${url}/rest/v1/site_snapshot?select=version,data&id=eq.1`, {
        headers: { apikey: key!, Authorization: `Bearer ${key}` },
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      const rows = (await response.json()) as { version: number; data: unknown }[];
      if (rows.length !== 1) throw new Error("No published snapshot");
      return rows[0];
    } catch (error) {
      lastError = error;
      await new Promise((resolve) => setTimeout(resolve, 2 ** attempt * 500));
    }
  }
  throw lastError;
}

/**
 * An image replaced in Pages CMS gets a new src but keeps the old image's smaller copies (variants), which would show
 * the old picture on phones; drop variants that are not copies of the current src.
 */
function dropStaleVariants(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(dropStaleVariants);
  if (!value || typeof value !== "object") return value;
  const object = Object.fromEntries(Object.entries(value).map(([k, v]) => [k, dropStaleVariants(v)])) as Record<string, unknown>;
  if (typeof object.src === "string" && Array.isArray(object.variants)) {
    const base = object.src.replace(/(-\d+)?\.[a-z0-9]+$/i, "");
    object.variants = object.variants.filter((v) => typeof v?.src === "string" && v.src.replace(/(-\d+)?\.[a-z0-9]+$/i, "") === base);
  }
  return object;
}

async function main() {
  if (existsSync("content/site.json")) {
    const parsed = siteDataSchema.safeParse(dropStaleVariants(JSON.parse(readFileSync("content/site.json", "utf8"))));
    if (!parsed.success) {
      console.error("snapshot: content/site.json does not match the schema:", parsed.error.issues.slice(0, 10));
      process.exit(1);
    }
    writeFileSync(out, JSON.stringify(parsed.data));
    await writeFonts(parsed.data);
    console.log("snapshot: content/site.json (edited in Pages CMS)");
    return;
  }
  if (!url || !key) {
    const baseline = siteDataSchema.parse(JSON.parse(readFileSync("content/baseline.json", "utf8")));
    writeFileSync(out, JSON.stringify(baseline));
    await writeFonts(baseline);
    console.log("snapshot: not connected to Supabase, using content/baseline.json");
    return;
  }

  const { version, data } = await fetchPublished();
  const parsed = siteDataSchema.safeParse(data);
  if (!parsed.success) {
    console.error("snapshot: the published content does not match the schema:", parsed.error.issues.slice(0, 10));
    process.exit(1);
  }
  writeFileSync(out, JSON.stringify(parsed.data));
  await writeFonts(parsed.data);
  // The admin compares this with the published version to tell when the new site is live.
  writeFileSync("public/site-version.json", JSON.stringify({ version }));
  console.log(`snapshot: published version ${version} from Supabase`);
}

main().catch((error) => {
  console.error("snapshot: could not fetch the published content:", error);
  process.exit(1);
});
