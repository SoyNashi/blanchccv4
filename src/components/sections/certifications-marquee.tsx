"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

const ICONS: Record<string, string> = {
  aws: "☁️",
  gcp: "🔷",
  mongodb: "🍃",
  react: "⚛️",
  nextjs: "▲",
};

export const CertificationsMarquee = ({ items }: { items: any[] }) => {
  // Duplicamos los items para crear el efecto infinito sin saltos
  const doubledItems = [...items, ...items, ...items];

  return (
    <section className="bg-background py-20 overflow-hidden border-y border-white/5">
      <div className="mb-12 px-6 mx-auto max-w-7xl flex items-center justify-between">
        <span className="text-[10px] font-bold tracking-[0.3em] text-muted-foreground uppercase">
          Reconocimientos y Certificaciones
        </span>
        <Link 
          href="/certifications" 
          className="group flex items-center gap-2 text-xs font-bold tracking-widest text-white uppercase hover:text-white/80 transition-colors"
        >
          Ver todas <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-1" />
        </Link>
      </div>
      
      <div className="relative flex">
        <motion.div
          className="flex gap-20 items-center whitespace-nowrap"
          animate={{ x: ["0%", "-33.33%"] }}
          transition={{
            duration: 30,
            repeat: Infinity,
            ease: "linear",
          }}
        >
          {doubledItems.map((cert, idx) => (
            <div key={idx} className="flex items-center gap-6 group">
              <div className="text-3xl grayscale opacity-40 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-500">
                {ICONS[cert.icon] || "📜"}
              </div>
              <span className="text-3xl font-bold tracking-tighter text-white/20 group-hover:text-white transition-colors duration-500 uppercase">
                {cert.name}
              </span>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};