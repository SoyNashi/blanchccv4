"use client";
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import Image from "next/image";

const PROJECTS = [
  {
    id: "blau360",
    title: "Blau360",
    description: "Digitalización a medida para PYMES y publicidad exterior. Construyendo puentes entre el mundo físico y digital.",
    tags: ["Product Strategy", "Full Stack Dev", "Consulting"],
    tech: [
      { label: "Frontend", value: "Next.js / React" },
      { label: "Backend", value: "Node.js / PostgreSQL" },
      { label: "Infrastructure", value: "AWS / Docker" },
    ],
    color: "#0055ff",
    image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=2426",
  },
  {
    id: "bastet",
    title: "Bastet Project",
    description: "Marca de ropa impulsada por valores y comunidad. Un ecosistema donde el diseño y la identidad convergen.",
    tags: ["E-commerce", "Brand Identity", "UX Design"],
    tech: [
      { label: "Storefront", value: "Shopify / Liquid" },
      { label: "Automation", value: "Klaviyo / Zapier" },
      { label: "Analytics", value: "GA4 / GTM" },
    ],
    color: "#ff3300",
    image: "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?auto=format&fit=crop&q=80&w=2340",
  },
];

export const ProjectsWall = () => {
  return (
    <section className="bg-background py-20">
      <div className="flex flex-col gap-40">
        {PROJECTS.map((project, index) => (
          <ProjectItem key={project.id} project={project} index={index} />
        ))}
      </div>
    </section>
  );
};

const ProjectItem = ({ project, index }: { project: typeof PROJECTS[0]; index: number }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [0.9, 1, 0.9]);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]);

  return (
    <motion.div
      ref={containerRef}
      style={{ opacity }}
      className="relative flex min-h-[80vh] w-full flex-col items-center justify-center px-6"
    >
      <div className="grid w-full max-w-7xl grid-cols-1 gap-12 lg:grid-cols-2 lg:items-center">
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
            {project.tech.map((item) => (
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
