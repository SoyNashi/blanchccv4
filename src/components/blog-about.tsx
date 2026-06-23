import { GithubIcon, LinkedinIcon, MailIcon, MapPinIcon } from "lucide-react";

export default function BlogAbout() {
  return (
    <section className="bg-gradient-to-b from-background to-card border-b border-white/5 py-16 md:py-24">
      <div className="mx-auto max-w-7xl px-4 md:px-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 items-center">
          {/* Logo grande */}
          <div className="lg:col-span-1 flex justify-center">
            <svg viewBox="0 0 100 100" className="w-48 h-48 md:w-64 md:h-64">
              <defs>
                <linearGradient id="aboutLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#00ff00" />
                  <stop offset="100%" stopColor="#00cc00" />
                </linearGradient>
              </defs>
              <circle cx="50" cy="50" r="45" fill="none" stroke="url(#aboutLogoGradient)" strokeWidth="2" />
              <path d="M30 50 L50 30 L70 50 L50 70 Z" fill="url(#aboutLogoGradient)" />
              <circle cx="50" cy="50" r="8" fill="#0a0a0a" />
            </svg>
          </div>

          {/* Información */}
          <div className="lg:col-span-2 space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight">
              Nil Blanch
            </h1>
            
            <p className="text-xl text-muted-foreground">
              Digital Product Builder & Full-Stack Developer
            </p>

            <div className="space-y-4 text-muted-foreground">
              <p>
                Especialista en desarrollo web, ecommerce y SEO técnico. Construyendo productos digitales reales con foco en rendimiento, seguridad y experiencia de usuario.
              </p>
              <p>
                Más de 5 años de experiencia creando soluciones escalables para startups y empresas, combinando diseño minimalista con arquitectura robusta.
              </p>
            </div>

            <div className="flex items-center gap-2 text-muted-foreground">
              <MapPinIcon className="h-4 w-4" />
              <span>Barcelona, España</span>
            </div>

            <div className="flex gap-4 pt-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors"
              >
                <GithubIcon className="h-5 w-5" />
                GitHub
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors"
              >
                <LinkedinIcon className="h-5 w-5" />
                LinkedIn
              </a>
              <a
                href="mailto:contact@blanch.cc"
                className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors"
              >
                <MailIcon className="h-5 w-5" />
                Email
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
