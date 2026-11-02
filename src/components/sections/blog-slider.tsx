"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, BookOpen } from "lucide-react";

const CATEGORY_STYLES: Record<string, string> = {
  novedad: "text-[#57e6e6] border-[#57e6e6]/25 bg-[#57e6e6]/[0.06]",
  alerta: "text-[#ff647c] border-[#ff647c]/25 bg-[#ff647c]/[0.06]",
  descubrimiento: "text-[#c4a7ff] border-[#c4a7ff]/25 bg-[#c4a7ff]/[0.06]",
  creacion: "text-[#b7ff3c] border-[#b7ff3c]/25 bg-[#b7ff3c]/[0.06]",
  seguridad: "text-[#b7ff3c] border-[#b7ff3c]/25 bg-[#b7ff3c]/[0.06]",
  malware: "text-[#ff9a62] border-[#ff9a62]/25 bg-[#ff9a62]/[0.06]",
  opinión: "text-[#c4a7ff] border-[#c4a7ff]/25 bg-[#c4a7ff]/[0.06]",
};

export const BlogSlider = ({ posts }: { posts: any[] }) => (
  <section id="blog" className="border-t border-white/[0.07] px-5 py-24 sm:px-8 lg:px-12 lg:py-32">
    <div className="mx-auto max-w-7xl">
      <div className="mb-12 flex flex-col justify-between gap-6 sm:flex-row sm:items-end">
        <div><p className="section-kicker mb-4">03 / Dispatches & research</p><h2 className="text-5xl font-black tracking-[-.06em] text-white sm:text-7xl">FIELD<span className="neon-text">_NOTES.</span></h2><p className="mt-4 max-w-md text-sm leading-7 text-[#91a0a8]">Ideas, aprendizajes, pruebas, seguridad y tecnología sin convertir cada entrada en un comunicado corporativo.</p></div>
        <Link href="/blog" className="group inline-flex items-center gap-3 border-b border-[#b7ff3c]/40 pb-2 font-mono text-[10px] font-bold uppercase tracking-[.18em] text-[#d8fca5]">Explorar bitácora <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" /></Link>
      </div>
      <div className="grid gap-5 md:grid-cols-2">
        {posts.map((post, i) => (
          <Link key={post.slug} href={`/blog/${post.slug}`} className="group">
            <motion.article initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: .5, delay: i * .1 }}
              className="tech-card flex h-full min-h-64 flex-col rounded-xl p-7 sm:p-9">
              <div className="flex items-center justify-between"><span className={`rounded border px-3 py-1.5 font-mono text-[9px] uppercase tracking-widest ${CATEGORY_STYLES[post.category] || "border-white/15 bg-white/5 text-white/60"}`}>{post.category}</span><BookOpen className="h-4 w-4 text-white/30 transition group-hover:text-[#b7ff3c]" /></div>
              <h3 className="mt-7 max-w-xl text-2xl font-bold leading-tight text-white transition group-hover:text-[#d8fca5] sm:text-3xl">{post.title}</h3>
              <p className="mt-4 line-clamp-3 text-sm leading-7 text-[#91a0a8]">{post.description}</p>
              <div className="mt-auto flex items-center justify-between pt-8 font-mono text-[9px] uppercase tracking-[.18em] text-white/35"><span>{post.readingTime || "—"} min read / dispatch 0{i + 1}</span><ArrowRight className="h-4 w-4 text-[#b7ff3c] transition-transform group-hover:translate-x-1" /></div>
            </motion.article>
          </Link>
        ))}
      </div>
    </div>
  </section>
);
