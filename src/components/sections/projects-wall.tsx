"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, Network, ShoppingBag, Workflow } from "lucide-react";

const projectIcons = [Workflow, ShoppingBag, Network];

export const ProjectsWall = ({ projects, posts }: { projects: any[]; posts?: any[] }) => (
  <section id="projects" className="relative px-5 py-24 sm:px-8 lg:px-12 lg:py-32">
    <div className="mx-auto max-w-7xl">
      <div className="mb-12 flex flex-col justify-between gap-6 md:mb-16 md:flex-row md:items-end">
        <div><p className="section-kicker mb-4">01 / Selected work</p><h2 className="text-5xl font-black tracking-[-.06em] text-white sm:text-7xl">PROJECT<span className="neon-text">_INDEX</span></h2></div>
        <p className="max-w-sm text-sm leading-7 text-[#91a0a8]">Tres líneas de trabajo, tres problemas distintos. Proyectos propios y colaboraciones en diferentes fases de desarrollo.</p>
      </div>
      <div className="grid gap-5 lg:grid-cols-3">
        {projects.map((project, index) => {
          const Icon = projectIcons[index] || Network;
          const isGhostnet = project.slug === "ghostnet";
          const relatedPosts = posts?.filter((post: any) => project.relatedPostIds?.includes(post.id)) || [];
          return (
            <motion.article key={project.id} initial={{ opacity: 0, y: 28 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: .15 }} transition={{ duration: .55, delay: index * .08 }}
              className="tech-card group relative flex min-h-[34rem] flex-col overflow-hidden rounded-xl">
              <div className="relative h-64 overflow-hidden border-b border-white/10 bg-[#0b1217]">
                {project.image ? <Image src={project.image} alt={project.title} fill sizes="(max-width: 1024px) 100vw, 33vw" className="object-cover opacity-70 transition duration-700 group-hover:scale-105 group-hover:opacity-90" /> :
                  <div className="site-grid absolute inset-0 flex items-center justify-center"><div className="absolute h-48 w-48 rounded-full border border-dashed border-[#57e6e6]/25" /><div className="absolute h-36 w-36 rounded-full border border-[#b7ff3c]/30" /><div className="relative flex h-20 w-20 items-center justify-center rounded-2xl border border-[#57e6e6]/50 bg-[#57e6e6]/10 text-[#57e6e6] shadow-[0_0_45px_rgba(87,230,230,.12)]"><Icon className="h-9 w-9" /></div><span className="absolute left-5 top-5 font-mono text-[9px] tracking-[.2em] text-[#57e6e6]/70">GHOSTNET // NODE MAP</span><span className="absolute bottom-5 right-5 font-mono text-[9px] text-white/35">NETWORK CONCEPT</span></div>}
                <div className="absolute inset-0 bg-gradient-to-t from-[#0b1015] via-transparent to-black/10" />
                <span className="absolute right-4 top-4 rounded border border-white/15 bg-black/50 px-3 py-1.5 font-mono text-[9px] uppercase tracking-widest text-white/70">0{index + 1} / {project.status || "Project"}</span>
              </div>
              <div className="flex flex-1 flex-col p-6 sm:p-7">
                <div className="mb-4 flex items-center justify-between"><span className="section-kicker">{isGhostnet ? "Network / Privacy" : index === 0 ? "Digital platform" : "Independent brand"}</span><Icon className="h-5 w-5 text-[#b7ff3c]" /></div>
                <h3 className="text-3xl font-black tracking-tight text-white">{project.title}</h3>
                <p className="mt-4 flex-1 text-sm leading-7 text-[#a5b3b8]">{project.description}</p>
                {project.details && <p className="mt-3 text-xs leading-6 text-white/45">{project.details}</p>}
                <div className="mt-6 flex flex-wrap gap-2">{project.tags?.map((tag: string) => <span key={tag} className="rounded border border-white/10 bg-white/[0.03] px-2.5 py-1.5 font-mono text-[9px] uppercase tracking-wider text-white/55">{tag}</span>)}</div>
                <div className="mt-6 grid grid-cols-2 gap-3 border-t border-white/10 pt-5">{project.tech?.slice(0, 4).map((item: any) => <div key={item.label}><span className="block font-mono text-[8px] uppercase tracking-[.18em] text-white/35">{item.label}</span><span className="mt-1 block text-xs text-white/75">{item.value}</span></div>)}</div>
                {relatedPosts.length > 0 && <Link href={`/blog/${relatedPosts[0].slug}`} className="mt-5 inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-[#57e6e6] hover:text-white">Leer notas relacionadas <ArrowUpRight className="h-4 w-4" /></Link>}
              </div>
            </motion.article>
          );
        })}
      </div>
    </div>
  </section>
);
