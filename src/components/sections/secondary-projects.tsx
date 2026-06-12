"use client";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronRight, ArrowUpRight } from "lucide-react";
import { useState } from "react";
import secondaryProjects from "@/data/secondary-projects.json";

export const SecondaryProjects = () => {
  const [openCategory, setOpenCategory] = useState<string | null>(null);

  return (
    <section id="other-projects" className="bg-background py-40 px-6">
      <div className="mx-auto max-w-7xl">
        <div className="mb-20">
          <span className="text-xs font-bold tracking-[0.2em] text-muted-foreground uppercase">
            Más Construcciones
          </span>
          <h2 className="mt-6 text-5xl font-bold tracking-tighter text-white sm:text-7xl">
            OTROS PROYECTOS.
          </h2>
        </div>

        <div className="space-y-4">
          {Object.entries(secondaryProjects).map(([category, projects], index) => (
            <div key={category} className="border border-white/5 rounded-2xl overflow-hidden">
              <motion.button
                onClick={() => setOpenCategory(openCategory === category ? null : category)}
                className="w-full flex items-center justify-between p-6 hover:bg-white/5 transition-colors"
                initial={false}
              >
                <div className="flex items-center gap-4">
                  <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
                    {projects.length} proyectos
                  </span>
                  <h3 className="text-2xl font-bold text-white">{category}</h3>
                </div>
                <motion.div
                  animate={{ rotate: openCategory === category ? 90 : 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <ChevronRight className="h-5 w-5 text-white/40" />
                </motion.div>
              </motion.button>

              <AnimatePresence>
                {openCategory === category && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="border-t border-white/5"
                  >
                    <div className="p-6 space-y-4">
                      {projects.map((project: any, projectIndex: number) => (
                        <motion.div
                          key={project.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: projectIndex * 0.1 }}
                          className="bg-card border border-white/5 rounded-xl p-6 hover:border-white/10 transition-colors"
                        >
                          <div className="flex items-start justify-between mb-4">
                            <div>
                              <h4 className="text-xl font-bold text-white mb-2">{project.name}</h4>
                              <p className="text-muted-foreground">{project.description}</p>
                            </div>
                            <a
                              href={project.link}
                              className="h-10 w-10 flex items-center justify-center rounded-full border border-white/10 text-white hover:bg-white hover:text-black transition-all"
                            >
                              <ArrowUpRight className="h-5 w-5" />
                            </a>
                          </div>
                          
                          <p className="text-sm text-white/60 mb-4">{project.details}</p>
                          
                          <div className="flex flex-wrap gap-2">
                            {project.tech.map((tech: string) => (
                              <span
                                key={tech}
                                className="px-3 py-1 bg-white/5 rounded-full text-xs font-mono text-white/80"
                              >
                                {tech}
                              </span>
                            ))}
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
