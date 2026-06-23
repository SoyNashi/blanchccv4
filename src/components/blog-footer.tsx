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
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a
                href="mailto:nil@blanch.cc"
                className="text-muted-foreground hover:text-white transition-colors"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </a>
              <Link href="/rss.xml" className="text-muted-foreground hover:text-white transition-colors">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 13c0 3.314 2.686 6 6 6s6-2.686 6-6M6 8c0 5.523 4.477 10 10 10s10-4.477 10-10M6 3c0 7.732 6.268 14 14 14s14-6.268 14-14" />
                </svg>
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
