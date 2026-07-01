"use client";
import { motion } from "framer-motion";
import { Home, Briefcase, Award, PenTool, Mail } from "lucide-react";
import Link from "next/link";

const DOCK_ITEMS = [
  { icon: <Home className="h-5 w-5" />, label: "Inicio", href: "#hero" },
  { icon: <Briefcase className="h-5 w-5" />, label: "Proyectos", href: "#projects" },
  { icon: <Award className="h-5 w-5" />, label: "Certificados", href: "#certifications" },
  { icon: <PenTool className="h-5 w-5" />, label: "Blog", href: "#blog" },
  { icon: <Mail className="h-5 w-5" />, label: "Contacto", href: "#contact" },
];

export const Dock = () => {
  return (
    <div className="fixed bottom-4 left-1/2 z-50 -translate-x-1/2 w-full max-w-md px-4">
      <motion.div
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="flex items-center justify-center gap-1 sm:gap-2 rounded-full border border-white/10 bg-black/50 p-1 sm:p-2 backdrop-blur-xl mx-auto"
      >
        {DOCK_ITEMS.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className="group relative flex h-10 w-10 sm:h-12 sm:w-12 items-center justify-center rounded-full text-white/50 transition-all hover:bg-white/10 hover:text-white flex-shrink-0"
          >
            {item.icon}
            <span className="absolute -top-10 scale-0 rounded bg-white px-2 py-1 text-[10px] font-bold uppercase text-black transition-all group-hover:scale-100 whitespace-nowrap">
              {item.label}
            </span>
          </Link>
        ))}
      </motion.div>
    </div>
  );
};
