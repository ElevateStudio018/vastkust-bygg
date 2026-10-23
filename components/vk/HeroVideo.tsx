"use client";

import { useEffect, useRef } from "react";
import { withBasePath } from "@/lib/site/images.ts";

/**
 * The start page's film behind the hero: muted, looping, playing inline on phones and never showing controls or a play
 * button. Where the browser refuses to start it on its own (iPhone in low power mode, data saver), the first frame
 * stays as a still picture and the film starts on the visitor's first touch or scroll. Visitors who ask for less
 * motion get the still picture only.
 */
export function HeroVideo() {
  const box = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = box.current?.querySelector("video");
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      el.removeAttribute("autoplay");
      el.pause();
      return;
    }
    // Set again from script as well; some browsers only trust the property.
    el.muted = true;
    el.defaultMuted = true;
    const start = () => {
      el.play().catch(() => {});
    };
    start();
    const events = ["touchstart", "scroll", "pointerdown", "keydown"] as const;
    const retry = () => {
      start();
      if (!el.paused) events.forEach((name) => window.removeEventListener(name, retry));
    };
    events.forEach((name) => window.addEventListener(name, retry, { passive: true }));
    // Back from another tab or app: carry on where it stopped.
    const visible = () => document.visibilityState === "visible" && start();
    document.addEventListener("visibilitychange", visible);
    return () => {
      events.forEach((name) => window.removeEventListener(name, retry));
      document.removeEventListener("visibilitychange", visible);
    };
  }, []);

  // Phones get the 720p film, larger screens 1080p; MP4 first (smaller, and what iPhones play), WebM for browsers
  // without H.264. Written as plain HTML: React leaves the muted attribute out of the page it renders, and phones only start a film
  // on their own when the attribute is there from the start.
  const html =
    `<video class="hero-video" autoplay muted loop playsinline webkit-playsinline preload="auto" disablepictureinpicture disableremoteplayback ` +
    `aria-hidden="true" tabindex="-1" poster="${withBasePath("/videos/hero-poster.webp")}">` +
    `<source src="${withBasePath("/videos/hero-720.mp4")}" type="video/mp4" media="(max-width: 900px)">` +
    `<source src="${withBasePath("/videos/hero-720.webm")}" type="video/webm" media="(max-width: 900px)">` +
    `<source src="${withBasePath("/videos/hero-1080.mp4")}" type="video/mp4">` +
    `<source src="${withBasePath("/videos/hero-1080.webm")}" type="video/webm">` +
    `</video>`;
  return <div ref={box} className="hero-video-box" dangerouslySetInnerHTML={{ __html: html }} />;
}
