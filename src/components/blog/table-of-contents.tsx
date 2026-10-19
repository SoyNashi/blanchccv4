"use client";

import { useEffect, useState } from "react";

type Heading = {
  level: number;
  text: string;
  id: string;
};

export default function TableOfContents({ headings }: { headings: Heading[] }) {
  const [activeId, setActiveId] = useState(headings[0]?.id ?? "");

  useEffect(() => {
    if (!headings.length) return;

    const elements = headings
      .map((heading) => document.getElementById(heading.id))
      .filter((element): element is HTMLElement => element instanceof HTMLElement);

    if (!elements.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

        if (visible[0]?.target instanceof HTMLElement) {
          setActiveId(visible[0].target.id);
        }
      },
      {
        rootMargin: "-12% 0px -72% 0px",
        threshold: 0,
      }
    );

    elements.forEach((element) => observer.observe(element));

    const updateFromScroll = () => {
      const marker = 150;
      let current = elements[0];

      for (const element of elements) {
        if (element.getBoundingClientRect().top <= marker) current = element;
        else break;
      }

      if (current) setActiveId(current.id);
    };

    window.addEventListener("scroll", updateFromScroll, { passive: true });
    updateFromScroll();

    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", updateFromScroll);
    };
  }, [headings]);

  return (
    <div className="sticky top-8 max-h-[calc(100vh-4rem)] overflow-y-auto overscroll-contain bg-card border border-white/5 rounded-2xl p-5">
      <h3 className="text-sm font-bold tracking-widest text-white uppercase mb-4">
        Contenido
      </h3>
      <nav aria-label="Tabla de contenido" className="space-y-2">
        {headings.map((heading, index) => {
          const active = activeId === heading.id;

          return (
            <a
              key={`${heading.id}-${index}`}
              href={`#${heading.id}`}
              aria-current={active ? "location" : undefined}
              aria-label={`Ir a sección ${heading.text}`}
              className={`block rounded-sm transition-colors hover:text-white ${ 
                active
                  ? "font-bold text-white"
                  : heading.level === 1
                    ? "font-semibold text-white/75"
                    : heading.level === 2
                      ? "font-medium text-white/65"
                      : "text-white/50"
              } ${heading.level === 2 ? "ml-2" : heading.level >= 3 ? "ml-4" : ""}`}
            >
              {heading.text}
            </a>
          );
        })}
      </nav>
    </div>
  );
}
