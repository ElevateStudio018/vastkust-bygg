import { Btn, Eyebrow } from "../vk/parts";
import { focusStyle, imageProps } from "@/lib/site/images.ts";
import type { SectionProps } from "./types";

/**
 * Free text: a heading, paragraphs, an optional photo beside them and an optional button. Text sections that follow
 * each other read as one text (a policy, a longer story), so only the first keeps the space above it.
 */
export function TextSection({ section }: SectionProps<"text">) {
  const image = section.image;
  const tone = section.tone === "card" ? " tint" : section.tone === "primary" ? " text-dark" : "";
  return (
    <section id={section.anchor || undefined} className={`sec text-sec${tone}`}>
      <div className={`wrap${image ? " text-grid" : ""}${image && section.imageSide === "left" ? " img-left" : ""}`}>
        <div className="prose">
          <Eyebrow text={section.eyebrow} />
          {section.heading && <h2>{section.heading}</h2>}
          {section.paragraphs.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
          {section.button && <Btn link={section.button} kind={section.tone === "primary" ? "light" : "blue"} arrow />}
        </div>
        {image && (
          <div className="text-img">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img {...imageProps(image, "(min-width: 1000px) 50vw, 100vw")} alt={image.alt} style={focusStyle(image)} loading="lazy" />
          </div>
        )}
      </div>
    </section>
  );
}
