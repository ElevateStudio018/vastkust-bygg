import { withBasePath } from "@/lib/site/images.ts";
import type { Settings } from "@/lib/site/schema.ts";

/** What the logo spots (header, menu, footer) need to draw the logo. */
export interface LogoContent {
  logo: Settings["logo"];
  /** The company's name for screen readers. */
  name: string;
}

// Västkust Bygg & Montage's own logo: the blue V with the name beside it, in a dark version for light backgrounds and
// a light one for the dark footer (public/logo-mork.png, public/logo-ljus.png, made by tools/bilder.py). An uploaded
// logo replaces it at the same height.
export function Wordmark({ content, className = "", onDark = false }: { content: LogoContent; className?: string; onDark?: boolean }) {
  const src = content.logo.kind === "image" ? content.logo.image.src : onDark ? "/logo-ljus.png" : "/logo-mork.png";
  const alt = content.logo.kind === "image" ? content.logo.image.alt || content.name : content.name;
  // eslint-disable-next-line @next/next/no-img-element
  return <img src={withBasePath(src)} alt={alt} width={900} height={320} className={`wordmark h-10 w-auto sm:h-12 ${className}`} />;
}
