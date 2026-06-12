"use client";
import { ArrowLeft, Search } from "lucide-react";
import Link from "next/link";
import posts from "@/data/posts.json";
import { useState } from "react";

export default function BlogPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const sortedPosts = posts.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  
  const filteredPosts = sortedPosts.filter(post => 
    post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background px-6 py-20">
      <div className="mx-auto max-w-5xl">
        <Link href="/" className="group flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase mb-12">
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Volver
        </Link>
        
        <h1 className="text-6xl font-bold tracking-tighter text-white mb-4">Bitácora Técnica</h1>
        <p className="text-xl text-muted-foreground mb-12 max-w-2xl">
          Artículos sobre desarrollo web, seguridad, arquitectura de sistemas y tecnología.
        </p>
        
        <div className="relative mb-12">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          <input 
            type="text" 
            placeholder="Buscar artículos..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-card border border-white/5 rounded-2xl py-4 pl-12 pr-6 text-white focus:outline-none focus:border-white/20 transition-colors"
          />
        </div>

        <div className="space-y-8">
          {filteredPosts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">No se encontraron artículos que coincidan con la búsqueda.</p>
            </div>
          ) : (
            filteredPosts.map((post) => (
              <Link key={post.id} href={`/blog/${post.slug}`} className="group block bg-card border border-white/5 rounded-2xl p-8 hover:border-white/20 transition-all">
                <div className="flex items-start justify-between mb-4">
                  <span className="px-3 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                    {post.category}
                  </span>
                  <span className="text-white/40 text-sm">{new Date(post.createdAt).toLocaleDateString()}</span>
                </div>
                
                <h2 className="text-3xl font-bold text-white mb-4 group-hover:text-blue-400 transition-colors">
                  {post.title}
                </h2>
                
                <p className="text-muted-foreground mb-6 leading-relaxed">
                  {post.description}
                </p>
                
                <div className="flex items-center justify-between">
                  <span className="text-blue-400 font-medium group-hover:text-blue-300 transition-colors">
                    Leer artículo →
                  </span>
                </div>
              </Link>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
