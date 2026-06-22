import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import posts from "@/data/posts.json";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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

  return (
    <div className="min-h-screen bg-background px-6 py-20">
      <div className="mx-auto max-w-6xl">
        <Link href="/blog" className="group flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase mb-12">
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Volver al blog
        </Link>
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Tabla de contenido */}
          <aside className="lg:col-span-1">
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

          {/* Contenido principal */}
          <article className="lg:col-span-3 bg-card border border-white/5 rounded-2xl p-8 md:p-12">
            <div className="flex items-start justify-between mb-6">
              <span className="px-3 py-1 bg-blue-500/10 text-blue-500 rounded-full text-xs font-bold uppercase tracking-wider">
                {post.category}
              </span>
              <span className="text-white/40 text-sm">{new Date(post.createdAt).toLocaleDateString()}</span>
            </div>
            
            <h1 className="text-4xl md:text-5xl font-bold tracking-tighter text-white mb-6">
              {post.title}
            </h1>
            
            <p className="text-xl text-muted-foreground mb-12 leading-relaxed">
              {post.description}
            </p>

            <div className="border-t border-white/10 pt-8">
              <div className="prose prose-invert prose-lg max-w-none prose-headings:text-white prose-headings:font-bold prose-h1:text-4xl prose-h1:mb-6 prose-h1:mt-8 prose-h1:font-extrabold prose-h2:text-3xl prose-h2:mb-4 prose-h2:mt-6 prose-h2:font-bold prose-h3:text-2xl prose-h3:mb-3 prose-h3:mt-4 prose-h3:font-semibold prose-h4:text-xl prose-h4:mb-2 prose-h4:mt-3 prose-h4:font-semibold prose-h5:text-lg prose-h5:mb-2 prose-h5:mt-2 prose-h5:font-medium prose-h6:text-base prose-h6:mb-2 prose-h6:mt-2 prose-h6:font-medium prose-p:text-white/90 prose-p:leading-relaxed prose-p:mb-4 prose-p:text-base prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline prose-a:font-medium prose-strong:text-white prose-strong:font-bold prose-em:text-white/80 prose-em:italic prose-code:text-blue-400 prose-code:bg-white/5 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:font-mono prose-pre:bg-white/5 prose-pre:border prose-pre:border-white/10 prose-pre:rounded-lg prose-pre:p-4 prose-pre:overflow-x-auto prose-pre:text-sm prose-pre:text-white/90 prose-ul:list-disc prose-ul:pl-6 prose-ul:mb-4 prose-ul:text-white/90 prose-ul:space-y-2 prose-li:mb-1 prose-li:text-white/90 prose-ol:list-decimal prose-ol:pl-6 prose-ol:mb-4 prose-ol:text-white/90 prose-ol:space-y-2 prose-blockquote:border-l-4 prose-blockquote:border-white/20 prose-blockquote:pl-4 prose-blockquote:italic prose-blockquote:text-white/70 prose-blockquote:my-4 prose-hr:border-white/10 prose-hr:my-8 prose-table:text-white/90 prose-table:border prose-table:border-white/10 prose-thead:border-b prose-thead:border-white/10 prose-th:text-white prose-th:font-semibold prose-th:p-3 prose-th:bg-white/5 prose-tr:border-b prose-tr:border-white/10 prose-td:p-3 prose-td:text-white/90 prose-img:rounded-lg prose-img:my-4">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {post.content}
                </ReactMarkdown>
              </div>
            </div>
          </article>
        </div>

        <div className="mt-12 flex items-center justify-between">
          <Link href="/blog" className="text-blue-400 font-medium hover:text-blue-300 transition-colors">
            ← Volver a todos los artículos
          </Link>
        </div>
      </div>
    </div>
  );
}
