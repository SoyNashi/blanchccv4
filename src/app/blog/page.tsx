import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import posts from "@/data/posts.json";

export default async function BlogPage() {
  const sortedPosts = posts.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());

  return (
    <div className="min-h-screen bg-black px-4 py-8 font-mono">
      <div className="mx-auto max-w-5xl">
        <Link href="/" className="group flex items-center gap-2 text-sm text-green-400 mb-8 hover:text-green-300">
          <ArrowLeft className="h-4 w-4" /> ../
        </Link>
        
        <div className="mb-8">
          <span className="text-green-400">$</span>
          <span className="text-white ml-2">cd ~/bitacora</span>
        </div>
        
        <div className="mb-8">
          <span className="text-green-400">$</span>
          <span className="text-white ml-2">ls -la</span>
        </div>

        <div className="bg-gray-900 border border-green-500/30 rounded-lg p-4 mb-8">
          <div className="text-green-400 mb-2">total {sortedPosts.length}</div>
          <div className="text-gray-400 mb-2">drwxr-xr-x  2 nil nil 4096 Jun 12 16:27 .</div>
          <div className="text-gray-400 mb-2">drwxr-xr-x  3 nil nil 4096 Jun 12 16:27 ..</div>
          {sortedPosts.map((post) => (
            <div key={post.id} className="flex items-center gap-4 text-white hover:bg-green-500/10 px-2 py-1 rounded">
              <span className="text-green-400">-rw-r--r--</span>
              <span className="text-yellow-400 w-12">{post.likes} likes</span>
              <span className="text-blue-400 w-24 text-xs uppercase">{post.category}</span>
              <Link 
                href={`/blog/${post.slug}`} 
                className="text-green-400 hover:text-green-300 hover:underline flex-1"
              >
                {post.slug}.md
              </Link>
              <span className="text-gray-500 text-xs">{new Date(post.createdAt).toLocaleDateString()}</span>
            </div>
          ))}
        </div>

        <div className="mb-8">
          <span className="text-green-400">$</span>
          <span className="text-white ml-2">cat README.md</span>
        </div>

        <div className="bg-gray-900 border border-green-500/30 rounded-lg p-4 text-gray-300 text-sm">
          <p>Bitácora técnica de desarrollo web, seguridad y arquitectura de sistemas.</p>
          <p className="mt-2">Total de entradas: {sortedPosts.length}</p>
        </div>
      </div>
    </div>
  );
}
