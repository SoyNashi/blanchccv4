import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import certifications from "@/data/certifications.json";

export default function CertificationsPage() {
  const sortedCerts = certifications.sort((a, b) => a.order - b.order);

  return (
    <div className="min-h-screen bg-background px-6 py-20">
      <div className="mx-auto max-w-7xl">
        <Link href="/" className="group flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase mb-12">
          <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Volver
        </Link>
        
        <h1 className="text-6xl font-bold tracking-tighter text-white mb-4">Certificaciones</h1>
        <p className="text-xl text-muted-foreground mb-16 max-w-2xl">
          Credenciales profesionales y certificaciones técnicas obtenidas a lo largo de mi carrera.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sortedCerts.map((cert) => (
            <div key={cert.id} className="bg-card border border-white/5 rounded-2xl p-8 hover:border-white/20 transition-all group">
              <div className="h-16 w-16 mb-6 flex items-center justify-center">
                <img
                  src={`/certifications/${cert.icon}.svg`}
                  alt={cert.name}
                  className="h-14 w-14 object-contain"
                />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{cert.name}</h3>
              <p className="text-muted-foreground mb-4">{cert.issuer}</p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-white/60">{cert.date}</span>
                <span className="text-white/40 font-mono text-xs">{cert.credentialId}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
