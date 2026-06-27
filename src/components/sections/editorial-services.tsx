"use client";
import { motion } from "framer-motion";

export const EditorialServices = ({ services }: { services: any[] }) => {
  return (
    <section className="bg-background py-40 px-6">
      <div className="mx-auto max-w-7xl">
        <div className="mb-32">
          <span className="text-xs font-bold tracking-[0.2em] text-muted-foreground uppercase">
            Capacidades
          </span>
          <h2 className="mt-6 text-5xl font-bold tracking-tighter text-white sm:text-7xl">
            CÓMO CONSTRUYO.
          </h2>
        </div>

        <div className="grid grid-cols-1 gap-x-8 gap-y-16 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((service, index) => (
            <motion.div
              key={service.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: index * 0.1 }}
              className="flex flex-col border-t border-white/10 pt-8"
            >
              <span className="mb-4 text-sm font-mono text-muted-foreground">
                0{index + 1}
              </span>
              <h3 className="text-2xl font-bold text-white mb-4">
                {service.title}
              </h3>
              <p className="text-lg leading-relaxed text-muted-foreground">
                {service.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};
