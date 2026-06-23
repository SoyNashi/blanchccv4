import { Github, Linkedin, Mail, Rss } from "lucide-react";
import Link from "next/link";

export default function BlogFooter() {
  return (
    <footer className="bg-card border-t border-white/5 py-12 mt-20">
      <div className="mx-auto max-w-7xl px-4 md:px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Logo y descripción */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <svg viewBox="0 0 100 100" className="w-8 h-8">
                <defs>
                  <linearGradient id="footerLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#00ff00" />
                    <stop offset="100%" stopColor="#00cc00" />
                  </linearGradient>
                </defs>
                <circle cx="50" cy="50" r="45" fill="none" stroke="url(#footerLogoGradient)" strokeWidth="2" />
                <path d="M30 50 L50 30 L70 50 L50 70 Z" fill="url(#footerLogoGradient)" />
                <circle cx="50" cy="50" r="8" fill="#0a0a0a" />
              </svg>
              <span className="text-white font-bold tracking-tighter">Nil Blanch</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Digital Product Builder & Full-Stack Developer
            </p>
          </div>

          {/* Enlaces rápidos */}
          <div>
            <h3 className="text-sm font-bold tracking-widest text-white uppercase mb-4">
              Enlaces
            </h3>
            <div className="space-y-2">
              <Link href="/" className="block text-sm text-muted-foreground hover:text-white transition-colors">
                Portfolio
              </Link>
              <Link href="/blog" className="block text-sm text-muted-foreground hover:text-white transition-colors">
                Insights
              </Link>
              <Link href="/rss.xml" className="block text-sm text-muted-foreground hover:text-white transition-colors">
                RSS Feed
              </Link>
            </div>
          </div>

          {/* Social */}
          <div>
            <h3 className="text-sm font-bold tracking-widest text-white uppercase mb-4">
              Conectar
            </h3>
            <div className="flex gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-white transition-colors"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-white transition-colors"
              >
                <Linkedin className="h-5 w-5" />
              </a>
              <a
                href="mailto:nil@blanch.cc"
                className="text-muted-foreground hover:text-white transition-colors"
              >
                <Mail className="h-5 w-5" />
              </a>
              <Link href="/rss.xml" className="text-muted-foreground hover:text-white transition-colors">
                <Rss className="h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>

        <div className="border-t border-white/5 pt-8 text-center">
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} Nil Blanch. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}
