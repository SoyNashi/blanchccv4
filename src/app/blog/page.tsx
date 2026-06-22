"use client";
import { ArrowLeft, Search, Clock, FileText, Star, Filter } from "lucide-react";
import Link from "next/link";
import posts from "@/data/posts.json";
import { useState, useMemo } from "react";
import BlogNavbar from "@/components/blog-navbar";

type PostCategory = 'novedad' | 'alerta' | 'descubrimiento' | 'creacion' | 'seguridad' | 'malware';

export default function BlogPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<PostCategory | 'all'>('all');
  const [selectedKeyword, setSelectedKeyword] = useState<string | 'all'>('all');
  const [showFilters, setShowFilters] = useState(false);

  // Obtener categorías únicas
  const categories = useMemo(() => {
    const cats = new Set<PostCategory>();
    posts.forEach(post => cats.add(post.category));
    return Array.from(cats);
  }, []);

  // Obtener keywords únicas
  const keywords = useMemo(() => {
    const kw = new Set<string>();
    posts.forEach(post => post.keywords.forEach(k => kw.add(k)));
    return Array.from(kw).sort();
  }, []);

  // Filtrar y ordenar posts
  const filteredPosts = useMemo(() => {
    let filtered = posts.filter(post => post.published);

    // Filtrar por categoría
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(post => post.category === selectedCategory);
    }

    // Filtrar por keyword
    if (selectedKeyword !== 'all') {
      filtered = filtered.filter(post => post.keywords.includes(selectedKeyword));
    }

    // Filtrar por búsqueda
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(post => 
        post.title.toLowerCase().includes(term) ||
        post.description.toLowerCase().includes(term) ||
        post.keywords.some(k => k.toLowerCase().includes(term))
      );
    }

    // Ordenar: destacados primero, luego por fecha
    return filtered.sort((a, b) => {
      if (a.featured && !b.featured) return -1;
      if (!a.featured && b.featured) return 1;
      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    });
  }, [searchTerm, selectedCategory, selectedKeyword]);

  // Posts destacados
  const featuredPosts = useMemo(() => {
    return posts.filter(post => post.featured && post.published).slice(0, 3);
  }, []);

  // Series
  const series = useMemo(() => {
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
    
    return seriesMap;
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <BlogNavbar />
      <div className="px-4 py-12 md:px-6 md:py-20">
        <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-12">
          <Link href="/" className="group inline-flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase mb-8">
            <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Volver
          </Link>
          
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
            <div>
              <h1 className="text-5xl md:text-6xl font-bold tracking-tighter text-white mb-4">Bitácora Técnica</h1>
              <p className="text-lg md:text-xl text-muted-foreground max-w-2xl">
                Artículos sobre desarrollo web, seguridad, arquitectura de sistemas y tecnología.
              </p>
            </div>
            
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-2">
                <FileText className="h-4 w-4" />
                {posts.filter(p => p.published).length} artículos
              </span>
              <span className="flex items-center gap-2">
                <Star className="h-4 w-4" />
                {featuredPosts.length} destacados
              </span>
            </div>
          </div>
        </div>

        {/* Búsqueda y Filtros */}
        <div className="mb-12">
          <div className="relative mb-6">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Buscar por título, descripción o keywords..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-card border border-white/5 rounded-2xl py-4 pl-12 pr-6 text-white placeholder:text-white/30 focus:outline-none focus:border-white/20 transition-colors"
            />
          </div>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase mb-4 hover:text-white transition-colors"
          >
            <Filter className="h-4 w-4" />
            {showFilters ? 'Ocultar filtros' : 'Mostrar filtros'}
          </button>

          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-6 bg-card border border-white/5 rounded-2xl">
              <div>
                <label className="block text-xs font-bold tracking-widest text-muted-foreground uppercase mb-3">
                  Categoría
                </label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value as PostCategory | 'all')}
                  className="w-full bg-background border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-white/20 transition-colors"
                >
                  <option value="all">Todas las categorías</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold tracking-widest text-muted-foreground uppercase mb-3">
                  Keyword
                </label>
                <select
                  value={selectedKeyword}
                  onChange={(e) => setSelectedKeyword(e.target.value)}
                  className="w-full bg-background border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-white/20 transition-colors"
                >
                  <option value="all">Todas las keywords</option>
                  {keywords.map(kw => (
                    <option key={kw} value={kw}>{kw}</option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Posts Destacados */}
        {featuredPosts.length > 0 && selectedCategory === 'all' && selectedKeyword === 'all' && !searchTerm && (
          <div className="mb-16">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <Star className="h-5 w-5 text-yellow-500" />
              Destacados
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {featuredPosts.map((post) => (
                <Link key={post.id} href={`/blog/${post.slug}`} className="group block bg-card border border-white/5 rounded-2xl p-6 hover:border-white/20 transition-all">
                  <div className="flex items-center justify-between mb-4">
                    <span className="px-3 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                      {post.category}
                    </span>
                    <Star className="h-4 w-4 text-yellow-500" />
                  </div>
                  
                  <h3 className="text-xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors line-clamp-2">
                    {post.title}
                  </h3>
                  
                  <p className="text-muted-foreground text-sm mb-4 line-clamp-2">
                    {post.description}
                  </p>
                  
                  <div className="flex items-center gap-4 text-xs text-white/40">
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {post.readingTime} min
                    </span>
                    <span>{post.wordCount} palabras</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Series */}
        {series.size > 0 && selectedCategory === 'all' && selectedKeyword === 'all' && !searchTerm && (
          <div className="mb-16">
            <h2 className="text-2xl font-bold text-white mb-6">Series</h2>
            <div className="space-y-6">
              {Array.from(series.entries()).map(([seriesName, seriesPosts]) => (
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
          <h2 className="text-2xl font-bold text-white mb-6">
            {selectedCategory === 'all' && selectedKeyword === 'all' && !searchTerm ? 'Todos los artículos' : 'Resultados'}
            <span className="text-muted-foreground ml-2">({filteredPosts.length})</span>
          </h2>

          <div className="space-y-6">
            {filteredPosts.length === 0 ? (
              <div className="text-center py-16 bg-card border border-white/5 rounded-2xl">
                <p className="text-muted-foreground">No se encontraron artículos que coincidan con los filtros.</p>
              </div>
            ) : (
              filteredPosts.map((post) => (
                <Link key={post.id} href={`/blog/${post.slug}`} className="group block bg-card border border-white/5 rounded-2xl p-6 md:p-8 hover:border-white/20 transition-all">
                  <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-4">
                    <div className="flex items-center gap-3">
                      <span className="px-3 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                        {post.category}
                      </span>
                      {post.featured && <Star className="h-4 w-4 text-yellow-500" />}
                      {post.series && <span className="text-xs text-white/40">{post.series}</span>}
                    </div>
                    <div className="flex items-center gap-4 text-xs text-white/40">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {post.readingTime} min
                      </span>
                      <span>{post.wordCount} palabras</span>
                      <span>{new Date(post.createdAt).toLocaleDateString()}</span>
                    </div>
                  </div>
                  
                  <h2 className="text-2xl md:text-3xl font-bold text-white mb-4 group-hover:text-blue-400 transition-colors">
                    {post.title}
                  </h2>
                  
                  <p className="text-muted-foreground mb-6 leading-relaxed">
                    {post.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.keywords.map(kw => (
                      <span key={kw} className="px-2 py-1 bg-white/5 rounded text-xs text-white/60">
                        #{kw}
                      </span>
                    ))}
                  </div>
                  
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
      </div>
    </div>
  );
}
