import { ArrowLeft, Search, ArrowRight } from "lucide-react";
import Link from "next/link";
import { db } from "@/lib/db";
import { postsMeta } from "@/db/schema";
import { desc } from "drizzle-orm";

export default async function BlogPage() {
  const posts = db ? await db.select().from(postsMeta).orderBy(desc(postsMeta.createdAt)) : [];

  return (
    <div className="min-h-screen bg-background px-6 py-20">
      <div className="mx-auto max-w-4xl">
        <Link href="/" className="group flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase mb-12">
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Volver
        </Link>
        
        <h1 className="text-6xl font-bold tracking-tighter text-white mb-12">Bitácora Técnica</h1>
        
        <div className="relative mb-20">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          <input 
            type="text" 
            placeholder="Buscar en el archivo..." 
            className="w-full bg-card border border-white/5 rounded-2xl py-4 pl-12 pr-6 text-white focus:outline-none focus:border-white/20 transition-colors"
          />
        </div>

        <div className="flex flex-col gap-12">
          {posts.map((post) => (
            <Link key={post.id} href={`/blog/${post.slug}`} className="group border-b border-white/5 pb-12">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-[10px] font-bold text-blue-500 uppercase tracking-widest">{post.category}</span>
                  <h3 className="mt-4 text-3xl font-bold text-white group-hover:text-blue-400 transition-colors">{post.title}</h3>
                  <p className="mt-4 text-muted-foreground line-clamp-2 max-w-2xl">{post.description}</p>
                </div>
                <ArrowRight className="h-6 w-6 text-white/20 group-hover:text-white transition-colors" />
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
