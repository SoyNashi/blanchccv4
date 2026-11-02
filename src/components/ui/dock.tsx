"use client";

import { motion } from "framer-motion";
import { Home, Briefcase, Award, Radio, Mail } from "lucide-react";
import Link from "next/link";

const DOCK_ITEMS = [
  { icon: <Home className="h-4 w-4" />, label: "Inicio", href: "#hero" },
  { icon: <Briefcase className="h-4 w-4" />, label: "Proyectos", href: "#projects" },
  { icon: <Radio className="h-4 w-4" />, label: "Enfoque", href: "#about-focus" },
  { icon: <Award className="h-4 w-4" />, label: "Certificados", href: "#certifications" },
  { icon: <Mail className="h-4 w-4" />, label: "Contacto", href: "#contact" },
];

export const Dock = () => (
  <div className="fixed bottom-4 left-1/2 z-50 w-full max-w-md -translate-x-1/2 px-4">
    <motion.nav initial={{ y: 80, opacity: 0 }} animate={{ y: 0, opacity: 1 }} aria-label="Navegación principal"
      className="mx-auto flex items-center justify-center gap-1 rounded-xl border border-[#b7ff3c]/20 bg-[#080d11]/85 p-1.5 shadow-[0_12px_50px_rgba(0,0,0,.5)] backdrop-blur-2xl sm:gap-2 sm:p-2">
      {DOCK_ITEMS.map(item => (
        <Link key={item.label} href={item.href} aria-label={item.label}
          className="group relative flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg text-white/55 transition hover:bg-[#b7ff3c]/10 hover:text-[#b7ff3c] sm:h-11 sm:w-11">
          {item.icon}
          <span className="pointer-events-none absolute -top-10 scale-0 whitespace-nowrap rounded border border-[#b7ff3c]/25 bg-[#0b1116] px-2.5 py-1.5 font-mono text-[9px] uppercase tracking-widest text-[#d8fca5] opacity-0 transition group-hover:scale-100 group-hover:opacity-100">{item.label}</span>
        </Link>
      ))}
    </motion.nav>
  </div>
);
