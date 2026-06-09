import { ArrowLeft, Search } from "lucide-react";
import Link from "next/link";

// Forzar el uso de Edge Runtime para compatibilidad con Cloudflare y DB
export const runtime = 'edge';

export default function BlogPage() {
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

        <div className="flex flex-col gap-8">
          {/* We'll map real posts here later */}
          <p className="text-muted-foreground font-mono text-sm italic">Conexión con base de datos preparada. Esperando contenido...</p>
        </div>
      </div>
    </div>
  );
}
