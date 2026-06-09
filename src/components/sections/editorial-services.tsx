"use client";
import { motion } from "framer-motion";

const SERVICES = [
  {
    id: "web",
    title: "Desarrollo Web",
    description: "Aplicaciones web de alto rendimiento construidas con las tecnologías más modernas para garantizar velocidad, escalabilidad y una experiencia de usuario excepcional.",
  },
  {
    id: "ecommerce",
    title: "Ecommerce",
    description: "Soluciones de comercio electrónico robustas y personalizadas, enfocadas en la conversión y la optimización de la experiencia de compra.",
  },
  {
    id: "seo",
    title: "SEO Técnico",
    description: "Optimización profunda desde el código para asegurar que tu producto no solo sea excelente, sino también visible para quienes lo buscan.",
  },
  {
    id: "hosting",
    title: "Hosting & Ops",
    description: "Infraestructura gestionada y despliegue continuo para que tu producto esté siempre disponible y funcione a la perfección.",
  },
  {
    id: "maintenance",
    title: "Mantenimiento",
    description: "Cuidado constante y evolución de tus sistemas para prevenir problemas antes de que ocurran y mantenerte a la vanguardia.",
  },
  {
    id: "consulting",
    title: "Consultoría",
    description: "Asesoramiento estratégico para definir la arquitectura técnica y el roadmap de tu próximo gran producto digital.",
  },
];

export const EditorialServices = () => {
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

        <div className="grid grid-cols-1 gap-x-12 gap-y-24 md:grid-cols-2 lg:grid-cols-3">
          {SERVICES.map((service, index) => (
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
