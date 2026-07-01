"use client";

import { Magnetic } from "@/components/ui/magnetic";

const SOCIAL_LINKS = [
  { name: "LinkedIn", url: "https://linkedin.com/in/nilblanch" },
  { name: "GitHub", url: "https://github.com/nilblanch" },
  { name: "Reddit", url: "https://reddit.com/u/nilblanch" },
  { name: "PayPal", url: "https://paypal.me/nilblanch" },
];

export const Contact = () => {
  return (
    <section id="contact" className="bg-background py-40 px-6 border-t border-white/5">
      <div className="mx-auto max-w-7xl flex flex-col items-center text-center">
        <span className="text-xs font-bold tracking-[0.2em] text-muted-foreground uppercase mb-12">
          ¿Hablamos?
        </span>
        
        <Magnetic>
          <a href="mailto:nil@blanch.cc">
            <h2 className="text-4xl sm:text-5xl md:text-6xl lg:text-huge font-bold tracking-tighter text-white mb-12 cursor-pointer hover:text-white/80 transition-colors break-words px-4">
              NIL@BLANCH.CC
            </h2>
          </a>
        </Magnetic>
        
        <div className="flex flex-wrap justify-center gap-4 sm:gap-8">
          {SOCIAL_LINKS.map((link) => (
            <Magnetic key={link.name}>
              <a
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors p-2 sm:p-4"
              >
                {link.name}
              </a>
            </Magnetic>
          ))}
        </div>
        
        <p className="mt-40 text-[10px] font-mono text-white/20 uppercase tracking-[0.3em]">
          © 2024 Nil Blanch — All Rights Reserved
        </p>
      </div>
    </section>
  );
};
