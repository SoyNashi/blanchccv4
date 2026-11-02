"use client";

import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight, ArrowUpRight, BookOpen } from "lucide-react";
import { useState } from "react";
import Link from "next/link";
import secondaryProjects from "@/data/secondary-projects.json";

export const SecondaryProjects = ({ posts }: { posts?: any[] }) => {
  const [openCategory, setOpenCategory] = useState<string | null>(null);

  return (
    <section id="other-projects" className="px-5 py-20 sm:px-8 lg:px-12">
      <div className="mx-auto max-w-7xl">
        <div className="mb-10"><p className="section-kicker mb-4">Side quests / Experiments</p><h2 className="text-4xl font-black tracking-[-.06em] text-white sm:text-6xl">OTHER<span className="neon-text">_BUILDS.</span></h2><p className="mt-4 max-w-lg text-sm leading-7 text-[#91a0a8]">Colaboraciones, pruebas y proyectos más pequeños que también forman parte del recorrido.</p></div>
        <div className="space-y-3">
          {Object.entries(secondaryProjects).map(([category, projects], index) => (
            <div key={category} className="overflow-hidden rounded-xl border border-white/10 bg-[#0b1116]/80">
              <button type="button" onClick={() => setOpenCategory(openCategory === category ? null : category)} aria-expanded={openCategory === category}
                className="flex w-full items-center justify-between gap-4 p-5 text-left transition hover:bg-white/[0.03] sm:p-7">
                <div className="flex items-center gap-4 sm:gap-6"><span className="font-mono text-[9px] tracking-widest text-[#b7ff3c]">0{index + 1}</span><div><h3 className="text-lg font-bold text-white sm:text-xl">{category}</h3><span className="mt-1 block font-mono text-[9px] uppercase tracking-widest text-white/35">{projects.length} projects archived</span></div></div>
                <ChevronRight className={`h-5 w-5 text-[#b7ff3c] transition-transform ${openCategory === category ? "rotate-90" : ""}`} />
              </button>
              <AnimatePresence>{openCategory === category && <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: .25 }} className="border-t border-white/10">
                <div className="grid gap-3 p-4 sm:grid-cols-2 sm:p-6">
                  {projects.map((project: any, projectIndex: number) => {
                    const relatedPosts = posts?.filter((post: any) => project.relatedPostIds?.includes(post.id)) || [];
                    return <motion.article key={project.id || project.name} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: projectIndex * .04 }} className="rounded-lg border border-white/[0.08] bg-[#080d11] p-5">
                      <div className="flex items-start justify-between gap-4"><div><h4 className="text-lg font-bold text-white">{project.name}</h4><p className="mt-2 text-xs leading-6 text-[#91a0a8]">{project.description}</p></div><a href={project.link} target="_blank" rel="noopener noreferrer" aria-label={`Abrir ${project.name}`} className="rounded border border-white/10 p-2 text-[#b7ff3c] transition hover:bg-[#b7ff3c] hover:text-[#07090d]"><ArrowUpRight className="h-4 w-4" /></a></div>
                      {project.details && <p className="mt-4 text-xs leading-6 text-white/45">{project.details}</p>}
                      <div className="mt-4 flex flex-wrap gap-2">{project.tech.map((tech: string) => <span key={tech} className="rounded border border-white/10 px-2 py-1 font-mono text-[8px] uppercase tracking-wider text-white/55">{tech}</span>)}</div>
                      {relatedPosts.length > 0 && <div className="mt-4 flex flex-wrap gap-2">{relatedPosts.map((post: any) => <Link key={post.id} href={`/blog/${post.slug}`} className="inline-flex items-center gap-2 text-[10px] text-[#57e6e6] hover:text-white"><BookOpen className="h-3 w-3" />{post.title}</Link>)}</div>}
                    </motion.article>;
                  })}
                </div>
              </motion.div>}</AnimatePresence>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
