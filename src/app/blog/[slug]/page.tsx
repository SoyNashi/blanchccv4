import Link from "next/link";
import posts from "@/data/posts.json";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import BlogNavbar from "@/components/blog-navbar";
import BlogFooter from "@/components/blog-footer";

// Función para extraer headings del markdown
function extractHeadings(markdown: string) {
  const headingRegex = /^(#{1,3})\s+(.+)$/gm;
  const headings: { level: number; text: string; id: string }[] = [];
  let match;

  while ((match = headingRegex.exec(markdown)) !== null) {
    const level = match[1].length;
    const text = match[2].trim();
    const id = text
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-');
    headings.push({ level, text, id });
  }

  return headings;
}

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { slug } = await params;
  const post = posts.find(p => p.slug === slug);
  
  if (!post) {
    return {
      title: "Post no encontrado",
    };
  }

  return {
    title: `${post.title} | Nil Blanch`,
    description: post.description,
    openGraph: {
      title: post.title,
      description: post.description,
      type: "article",
      publishedTime: post.createdAt,
    },
  };
}

export default async function BlogPostPage({ params }: PageProps) {
  const { slug } = await params;
  const post = posts.find(p => p.slug === slug);

  if (!post) {
    notFound();
  }

  // Extraer headings para la tabla de contenido
  const headings = extractHeadings(post.content);

  // Obtener posts de la misma serie
  const seriesPosts = post.series 
    ? posts.filter(p => p.series === post.series && p.published).sort((a, b) => (a.seriesOrder || 0) - (b.seriesOrder || 0))
    : [];

  const currentSeriesIndex = seriesPosts.findIndex(p => p.slug === post.slug);
  const prevPost = currentSeriesIndex > 0 ? seriesPosts[currentSeriesIndex - 1] : null;
  const nextPost = currentSeriesIndex < seriesPosts.length - 1 ? seriesPosts[currentSeriesIndex + 1] : null;

  return (
    <div className="min-h-screen bg-background">
      <BlogNavbar />
      <div className="px-4 py-12 md:px-6 md:py-20">
        <div className="mx-auto max-w-6xl">
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
          {/* Sidebar izquierdo - Tabla de contenido (oculto en móvil) */}
          <aside className="hidden xl:block xl:col-span-1">
            <div className="bg-card border border-white/5 rounded-2xl p-6 sticky top-8">
              <h3 className="text-sm font-bold tracking-widest text-white uppercase mb-4">
                Contenido
              </h3>
              {headings.length > 0 && (
                <nav className="space-y-2">
                  {headings.map((heading, index) => (
                    <a
                      key={index}
                      href={`#${heading.id}`}
                      className={`block text-sm hover:text-white transition-colors ${
                        heading.level === 1 
                          ? 'text-white font-bold' 
                          : heading.level === 2 
                            ? 'text-white/80 font-medium ml-2' 
                            : 'text-white/60 ml-4'
                      }`}
                    >
                      {heading.text}
                    </a>
                  ))}
                </nav>
              )}
            </div>
          </aside>

          {/* Contenido principal - más ancho */}
          <article className="xl:col-span-2 lg:col-span-3">
            <div className="bg-card border border-white/5 rounded-2xl p-6 md:p-8 lg:p-12">
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">
                <div className="flex items-center gap-3">
                  <span className="px-3 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                    {post.category}
                  </span>
                  {post.featured && <svg className="h-4 w-4 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                  </svg>}
                  {post.series && <span className="text-xs text-white/40">{post.series}</span>}
                </div>
                <span className="text-white/40 text-sm">{new Date(post.createdAt).toLocaleDateString()}</span>
              </div>
              
              <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tighter text-white mb-6">
                {post.title}
              </h1>
              
              <p className="text-lg md:text-xl text-muted-foreground mb-12 leading-relaxed">
                {post.description}
              </p>

              <div className="border-t border-white/10 pt-8">
                <div className="prose prose-invert prose-lg max-w-none prose-headings:text-white prose-headings:font-bold prose-h1:text-4xl prose-h1:mb-6 prose-h1:mt-8 prose-h1:font-extrabold prose-h2:text-3xl prose-h2:mb-4 prose-h2:mt-6 prose-h2:font-bold prose-h3:text-2xl prose-h3:mb-3 prose-h3:mt-4 prose-h3:font-semibold prose-h4:text-xl prose-h4:mb-2 prose-h4:mt-3 prose-h4:font-semibold prose-h5:text-lg prose-h5:mb-2 prose-h5:mt-2 prose-h5:font-medium prose-h6:text-base prose-h6:mb-2 prose-h6:mt-2 prose-h6:font-medium prose-p:text-white/90 prose-p:leading-relaxed prose-p:mb-4 prose-p:text-base prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline prose-a:font-medium prose-strong:text-white prose-strong:font-bold prose-em:text-white/80 prose-em:italic prose-code:text-blue-400 prose-code:bg-white/5 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:font-mono prose-pre:bg-white/5 prose-pre:border prose-pre:border-white/10 prose-pre:rounded-lg prose-pre:p-4 prose-pre:overflow-x-auto prose-pre:text-sm prose-pre:text-white/90 prose-ul:list-disc prose-ul:pl-6 prose-ul:mb-4 prose-ul:text-white/90 prose-ul:space-y-2 prose-li:mb-1 prose-li:text-white/90 prose-ol:list-decimal prose-ol:pl-6 prose-ol:mb-4 prose-ol:text-white/90 prose-ol:space-y-2 prose-blockquote:border-l-4 prose-blockquote:border-white/20 prose-blockquote:pl-4 prose-blockquote:italic prose-blockquote:text-white/70 prose-blockquote:my-4 prose-hr:border-white/10 prose-hr:my-8 prose-table:text-white/90 prose-table:border prose-table:border-white/10 prose-thead:border-b prose-thead:border-white/10 prose-th:text-white prose-th:font-semibold prose-th:p-3 prose-th:bg-white/5 prose-tr:border-b prose-tr:border-white/10 prose-td:p-3 prose-td:text-white/90 prose-img:rounded-lg prose-img:my-4">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {post.content}
                  </ReactMarkdown>
                </div>
              </div>
            </div>

            {/* Navegación de serie */}
            {seriesPosts.length > 1 && (
              <div className="mt-8 bg-card border border-white/5 rounded-2xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold tracking-widest text-white uppercase">
                    {post.series}
                  </h3>
                  <span className="text-xs text-white/40">
                    Parte {currentSeriesIndex + 1} de {seriesPosts.length}
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  {prevPost ? (
                    <Link href={`/blog/${prevPost.slug}`} className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors">
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
                      </svg>
                      <div className="text-left">
                        <div className="text-xs text-white/40">Anterior</div>
                        <div className="text-sm font-medium">{prevPost.seriesPartTitle || `Parte ${prevPost.seriesOrder}`}</div>
                      </div>
                    </Link>
                  ) : (
                    <div />
                  )}
                  
                  <div className="flex gap-2">
                    {seriesPosts.map((p, idx) => (
                      <Link
                        key={p.slug}
                        href={`/blog/${p.slug}`}
                        className={`w-8 h-8 rounded-full flex items-center justify-center text-xs transition-colors ${
                          p.slug === post.slug
                            ? 'bg-blue-500 text-white'
                            : 'bg-white/5 text-white/60 hover:bg-white/10'
                        }`}
                      >
                        {idx + 1}
                      </Link>
                    ))}
                  </div>
                  
                  {nextPost ? (
                    <Link href={`/blog/${nextPost.slug}`} className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors">
                      <div className="text-right">
                        <div className="text-xs text-white/40">Siguiente</div>
                        <div className="text-sm font-medium">{nextPost.seriesPartTitle || `Parte ${nextPost.seriesOrder}`}</div>
                      </div>
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </Link>
                  ) : (
                    <div />
                  )}
                </div>
              </div>
            )}
          </article>

          {/* Sidebar derecho - Info del post (oculto en móvil) */}
          <aside className="hidden xl:block xl:col-span-1 space-y-6">
            {/* Info del post */}
            <div className="bg-card border border-white/5 rounded-2xl p-6">
              <h3 className="text-sm font-bold tracking-widest text-white uppercase mb-4">
                Información
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex items-center gap-2 text-white/60">
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{post.readingTime} min de lectura</span>
                </div>
                <div className="flex items-center gap-2 text-white/60">
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span>{post.wordCount} palabras</span>
                </div>
                <div className="flex items-center gap-2 text-white/60">
                  <span className="text-xs">{new Date(post.createdAt).toLocaleDateString()}</span>
                </div>
              </div>

              {post.featured && (
                <div className="mt-4 pt-4 border-t border-white/10">
                  <div className="flex items-center gap-2 text-yellow-500">
                    <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                    </svg>
                    <span className="text-sm font-medium">Artículo destacado</span>
                  </div>
                </div>
              )}
            </div>

            {/* Keywords */}
            {post.keywords.length > 0 && (
              <div className="bg-card border border-white/5 rounded-2xl p-6">
                <h3 className="text-sm font-bold tracking-widest text-white uppercase mb-4">
                  Keywords
                </h3>
                <div className="flex flex-wrap gap-2">
                  {post.keywords.map(kw => (
                    <span key={kw} className="px-2 py-1 bg-white/5 rounded text-xs text-white/60">
                      #{kw}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </aside>
        </div>

        <div className="mt-12 flex items-center justify-between">
          <Link href="/blog" className="text-blue-400 font-medium hover:text-blue-300 transition-colors">
            ← Volver a todos los artículos
          </Link>
        </div>
      </div>
      </div>
      <BlogFooter />
    </div>
  );
}
