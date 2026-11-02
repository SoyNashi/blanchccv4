"use client";

import { motion } from "framer-motion";
import { Activity, Code2, Fingerprint, Network, Server, ShieldCheck } from "lucide-react";

const icons = [Code2, Network, ShieldCheck, Server, Fingerprint, Activity];

export const EditorialServices = ({ services }: { services: any[] }) => (
  <section id="about-focus" className="border-y border-white/[0.07] bg-[#0a0f13]/75 px-5 py-24 sm:px-8 lg:px-12 lg:py-32">
    <div className="mx-auto max-w-7xl">
      <div className="mb-14 grid gap-7 md:grid-cols-[1fr_.7fr] md:items-end">
        <div><p className="section-kicker mb-4">02 / Areas of interest</p><h2 className="text-5xl font-black tracking-[-.06em] text-white sm:text-7xl">BEYOND THE<br /><span className="neon-text">INTERFACE.</span></h2></div>
        <p className="max-w-lg text-sm leading-7 text-[#9baab0]">Una web es solo la superficie. Me interesa entender y construir también lo que hay debajo: cómo se comunican los sistemas, cómo se protegen los datos y cómo se mantiene una infraestructura fiable. Estas son mis áreas de trabajo y exploración, no una lista de certificaciones o promesas de auditoría.</p>
      </div>
      <div className="grid gap-px overflow-hidden rounded-xl border border-white/10 bg-white/10 sm:grid-cols-2 lg:grid-cols-3">
        {services.map((service, index) => {
          const Icon = icons[index] || Activity;
          return <motion.div key={service.id} initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: index * .06 }}
            className="group min-h-56 bg-[#0b1116] p-7 transition-colors hover:bg-[#111b20] sm:p-8">
            <div className="mb-9 flex items-center justify-between"><span className="font-mono text-[10px] tracking-[.2em] text-white/35">0{index + 1} / FIELD</span><Icon className="h-5 w-5 text-[#b7ff3c] transition-transform group-hover:scale-110" /></div>
            <h3 className="mb-3 text-xl font-bold text-white">{service.title}</h3><p className="text-sm leading-7 text-[#91a0a8]">{service.description}</p>
          </motion.div>;
        })}
      </div>
    </div>
  </section>
);
