import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import posts from "@/data/posts.json";
import { notFound } from "next/navigation";

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
    <div className="min-h-screen bg-black px-4 py-8 font-mono">
      <div className="mx-auto max-w-5xl">
        <Link href="/blog" className="group flex items-center gap-2 text-sm text-green-400 mb-8 hover:text-green-300">
          <ArrowLeft className="h-4 w-4" /> ../bitacora
        </Link>
        
        <div className="mb-8">
          <span className="text-green-400">$</span>
          <span className="text-white ml-2">cat {post.slug}.md</span>
        </div>

        <div className="bg-gray-900 border border-green-500/30 rounded-lg p-6 mb-8">
          <div className="text-gray-500 mb-4">
            <span className="text-green-400">#</span> {post.title}
          </div>
          
          <div className="flex gap-4 mb-6 text-sm">
            <span className="text-blue-400 uppercase">{post.category}</span>
            <span className="text-yellow-400">{post.likes} likes</span>
            <span className="text-gray-400">{new Date(post.createdAt).toLocaleDateString()}</span>
          </div>

          <div className="border-t border-green-500/20 pt-6">
            <div className="text-gray-500 mb-2">
              <span className="text-green-400">##</span> Descripción
            </div>
            <p className="text-gray-300 leading-relaxed">{post.description}</p>
          </div>

          <div className="border-t border-green-500/20 pt-6 mt-6">
            <div className="text-gray-500 mb-2">
              <span className="text-green-400">##</span> Contenido
            </div>
            <p className="text-gray-300 leading-relaxed">{post.content}</p>
          </div>
        </div>

        <div className="mb-8">
          <span className="text-green-400">$</span>
          <span className="text-white ml-2">git log --oneline -1</span>
        </div>

        <div className="bg-gray-900 border border-green-500/30 rounded-lg p-4 text-gray-400 text-sm">
          <span className="text-yellow-400">commit</span> {post.slug.slice(0, 7)} (HEAD -&gt; main)
          <br />
          <span className="text-blue-400">Author:</span> Nil Blanch &lt;hola@blanch.cc&gt;
          <br />
          <span className="text-purple-400">Date:</span> {new Date(post.createdAt).toLocaleString()}
          <br />
          <span className="text-green-400">    </span> {post.title}
        </div>
      </div>
    </div>
  );
}
