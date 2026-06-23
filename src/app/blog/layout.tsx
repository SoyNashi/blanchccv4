import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../globals.css";
import { cn } from "@/lib/utils";
import BlogDockHider from "@/components/blog-dock-hider";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Insights | Nil Blanch",
  description: "Artículos sobre desarrollo web, seguridad, arquitectura de sistemas y tecnología",
};

export default function BlogLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body
        className={cn(
          inter.variable,
          "min-h-screen bg-background font-sans antialiased text-foreground"
        )}
      >
        <BlogDockHider />
        <main className="relative flex min-h-screen flex-col">
          {children}
        </main>
      </body>
    </html>
  );
}
