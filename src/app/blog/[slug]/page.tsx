import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import posts from "@/data/posts.json";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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

  return (
    <div className="min-h-screen bg-background px-6 py-20">
      <div className="mx-auto max-w-4xl">
        <Link href="/blog" className="group flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase mb-12">
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Volver al blog
        </Link>
        
        <article className="bg-card border border-white/5 rounded-2xl p-8 md:p-12">
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
            <div className="prose prose-invert prose-lg max-w-none prose-headings:text-white prose-h1:text-3xl prose-h2:text-2xl prose-h3:text-xl prose-p:text-white/90 prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline prose-strong:text-white prose-code:text-blue-400 prose-pre:bg-white/5 prose-pre:border prose-pre:border-white/10">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {post.content}
              </ReactMarkdown>
            </div>
          </div>
        </article>

        <div className="mt-12 flex items-center justify-between">
          <Link href="/blog" className="text-blue-400 font-medium hover:text-blue-300 transition-colors">
            ← Volver a todos los artículos
          </Link>
        </div>
      </div>
    </div>
  );
}
