"use client";
import Link from "next/link";
import { useState } from "react";

export default function BlogNavbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-lg border-b border-white/5">
      <div className="mx-auto max-w-7xl px-4 md:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo con SVG */}
          <Link href="/blog" className="flex items-center gap-3">
            <img src="/path2.svg" alt="Logo" className="w-10 h-10" />
            <span className="text-white font-bold tracking-tighter text-lg">Insights</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            <Link href="/" className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Portfolio
            </Link>
            <Link href="/blog" className="text-sm font-bold tracking-widest text-white uppercase">
              Insights
            </Link>
            <Link href="/rss.xml" className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 13c0 3.314 2.686 6 6 6s6-2.686 6-6M6 8c0 5.523 4.477 10 10 10s10-4.477 10-10M6 3c0 7.732 6.268 14 14 14s14-6.268 14-14" />
              </svg>
              RSS
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-white hover:text-white/80 transition-colors"
          >
            {mobileMenuOpen ? <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg> : <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-white/5">
            <div className="flex flex-col gap-4">
              <Link
                href="/"
                className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Portfolio
              </Link>
              <Link
                href="/blog"
                className="text-sm font-bold tracking-widest text-white uppercase"
                onClick={() => setMobileMenuOpen(false)}
              >
                Insights
              </Link>
              <Link
                href="/rss.xml"
                className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 13c0 3.314 2.686 6 6 6s6-2.686 6-6M6 8c0 5.523 4.477 10 10 10s10-4.477 10-10M6 3c0 7.732 6.268 14 14 14s14-6.268 14-14" />
                </svg>
                RSS
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
