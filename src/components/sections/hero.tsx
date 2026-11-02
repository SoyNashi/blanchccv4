"use client";

import { motion } from "framer-motion";
import { ArrowDown, ArrowUpRight, Cpu, LockKeyhole, Network, RadioTower } from "lucide-react";

const signals = [
  { icon: Network, label: "Redes & sistemas" },
  { icon: LockKeyhole, label: "Seguridad & privacidad" },
  { icon: Cpu, label: "Producto & desarrollo" },
];

export const Hero = () => (
  <section id="hero" className="relative isolate flex min-h-[92svh] w-full items-center overflow-hidden px-5 pb-24 pt-28 sm:px-8 lg:px-12">
    <div className="site-grid absolute inset-0 -z-10" />
    <div className="absolute -right-32 top-20 -z-10 h-[28rem] w-[28rem] rounded-full bg-[#b7ff3c]/[0.07] blur-[110px]" />
    <div className="absolute -left-40 bottom-0 -z-10 h-[26rem] w-[26rem] rounded-full bg-[#57e6e6]/[0.07] blur-[110px]" />

    <div className="mx-auto grid w-full max-w-7xl items-center gap-14 lg:grid-cols-[1.15fr_.85fr]">
      <div>
        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .6 }}
          className="mb-8 inline-flex items-center gap-3 rounded-full border border-[#b7ff3c]/25 bg-[#b7ff3c]/[0.06] px-4 py-2">
          <span className="relative flex h-2 w-2"><span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#b7ff3c] opacity-50" /><span className="relative inline-flex h-2 w-2 rounded-full bg-[#b7ff3c]" /></span>
          <span className="font-mono text-[10px] uppercase tracking-[.2em] text-[#d8fca5]">Independent digital lab · Barcelona</span>
        </motion.div>

        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .15 }} className="section-kicker mb-5">Nil Blanch / Portfolio & field notes</motion.p>
        <motion.h1 initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .7, delay: .1 }}
          className="max-w-4xl text-6xl font-black leading-[.88] tracking-[-.075em] text-white sm:text-7xl md:text-8xl xl:text-[7.7rem]">
          BUILD THE<br /><span className="neon-text">NETWORK.</span><br />QUESTION<br />THE SYSTEM.
        </motion.h1>
        <motion.p initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .3 }}
          className="mt-8 max-w-xl text-base leading-8 text-[#a9b7bc] sm:text-lg">
          Desarrollo productos digitales, exploro cómo se conectan los sistemas y me interesa especialmente lo que ocurre detrás de la pantalla: redes, infraestructura, seguridad y privacidad.
        </motion.p>

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: .45 }} className="mt-9 flex flex-wrap gap-3">
          <a href="#projects" className="inline-flex items-center gap-3 rounded-sm bg-[#b7ff3c] px-5 py-3.5 text-xs font-black uppercase tracking-[.14em] text-[#07090d] transition hover:bg-white">
            Explorar proyectos <ArrowUpRight className="h-4 w-4" />
          </a>
          <a href="#about-focus" className="inline-flex items-center gap-3 rounded-sm border border-white/15 px-5 py-3.5 text-xs font-bold uppercase tracking-[.14em] text-white transition hover:border-[#57e6e6]/60 hover:text-[#57e6e6]">
            Mi enfoque <ArrowDown className="h-4 w-4" />
          </a>
        </motion.div>
      </div>

      <motion.div initial={{ opacity: 0, scale: .96, x: 20 }} animate={{ opacity: 1, scale: 1, x: 0 }} transition={{ duration: .8, delay: .25 }}
        className="terminal-panel scanlines relative mx-auto w-full max-w-xl overflow-hidden rounded-2xl p-5 sm:p-7">
        <div className="mb-8 flex items-center justify-between border-b border-white/10 pb-4">
          <div className="flex items-center gap-2"><span className="h-2.5 w-2.5 rounded-full bg-[#ff647c]" /><span className="h-2.5 w-2.5 rounded-full bg-[#f5c451]" /><span className="h-2.5 w-2.5 rounded-full bg-[#b7ff3c]" /></div>
          <span className="font-mono text-[9px] uppercase tracking-[.2em] text-white/35">NB // SYSTEM MAP</span>
          <RadioTower className="h-4 w-4 text-[#b7ff3c]" />
        </div>
        <div className="relative flex min-h-[19rem] items-center justify-center">
          <div className="absolute h-56 w-56 rounded-full border border-dashed border-[#57e6e6]/20 animate-[spin_55s_linear_infinite]" />
          <div className="absolute h-40 w-40 rounded-full border border-[#b7ff3c]/20" />
          <div className="absolute h-28 w-28 rounded-full border border-[#57e6e6]/25" />
          <div className="absolute h-2 w-2 translate-x-24 -translate-y-20 rounded-full bg-[#57e6e6] shadow-[0_0_18px_#57e6e6]" />
          <div className="absolute h-2 w-2 -translate-x-24 translate-y-16 rounded-full bg-[#b7ff3c] shadow-[0_0_18px_#b7ff3c]" />
          <div className="absolute h-2 w-2 translate-x-8 translate-y-28 rounded-full bg-[#a78bfa] shadow-[0_0_18px_#a78bfa]" />
          <div className="relative z-10 flex h-24 w-24 flex-col items-center justify-center rounded-2xl border border-[#b7ff3c]/45 bg-[#b7ff3c]/[0.08] shadow-[0_0_55px_rgba(183,255,60,.1)]">
            <Network className="h-8 w-8 text-[#b7ff3c]" /><span className="mt-2 font-mono text-[8px] tracking-[.2em] text-white/70">NODE_01</span>
          </div>
          <span className="absolute left-0 top-8 font-mono text-[9px] text-[#57e6e6]/70">ROUTING / 001</span>
          <span className="absolute bottom-8 right-0 font-mono text-[9px] text-[#b7ff3c]/70">SECURITY / ACTIVE</span>
        </div>
        <div className="grid grid-cols-3 gap-2 border-t border-white/10 pt-5">
          {signals.map(({ icon: Icon, label }, i) => <div key={label} className="flex flex-col gap-2"><Icon className="h-4 w-4 text-[#b7ff3c]" /><span className="font-mono text-[8px] uppercase leading-4 tracking-wider text-white/50 sm:text-[9px]">{label}</span><span className="font-mono text-[8px] text-[#57e6e6]">0{i + 1} / FIELD</span></div>)}
        </div>
      </motion.div>
    </div>

    <div className="absolute bottom-7 left-6 hidden items-center gap-3 font-mono text-[9px] uppercase tracking-[.2em] text-white/30 sm:flex"><span className="h-px w-10 bg-[#b7ff3c]/50" />Scroll to explore</div>
    <div className="absolute bottom-7 right-6 font-mono text-[9px] tracking-widest text-white/25">41°33' N / 02°24' E</div>
  </section>
);
