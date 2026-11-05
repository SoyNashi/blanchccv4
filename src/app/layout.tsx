import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { DockWrapper } from "@/components/ui/dock-wrapper";
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
export const metadata: Metadata = {
 title: "Nil Blanch | Desarrollo web y aplicaciones propias",
 description: "Desarrollo páginas web y aplicaciones a medida. Diseño brutalista, software propio y tecnología bajo tu control.",
 icons: { icon: "/favicon.ico", apple: "/favicon.ico" },
 manifest: "/manifest.json",
 alternates: { canonical: "https://blanch.cc" },
};
export default function RootLayout({children}:{children:React.ReactNode}){
 return <html lang="es" className="js dark"><head><meta name="theme-color" content="#0A0D10"/><link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous"/><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/></head><body className={cn(inter.variable,"min-h-screen antialiased")}><div className="relative min-h-screen">{children}</div><DockWrapper/></body></html>;
}
