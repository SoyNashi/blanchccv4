"use client";

import { CheckCircle2, BookOpen } from "lucide-react";
import Link from "next/link";

const CERTS = [
  { name: "Cloud Architecture", company: "AWS", status: "Active", category: "Infrastructure" },
  { name: "Professional Developer", company: "Google", status: "Active", category: "Cloud" },
  { name: "Azure Solutions", company: "Microsoft", status: "Active", category: "Systems" },
  { name: "Network Engineering", company: "Cisco", status: "Active", category: "Security" },
  { name: "Meta Frontend Prof", company: "Meta", status: "Active", category: "Frontend" },
  { name: "Cybersecurity Ops", company: "Cisco", status: "Active", category: "Security" },
  { name: "Data Engineering", company: "Google", status: "Active", category: "Data" },
  { name: "Cloud Practitioner", company: "AWS", status: "Active", category: "Infrastructure" },
];

export const Certifications = ({ items, posts }: { items?: any[]; posts?: any[] }) => {
  const certifications = items || CERTS;
  return (
    <section className="bg-background py-40 overflow-hidden">
      <div className="px-6 mb-20 max-w-7xl mx-auto">
        <span className="text-xs font-bold tracking-[0.2em] text-muted-foreground uppercase">
          Reconocimientos
        </span>
        <h2 className="mt-6 text-5xl font-bold tracking-tighter text-white sm:text-7xl">
          CERTIFICACIONES.
        </h2>
      </div>

      <div className="flex flex-col gap-8">
        {/* Top Marquee */}
        <div className="flex overflow-hidden group">
          <div className="flex animate-marquee group-hover:[animation-play-state:paused] py-4">
            {[...certifications, ...certifications].map((cert, i) => (
              <CertCard key={`top-${i}`} cert={cert} posts={posts} />
            ))}
          </div>
        </div>

        {/* Bottom Marquee (Reverse) */}
        <div className="flex overflow-hidden group">
          <div className="flex animate-marquee-reverse group-hover:[animation-play-state:paused] py-4">
            {[...certifications, ...certifications].map((cert, i) => (
              <CertCard key={`bottom-${i}`} cert={cert} posts={posts} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

const CertCard = ({ cert, posts }: { cert: any; posts?: any[] }) => {
  const relatedPost = posts?.find((post: any) => post.id === cert.relatedPostId);

  return (
    <div className="flex flex-col w-[300px] shrink-0 mx-4 p-6 bg-card border border-white/5 rounded-2xl hover:border-white/20 transition-colors">
      <div className="flex items-center justify-between mb-8">
        <div className="h-8 w-8 rounded-full bg-white/5 flex items-center justify-center text-xs font-bold text-white">
          {cert.company ? cert.company[0] : cert.issuer ? cert.issuer[0] : '?'}
        </div>
        <CheckCircle2 className="h-4 w-4 text-green-500" />
      </div>
      <span className="text-xs font-bold tracking-widest text-muted-foreground uppercase mb-2">
        {cert.company || cert.issuer}
      </span>
      <h3 className="text-lg font-bold text-white mb-4 leading-tight">
        {cert.name}
      </h3>
      <div className="mt-auto flex items-center justify-between mb-4">
        <span className="text-[10px] font-mono text-white/40 uppercase">
          {cert.category}
        </span>
        <span className="text-[10px] font-mono text-green-500/80 uppercase px-2 py-0.5 bg-green-500/10 rounded-full">
          {cert.status}
        </span>
      </div>
      {relatedPost && (
        <Link
          href={`/blog/${relatedPost.slug}`}
          className="inline-flex items-center gap-2 px-3 py-1.5 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-colors group text-sm"
        >
          <BookOpen className="h-3.5 w-3.5 text-white/60 group-hover:text-white" />
          <span className="text-white/60 group-hover:text-white">
            Leer artículo relacionado
          </span>
        </Link>
      )}
    </div>
  );
};
