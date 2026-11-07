/** @type {import('next').NextConfig} */
const isGithubPages = process.env.GITHUB_PAGES === "true";
// The site's own domain (e.g. vastkustbygg.se), set as the repository variable SITE_DOMAIN at launch. With it the site
// is served from the domain's root; without it from the preview address elevatestudio018.github.io/vastkust-bygg.
const customDomain = (process.env.CUSTOM_DOMAIN ?? "").trim().replace(/^https?:\/\//, "").replace(/\/+$/, "");
const basePath = isGithubPages && !customDomain ? "/vastkust-bygg" : "";

const nextConfig = {
  reactStrictMode: true,
  images: {
    formats: ["image/webp"],
  },
  // Plain files in public/ (such as the photos) need the base path added by hand.
  env: {
    NEXT_PUBLIC_BASE_PATH: basePath,
    // Overrides the address in the content (canonical links, sitemap, social cards) once the site has its own domain.
    NEXT_PUBLIC_SITE_URL: customDomain ? `https://${customDomain}` : "",
  },
  // Only applied for the GitHub Pages preview build (see .github/workflows/deploy-pages.yml).
  // The real deployment (Vercel etc.) keeps a normal Next.js server build.
  ...(isGithubPages && {
    output: "export",
    basePath,
    trailingSlash: true,
  }),
};

export default nextConfig;
