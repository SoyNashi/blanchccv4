import { db } from "@/lib/db";
import { postsMeta } from "@/db/schema";
import { eq } from "drizzle-orm";
import { notFound } from "next/navigation";
import { remark } from "remark";
import html from "remark-html";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default async function PostDetailPage({ params }: { params: { slug: string } }) {
  const post = await db.query.postsMeta.findFirst({
    where: eq(postsMeta.slug, params.slug),
  });

  if (!post) notFound();

  // Procesar Markdown a HTML
  const processedContent = await remark()
    .use(html)
    .process(post.content || "");
  const contentHtml = processedContent.toString();

  return (
    <article className="min-h-screen bg-background px-6 py-20">
      <div className="mx-auto max-w-3xl">
        <Link href="/blog" className="group flex items-center gap-2 text-sm font-bold text-muted-foreground uppercase mb-12">
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Volver al blog
        </Link>

        <header className="mb-16">
          <span className="text-xs font-bold tracking-widest text-blue-500 uppercase">
            {post.category}
          </span>
          <h1 className="mt-6 text-5xl font-bold tracking-tighter text-white sm:text-7xl">
            {post.title}
          </h1>
          <p className="mt-8 text-xl text-muted-foreground leading-relaxed">
            {post.description}
          </p>
        </header>

        <div 
          className="prose prose-invert prose-pre:bg-card max-w-none"
          dangerouslySetInnerHTML={{ __html: contentHtml }} 
        />
      </div>
    </article>
  );
}