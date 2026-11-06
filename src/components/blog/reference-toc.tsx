"use client";

import { useEffect, useState, type MouseEvent } from "react";

type Heading = { level: number; text: string; id: string };

export default function ReferenceToc({ headings }: { headings: Heading[] }) {
  const [active, setActive] = useState(headings[0]?.id || "");

  useEffect(() => {
    const elements = headings
      .map((heading) => document.getElementById(heading.id))
      .filter((element): element is HTMLElement => element !== null);

    if (!elements.length) return;

    let frame = 0;
    const updateActiveHeading = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const activationLine = Math.min(180, window.innerHeight * 0.3);
        let current = elements[0];

        for (const element of elements) {
          if (element.getBoundingClientRect().top <= activationLine) {
            current = element;
          } else {
            break;
          }
        }

        setActive(current.id);
      });
    };

    window.addEventListener("scroll", updateActiveHeading, { passive: true });
    window.addEventListener("resize", updateActiveHeading);
    updateActiveHeading();

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", updateActiveHeading);
      window.removeEventListener("resize", updateActiveHeading);
    };
  }, [headings]);

  const navigateToHeading = (
    event: MouseEvent<HTMLAnchorElement>,
    id: string,
  ) => {
    event.preventDefault();
    const target = document.getElementById(id);
    if (!target) return;

    setActive(id);
    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    const top = target.getBoundingClientRect().top + window.scrollY - 112;

    window.scrollTo({
      top: Math.max(0, top),
      behavior: reducedMotion ? "auto" : "smooth",
    });
    window.history.replaceState(null, "", `#${id}`);
  };

  return (
    <aside className="toc">
      <span className="mono">EN ESTE ARTÍCULO</span>
      <nav aria-label="Índice del artículo">
        {headings.map((heading) => (
          <a
            key={heading.id}
            href={`#${heading.id}`}
            onClick={(event) => navigateToHeading(event, heading.id)}
            className={active === heading.id ? "on" : ""}
            data-level={heading.level}
            aria-current={active === heading.id ? "location" : undefined}
          >
            {heading.text}
          </a>
        ))}
      </nav>
    </aside>
  );
}
