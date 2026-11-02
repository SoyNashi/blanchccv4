import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { DockWrapper } from "@/components/ui/dock-wrapper";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  metadataBase: new URL("https://blanch.cc"),
  title: {
    default: "Nil Blanch | Redes, seguridad y productos digitales",
    template: "%s | Nil Blanch",
  },
  description: "Espacio personal de Nil Blanch: desarrollo de producto, redes, infraestructura, ciberseguridad, privacidad digital y proyectos independientes como Blau360, Bastet Project y Ghostnet.",
  keywords: ["Nil Blanch", "redes", "ciberseguridad", "privacidad digital", "infraestructura", "desarrollo web", "Ghostnet", "Bastet Project", "Blau360"],
  authors: [{ name: "Nil Blanch", url: "https://blanch.cc" }],
  creator: "Nil Blanch",
  openGraph: {
    type: "website",
    locale: "es_ES",
    url: "https://blanch.cc",
    siteName: "Nil Blanch",
    title: "Nil Blanch | Redes, seguridad y productos digitales",
    description: "Desarrollo, redes, seguridad y proyectos construidos con criterio propio.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Nil Blanch | Redes, seguridad y productos digitales",
    description: "Desarrollo, redes, seguridad y proyectos construidos con criterio propio.",
  },
  icons: { icon: "/favicon.ico", apple: "/favicon.ico" },
  manifest: "/manifest.json",
  alternates: { canonical: "https://blanch.cc" },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es" className="dark">
      <body className={cn(inter.variable, "min-h-screen bg-background font-sans antialiased text-foreground")}>
        <main className="relative flex min-h-screen flex-col">{children}</main>
        <DockWrapper />
      </body>
    </html>
  );
}
