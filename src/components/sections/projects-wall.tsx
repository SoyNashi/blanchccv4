"use client";
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import Image from "next/image";
import Link from "next/link";
import { BookOpen } from "lucide-react";

export const ProjectsWall = ({ projects, posts }: { projects: any[]; posts?: any[] }) => {
  return (
    <section id="projects" className="bg-background py-20">
      <div className="flex flex-col gap-40">
        {projects.map((project, index) => (
          <ProjectItem key={project.id} project={project} index={index} posts={posts} />
        ))}
      </div>
    </section>
  );
};

const ProjectItem = ({ project, index, posts }: { project: any; index: number; posts?: any[] }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [0.9, 1, 0.9]);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]);

  // Encontrar los posts asociados
  const relatedPosts = posts?.filter((post: any) => project.relatedPostIds?.includes(post.id)) || [];

  return (
    <motion.div
      ref={containerRef}
      style={{ opacity }}
      className="relative flex min-h-[80vh] w-full flex-col items-center justify-center px-6"
    >
      <div className="grid w-full max-w-7xl grid-cols-1 gap-12 md:grid-cols-2 lg:items-center">
        <div className={`order-2 flex flex-col gap-6 ${index % 2 === 0 ? "lg:order-1" : "lg:order-2"}`}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <span className="text-xs font-bold tracking-[0.2em] text-muted-foreground uppercase">
              Case Study — 0{index + 1}
            </span>
            <h2 className="mt-4 text-6xl font-bold tracking-tighter text-white sm:text-7xl">
              {project.title}
            </h2>
          </motion.div>
          
          <motion.p
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="max-w-md text-xl leading-relaxed text-muted-foreground"
          >
            {project.description}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="grid grid-cols-1 gap-6 border-t border-white/10 pt-8 sm:grid-cols-3"
          >
            {project.tech.map((item: any) => (
              <div key={item.label} className="flex flex-col gap-1">
                <span className="text-[10px] font-bold tracking-widest text-muted-foreground uppercase">
                  {item.label}
                </span>
                <span className="text-sm font-medium text-white/80">
                  {item.value}
                </span>
              </div>
            ))}
          </motion.div>

          {relatedPosts.length > 0 && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="mt-4 flex flex-wrap gap-2"
            >
              {relatedPosts.map((post: any) => (
                <Link
                  key={post.id}
                  href={`/blog/${post.slug}`}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-colors group"
                >
                  <BookOpen className="h-4 w-4 text-white/60 group-hover:text-white" />
                  <span className="text-sm font-medium text-white/60 group-hover:text-white">
                    {post.title}
                  </span>
                </Link>
              ))}
            </motion.div>
          )}
        </div>

        <motion.div
          style={{ y, scale }}
          className={`order-1 flex aspect-[4/5] w-full overflow-hidden bg-muted lg:aspect-square ${index % 2 === 0 ? "lg:order-2" : "lg:order-1"}`}
        >
          <div className="relative h-full w-full grayscale transition-all duration-700 hover:grayscale-0">
            <Image
              src={project.image}
              alt={project.title}
              fill
              className="object-cover transition-transform duration-700 hover:scale-105"
            />
            <div className="absolute inset-0 bg-black/20" />
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};
