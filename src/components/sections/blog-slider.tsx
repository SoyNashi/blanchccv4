"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

const CATEGORY_STYLES: Record<string, string> = {
  novedad: "bg-blue-500/10 text-blue-500 border-blue-500/20",
  alerta: "bg-red-500/10 text-red-500 border-red-500/20",
  descubrimiento: "bg-purple-500/10 text-purple-500 border-purple-500/20",
  creacion: "bg-green-500/10 text-green-500 border-green-500/20",
  seguridad: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
  malware: "bg-orange-500/10 text-orange-500 border-orange-500/20",
};

export const BlogSlider = ({ posts }: { posts: any[] }) => {
  return (
    <section id="blog" className="bg-background py-40 px-6">
      <div className="mx-auto max-w-7xl">
        <div className="flex items-end justify-between mb-20">
          <div>
            <span className="text-xs font-bold tracking-[0.2em] text-muted-foreground uppercase">
              Bitácora
            </span>
            <h2 className="mt-6 text-5xl font-bold tracking-tighter text-white sm:text-7xl">
              BLOG.
            </h2>
          </div>
          <Link 
            href="/blog" 
            className="group flex items-center gap-2 text-sm font-bold tracking-widest text-white uppercase"
          >
            Ver todo <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {posts.map((post, i) => (
            <Link key={post.slug} href={`/blog/${post.slug}`} className="group">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="flex flex-col h-full p-8 bg-card border border-white/5 rounded-3xl hover:border-white/20 transition-all"
              >
                <span className={`w-fit px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ${CATEGORY_STYLES[post.category]}`}>
                  {post.category}
                </span>
                <h3 className="mt-6 text-2xl font-bold text-white group-hover:text-white/90 transition-colors">
                  {post.title}
                </h3>
                <p className="mt-4 text-muted-foreground line-clamp-2">
                  {post.description}
                </p>
                <div className="mt-auto pt-8 flex items-center justify-between">
                  <span className="text-xs font-mono text-white/40">Leer más</span>
                  <div className="h-8 w-8 rounded-full bg-white/5 flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity">
                    <ArrowRight className="h-4 w-4" />
                  </div>
                </div>
              </motion.div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
};
