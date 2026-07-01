"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, BookOpen } from "lucide-react";

export const CertificationsMarquee = ({ items, posts }: { items: any[]; posts?: any[] }) => {
  // Duplicamos los items más veces para crear el efecto infinito con pocas certificaciones
  const tripledItems = [...items, ...items, ...items, ...items, ...items, ...items];
  const tripledItemsReverse = [...items, ...items, ...items, ...items, ...items, ...items].reverse();

  return (
    <section id="certifications" className="bg-background py-20 overflow-hidden border-y border-white/5">
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
      
      {/* Primera fila - izquierda a derecha */}
      <div className="relative flex overflow-hidden mb-8">
        <motion.div
          className="flex gap-10 sm:gap-20 items-center whitespace-nowrap"
          animate={{ x: ["0%", "-50%"] }}
          transition={{
            duration: 40,
            repeat: Infinity,
            ease: "linear",
          }}
        >
          {tripledItems.map((cert, idx) => {
            const relatedPost = posts?.find((post: any) => post.id === cert.relatedPostId);
            return (
              <div key={`row1-${idx}`} className="flex items-center gap-6 group">
                {cert.badge && cert.badge !== "None" ? (
                  <img
                    src={cert.badge}
                    alt={cert.name}
                    className="h-16 w-auto object-contain grayscale opacity-40 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-500"
                  />
                ) : (
                  <>
                    <div className="h-12 w-12 grayscale opacity-40 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-500 flex items-center justify-center">
                      <img
                        src={`/certifications/${cert.icon}.svg`}
                        alt={cert.name}
                        className="h-10 w-10 object-contain"
                        onError={(e) => {
                          console.error(`Error loading image: /certifications/${cert.icon}.svg`);
                          (e.target as HTMLImageElement).style.display = 'none';
                        }}
                      />
                    </div>
                    <div className="flex flex-col">
                      <span className="text-3xl font-bold tracking-tighter text-white/20 group-hover:text-white transition-colors duration-500 uppercase">
                        {cert.name}
                      </span>
                      {relatedPost && (
                        <Link
                          href={`/blog/${relatedPost.slug}`}
                          className="inline-flex items-center gap-1 text-xs text-white/40 group-hover:text-white/60 transition-colors mt-1"
                        >
                          <BookOpen className="h-3 w-3" />
                          <span>Leer artículo</span>
                        </Link>
                      )}
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </motion.div>
      </div>
      
      {/* Segunda fila - derecha a izquierda */}
      <div className="relative flex overflow-hidden">
        <motion.div
          className="flex gap-10 sm:gap-20 items-center whitespace-nowrap"
          animate={{ x: ["-50%", "0%"] }}
          transition={{
            duration: 40,
            repeat: Infinity,
            ease: "linear",
          }}
        >
          {tripledItemsReverse.map((cert, idx) => {
            const relatedPost = posts?.find((post: any) => post.id === cert.relatedPostId);
            return (
              <div key={`row2-${idx}`} className="flex items-center gap-6 group">
                {cert.badge && cert.badge !== "None" ? (
                  <img
                    src={cert.badge}
                    alt={cert.name}
                    className="h-16 w-auto object-contain grayscale opacity-40 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-500"
                  />
                ) : (
                  <>
                    <div className="h-12 w-12 grayscale opacity-40 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-500 flex items-center justify-center">
                      <img
                        src={`/certifications/${cert.icon}.svg`}
                        alt={cert.name}
                        className="h-10 w-10 object-contain"
                        onError={(e) => {
                          console.error(`Error loading image: /certifications/${cert.icon}.svg`);
                          (e.target as HTMLImageElement).style.display = 'none';
                        }}
                      />
                    </div>
                    <div className="flex flex-col">
                      <span className="text-3xl font-bold tracking-tighter text-white/20 group-hover:text-white transition-colors duration-500 uppercase">
                        {cert.name}
                      </span>
                      {relatedPost && (
                        <Link
                          href={`/blog/${relatedPost.slug}`}
                          className="inline-flex items-center gap-1 text-xs text-white/40 group-hover:text-white/60 transition-colors mt-1"
                        >
                          <BookOpen className="h-3 w-3" />
                          <span>Leer artículo</span>
                        </Link>
                      )}
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
};