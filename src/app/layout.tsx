import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { DockWrapper } from "@/components/ui/dock-wrapper";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Nil Blanch | Digital Product Builder",
  description: "Especialista en desarrollo web, ecommerce y SEO técnico. Construyendo productos digitales reales.",
  icons: {
    icon: "/favicon.ico",
    apple: "/favicon.ico",
  },
  manifest: "/manifest.json",
};

export default function RootLayout({
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
        <main className="relative flex min-h-screen flex-col">
          {children}
        </main>
        <DockWrapper />
      </body>
    </html>
  );
}
