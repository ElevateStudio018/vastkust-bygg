"use client";

import { Children, cloneElement, isValidElement, useEffect, useRef, useState, type ReactElement, type ReactNode } from "react";
import { Icon } from "../Icon";

/** Pixels a second: the steady roll, and the slow roll while the pointer is over the reviews. */
const SPEED = 38;
const SLOW = 9;
/** How long the roll waits after the visitor scrolls, swipes or uses the arrows themselves. */
const PAUSE_MS = 4000;
/** Fewer reviews than this fit on the screen anyway, so they stand still. */
const MIN_TO_ROLL = 4;

/**
 * The reviews in a row that rolls by on its own and slows down under the mouse. The row is drawn twice so it can loop
 * without a jump; the copy is hidden from screen readers and the keyboard. The arrows and swiping still work, and the
 * roll stands still for visitors who have asked for less motion.
 */
export function ReviewSlider({ head, aside, children, labels }: { head: ReactNode; aside?: ReactNode; children: ReactNode; labels: { previous: string; next: string } }) {
  const track = useRef<HTMLUListElement>(null);
  const hovering = useRef(false);
  const pausedUntil = useRef(0);
  const items = Children.toArray(children).filter(isValidElement) as ReactElement[];
  const loops = items.length >= MIN_TO_ROLL;
  const [rolling, setRolling] = useState(false);
  const [atStart, setAtStart] = useState(true);
  const [atEnd, setAtEnd] = useState(false);

  // Where the copy starts: scrolling that far shows exactly what the start showed.
  const loopWidth = (el: HTMLElement) => {
    const copy = el.querySelector<HTMLElement>("[data-copy]");
    const first = el.firstElementChild as HTMLElement | null;
    return copy && first ? copy.offsetLeft - first.offsetLeft : 0;
  };

  useEffect(() => {
    const el = track.current;
    if (!el) return;
    el.querySelectorAll("[data-copy]").forEach((node) => node.setAttribute("inert", ""));

    const updateEnds = () => {
      if (loops) return;
      setAtStart(el.scrollLeft < 4);
      setAtEnd(el.scrollLeft + el.clientWidth >= el.scrollWidth - 4);
    };
    updateEnds();
    el.addEventListener("scroll", updateEnds, { passive: true });
    window.addEventListener("resize", updateEnds);

    const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let frame = 0;
    if (loops && !still) {
      setRolling(true);
      let speed = 0;
      let last = performance.now();
      let position = el.scrollLeft;
      const tick = (now: number) => {
        const seconds = Math.min(now - last, 64) / 1000;
        last = now;
        if (now < pausedUntil.current) {
          speed = 0;
          position = el.scrollLeft;
        } else {
          const target = hovering.current ? SLOW : SPEED;
          speed += (target - speed) * Math.min(1, seconds * 3);
          if (Math.abs(el.scrollLeft - position) > 2) position = el.scrollLeft;
          position += speed * seconds;
          const width = loopWidth(el);
          if (width > 0 && position >= width) position -= width;
          el.scrollLeft = position;
        }
        frame = requestAnimationFrame(tick);
      };
      frame = requestAnimationFrame(tick);
    }

    const pause = () => (pausedUntil.current = performance.now() + PAUSE_MS);
    el.addEventListener("pointerdown", pause);
    el.addEventListener("wheel", pause, { passive: true });
    el.addEventListener("focusin", pause);
    return () => {
      cancelAnimationFrame(frame);
      el.removeEventListener("scroll", updateEnds);
      window.removeEventListener("resize", updateEnds);
      el.removeEventListener("pointerdown", pause);
      el.removeEventListener("wheel", pause);
      el.removeEventListener("focusin", pause);
    };
  }, [loops]);

  function step(direction: 1 | -1) {
    const el = track.current;
    if (!el) return;
    pausedUntil.current = performance.now() + PAUSE_MS;
    const item = el.querySelector("li");
    const gap = parseFloat(getComputedStyle(el).columnGap || "0") || 0;
    const distance = item ? item.getBoundingClientRect().width + gap : el.clientWidth;
    // Going back from the very start: jump to the same spot in the copy first, so there is somewhere to go.
    if (loops && direction < 0 && el.scrollLeft < distance) el.scrollLeft += loopWidth(el);
    el.scrollBy({ left: direction * distance, behavior: "smooth" });
  }

  return (
    <>
      <div className="sec-head">
        {head}
        <div className="rev-nav">
          {aside}
          <span className="rev-btns">
            <button type="button" aria-label={labels.previous} disabled={!loops && atStart} onClick={() => step(-1)}>
              <Icon name="ChevronLeft" className="ic" />
            </button>
            <button type="button" aria-label={labels.next} disabled={!loops && atEnd} onClick={() => step(1)}>
              <Icon name="ChevronRight" className="ic" />
            </button>
          </span>
        </div>
      </div>
      <div className="rev-slider" onPointerEnter={() => (hovering.current = true)} onPointerLeave={() => (hovering.current = false)}>
        <ul className={`rev-track${rolling ? " rolling" : ""}`} ref={track} tabIndex={0}>
          {items}
          {loops && items.map((item, index) => cloneElement(item as ReactElement<Record<string, unknown>>, { key: `copy-${item.key ?? index}`, "aria-hidden": true, "data-copy": "" }))}
        </ul>
      </div>
    </>
  );
}
