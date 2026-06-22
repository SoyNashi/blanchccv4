"use client";
import { Home, Rss, Menu, X } from "lucide-react";
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
            <svg viewBox="0 0 100 100" className="w-10 h-10">
              <defs>
                <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#00ff00" />
                  <stop offset="100%" stopColor="#00cc00" />
                </linearGradient>
              </defs>
              <circle cx="50" cy="50" r="45" fill="none" stroke="url(#logoGradient)" strokeWidth="2" />
              <path d="M30 50 L50 30 L70 50 L50 70 Z" fill="url(#logoGradient)" />
              <circle cx="50" cy="50" r="8" fill="#0a0a0a" />
            </svg>
            <span className="text-white font-bold tracking-tighter text-lg">Insights</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            <Link href="/" className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors">
              <Home className="h-4 w-4" />
              Portfolio
            </Link>
            <Link href="/blog" className="text-sm font-bold tracking-widest text-white uppercase">
              Insights
            </Link>
            <Link href="/rss.xml" className="flex items-center gap-2 text-sm font-bold tracking-widest text-muted-foreground uppercase hover:text-white transition-colors">
              <Rss className="h-4 w-4" />
              RSS
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-white hover:text-white/80 transition-colors"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
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
                <Home className="h-4 w-4" />
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
                <Rss className="h-4 w-4" />
                RSS
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
