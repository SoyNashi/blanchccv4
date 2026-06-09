"use client";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";

const SECONDARY_PROJECTS = [
  {
    name: "Argentona Bocs",
    description: "Plataforma de gestión y comunicación para entidades locales.",
    category: "Web Platform",
  },
  {
    name: "Instint Global",
    description: "Estrategia digital y presencia online para marca de lifestyle.",
    category: "Brand Strategy",
  },
  {
    name: "Core System",
    description: "Librería de componentes internos optimizados para alto rendimiento.",
    category: "Open Source",
  },
  {
    name: "Data Flow",
    description: "Pipeline de datos automatizado para análisis de publicidad exterior.",
    category: "Engineering",
  },
];

export const SecondaryProjects = () => {
  return (
    <section className="bg-background py-40 px-6">
      <div className="mx-auto max-w-7xl">
        <div className="mb-20">
          <span className="text-xs font-bold tracking-[0.2em] text-muted-foreground uppercase">
            Más Construcciones
          </span>
          <h2 className="mt-6 text-5xl font-bold tracking-tighter text-white sm:text-7xl">
            OTROS PROYECTOS.
          </h2>
        </div>

        <div className="grid grid-cols-1 gap-4">
          {SECONDARY_PROJECTS.map((project, index) => (
            <motion.div
              key={project.name}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group relative flex items-center justify-between border-b border-white/5 py-12 transition-colors hover:border-white/20"
            >
              <div className="flex flex-col gap-2">
                <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
                  {project.category}
                </span>
                <h3 className="text-3xl font-bold text-white transition-transform group-hover:translate-x-2">
                  {project.name}
                </h3>
                <p className="max-w-xl text-lg text-muted-foreground">
                  {project.description}
                </p>
              </div>
              
              <div className="hidden h-12 w-12 items-center justify-center rounded-full border border-white/10 text-white transition-all group-hover:bg-white group-hover:text-black md:flex">
                <ArrowUpRight className="h-5 w-5" />
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};
