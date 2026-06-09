"use client";
import { motion } from "framer-motion";
import Image from "next/image";

export const CertificationsMarquee = ({ items }: { items: any[] }) => {
  // Duplicamos los items para crear el efecto infinito sin saltos
  const doubledItems = [...items, ...items, ...items];

  return (
    <section className="bg-background py-20 overflow-hidden border-y border-white/5">
      <div className="mb-12 px-6 mx-auto max-w-7xl">
        <span className="text-[10px] font-bold tracking-[0.3em] text-muted-foreground uppercase">
          Reconocimientos y Certificaciones
        </span>
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
              {cert.logo && (
                <div className="relative h-12 w-12 grayscale opacity-40 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-500">
                  <Image
                    src={cert.logo}
                    alt={cert.name}
                    fill
                    className="object-contain"
                  />
                </div>
              )}
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