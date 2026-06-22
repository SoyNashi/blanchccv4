"use client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const MESSAGES = [
  "CONSTRUYO PRODUCTOS REALES.",
  "SOLUCIONES DIGITALES PREMIUM.",
  "DISEÑO QUE IMPACTA.",
  "DESARROLLO QUE ESCALA.",
];

export const Hero = () => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % MESSAGES.length);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  return (
    <section id="hero" className="relative flex h-screen w-full flex-col items-center justify-center overflow-hidden bg-background px-6">
      <div className="z-10 w-full max-w-7xl">
        <AnimatePresence mode="wait">
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="flex flex-col items-start justify-center"
          >
            <h1 className="text-huge font-bold tracking-tighter text-white">
              {MESSAGES[index]}
            </h1>
          </motion.div>
        </AnimatePresence>
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 1 }}
          className="mt-12 flex items-center gap-4"
        >
          <div className="h-px w-12 bg-white/20" />
          <p className="text-sm font-medium tracking-widest text-muted-foreground uppercase">
            Nil Blanch — Digital Product Builder
          </p>
        </motion.div>
      </div>

      {/* SVG Logo con efecto flotante */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
        animate={{ opacity: 0.15, scale: 1, rotate: 0 }}
        transition={{ duration: 1.5, ease: [0.16, 1, 0.3, 1] }}
        className="absolute inset-0 z-0 flex items-center justify-center pointer-events-none"
      >
        <motion.div
          animate={{
            y: [0, -20, 0],
            rotate: [0, 5, -5, 0],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="w-[600px] h-[600px] opacity-10"
        >
          <img
            src="/path2.svg"
            alt="Logo"
            className="w-full h-full object-contain"
          />
        </motion.div>
      </motion.div>

      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white/[0.03] to-transparent opacity-50" />
    </section>
  );
};
