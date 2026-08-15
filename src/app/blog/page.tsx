"use client";

import Link from "next/link";
import posts from "@/data/posts.json";
import BlogNavbar from "@/components/blog-navbar";
import BlogFooter from "@/components/blog-footer";
import { useState, useMemo } from "react";

type PostCategory = 'novedad' | 'alerta' | 'descubrimiento' | 'creacion' | 'seguridad' | 'malware';

export default function BlogPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [showIndex, setShowIndex] = useState(false);

  // Obtener categorías únicas
  const categories = Array.from(new Set(posts.map(post => post.category as PostCategory))).filter(Boolean);

  // Obtener keywords únicas
  const keywords = Array.from(new Set<string>(posts.flatMap(post => post.keywords))).sort();

  // Posts destacados
  const featuredPosts = posts.filter(post => post.featured && post.published).slice(0, 3);

  // Series
  const seriesMap = new Map<string, typeof posts>();
  posts.forEach(post => {
    if (post.series && post.published) {
      if (!seriesMap.has(post.series)) {
        seriesMap.set(post.series, []);
      }
      seriesMap.get(post.series)!.push(post);
    }
  });
  
  // Ordenar posts dentro de cada serie
  seriesMap.forEach((seriesPosts) => {
    seriesPosts.sort((a, b) => (a.seriesOrder || 0) - (b.seriesOrder || 0));
  });

  // Filtrar posts
  const filteredPosts = useMemo(() => {
    return posts.filter(post => {
      if (!post.published) return false;
      
      const matchesSearch = searchQuery === "" || 
        post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.keywords.some(kw => kw.toLowerCase().includes(searchQuery.toLowerCase()));
      
      const matchesCategory = selectedCategory === "all" || post.category === selectedCategory;
      
      return matchesSearch && matchesCategory;
    });
  }, [searchQuery, selectedCategory]);

  return (
    <div className="min-h-screen bg-background">
      <BlogNavbar />
      <div className="px-4 py-12 md:px-6 md:py-20">
        <div className="mx-auto max-w-6xl">
          {/* Header */}
          <div className="mb-8">
            <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
              <div>
                <h1 className="text-5xl md:text-6xl font-bold tracking-tighter text-white mb-4">Insights</h1>
                <p className="text-lg md:text-xl text-muted-foreground max-w-2xl">
                  Artículos sobre desarrollo web, seguridad, arquitectura de sistemas y tecnología.
                </p>
              </div>
              
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <span className="flex items-center gap-2">
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  {posts.filter(p => p.published).length} artículos
                </span>
                <span className="flex items-center gap-2">
                  <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  {featuredPosts.length} destacados
                </span>
                <button
                  onClick={() => setShowIndex(!showIndex)}
                  className="flex items-center gap-2 px-3 py-1 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
                >
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h7" />
                  </svg>
                  Índice
                </button>
              </div>
            </div>

            {/* Filtros */}
            <div className="mt-6 flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Buscar artículos..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500 transition-colors"
                />
              </div>
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => setSelectedCategory("all")}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedCategory === "all" 
                      ? "bg-blue-500 text-white" 
                      : "bg-white/5 text-white/70 hover:bg-white/10"
                  }`}
                >
                  Todos
                </button>
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      selectedCategory === category 
                        ? "bg-blue-500 text-white" 
                        : "bg-white/5 text-white/70 hover:bg-white/10"
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Índice */}
          {showIndex && (
            <div className="mb-8 p-4 bg-white/5 border border-white/10 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-3">Índice de artículos</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                {filteredPosts.map((post) => (
                  <a
                    key={post.id}
                    href={`#post-${post.id}`}
                    className="text-sm text-white/70 hover:text-blue-400 transition-colors py-1"
                  >
                    {post.title}
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Posts Destacados */}
          {featuredPosts.length > 0 && (
            <div className="mb-12">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-3">
                <svg className="h-5 w-5 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                Destacados
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {featuredPosts.map((post) => (
                  <Link key={post.id} href={`/blog/${post.slug}`} className="group block bg-card border border-white/5 rounded-xl p-4 hover:border-white/20 transition-all">
                    <div className="flex items-center justify-between mb-3">
                      <span className="px-2 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                        {post.category}
                      </span>
                      <svg className="h-3 w-3 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                      </svg>
                    </div>
                    
                    <h3 className="text-base font-bold text-white mb-2 group-hover:text-blue-400 transition-colors line-clamp-2">
                      {post.title}
                    </h3>
                    
                    <p className="text-muted-foreground text-xs mb-3 line-clamp-2">
                      {post.description}
                    </p>
                    
                    <div className="flex items-center gap-3 text-xs text-white/40">
                      <span className="flex items-center gap-1">
                        <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {post.readingTime} min
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* Series */}
          {seriesMap.size > 0 && (
            <div className="mb-16">
              <h2 className="text-2xl font-bold text-white mb-6">Series</h2>
              <div className="space-y-6">
                {Array.from(seriesMap.entries()).map(([seriesName, seriesPosts]) => (
                  <div key={seriesName} className="bg-card border border-white/5 rounded-2xl p-6">
                    <h3 className="text-xl font-bold text-white mb-4">{seriesName}</h3>
                    <div className="flex flex-wrap gap-3">
                      {seriesPosts.map((post) => (
                        <Link key={post.id} href={`/blog/${post.slug}`} className="px-4 py-2 bg-white/5 rounded-lg text-sm text-white hover:bg-white/10 transition-colors">
                          {post.seriesPartTitle || `Parte ${post.seriesOrder}`}
                        </Link>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Lista de Posts */}
          <div>
            <h2 className="text-xl font-bold text-white mb-4">
              Todos los artículos
              <span className="text-muted-foreground ml-2">({filteredPosts.length})</span>
            </h2>

            {filteredPosts.length === 0 ? (
              <div className="text-center py-12 text-white/40">
                <p>No se encontraron artículos que coincidan con tu búsqueda.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredPosts.map((post) => (
                  <Link 
                    key={post.id} 
                    href={`/blog/${post.slug}`} 
                    id={`post-${post.id}`}
                    className="group block bg-card border border-white/5 rounded-xl p-4 hover:border-white/20 transition-all"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                          {post.category}
                        </span>
                        {post.featured && <svg className="h-3 w-3 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-white/40">
                        <span className="flex items-center gap-1">
                          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          {post.readingTime} min
                        </span>
                      </div>
                    </div>
                    
                    <h3 className="text-base font-bold text-white mb-2 group-hover:text-blue-400 transition-colors line-clamp-2">
                      {post.title}
                    </h3>
                    
                    <p className="text-muted-foreground text-xs mb-3 line-clamp-2">
                      {post.description}
                    </p>
                    
                    <div className="flex flex-wrap gap-1 mb-3">
                      {post.keywords.slice(0, 3).map(kw => (
                        <span key={kw} className="px-2 py-0.5 bg-white/5 rounded text-xs text-white/60">
                          #{kw}
                        </span>
                      ))}
                      {post.keywords.length > 3 && (
                        <span className="px-2 py-0.5 bg-white/5 rounded text-xs text-white/40">
                          +{post.keywords.length - 3}
                        </span>
                      )}
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-blue-400 font-medium group-hover:text-blue-300 transition-colors">
                        Leer →
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
      
      <BlogFooter />
    </div>
  );
}
