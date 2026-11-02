"use client";

import { ArrowUpRight, Mail } from "lucide-react";

const SOCIAL_LINKS = [
  { name: "LinkedIn", url: "https://linkedin.com/in/nilblanch" },
  { name: "GitHub", url: "https://github.com/nilblanch" },
  { name: "Reddit", url: "https://reddit.com/u/nilblanch" },
];

export const Contact = () => (
  <footer id="contact" className="relative overflow-hidden border-t border-white/10 px-5 pb-28 pt-24 sm:px-8 lg:px-12 lg:pt-32">
    <div className="absolute -bottom-40 left-1/2 h-96 w-[42rem] -translate-x-1/2 rounded-full bg-[#b7ff3c]/[0.06] blur-[100px]" />
    <div className="relative mx-auto max-w-7xl">
      <p className="section-kicker mb-6">04 / Open channel</p>
      <div className="grid gap-10 md:grid-cols-[1fr_auto] md:items-end">
        <div><h2 className="max-w-4xl break-words text-5xl font-black tracking-[-.07em] text-white sm:text-7xl lg:text-8xl">HAVE A<br /><span className="neon-text">GOOD SIGNAL?</span></h2><p className="mt-6 max-w-lg text-sm leading-7 text-[#91a0a8]">Ideas, colaboraciones, proyectos o una conversación técnica. El canal está abierto.</p></div>
        <a href="mailto:nil@blanch.cc" className="inline-flex w-fit items-center gap-3 border border-[#b7ff3c]/40 bg-[#b7ff3c]/[0.07] px-5 py-4 font-mono text-xs font-bold tracking-widest text-[#d9ffab] transition hover:bg-[#b7ff3c] hover:text-[#07090d]"><Mail className="h-4 w-4" /> NIL@BLANCH.CC <ArrowUpRight className="h-4 w-4" /></a>
      </div>
      <div className="mt-20 flex flex-col justify-between gap-7 border-t border-white/10 pt-7 sm:flex-row sm:items-center">
        <div className="font-mono text-[9px] uppercase tracking-[.2em] text-white/35">© {new Date().getFullYear()} Nil Blanch · Built with intent.</div>
        <nav aria-label="Redes sociales" className="flex flex-wrap gap-7">{SOCIAL_LINKS.map(link => <a key={link.name} href={link.url} target="_blank" rel="noopener noreferrer" className="font-mono text-[10px] uppercase tracking-[.18em] text-white/50 transition hover:text-[#b7ff3c]">{link.name}</a>)}</nav>
      </div>
    </div>
  </footer>
);
