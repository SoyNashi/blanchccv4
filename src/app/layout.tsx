import type { Metadata } from "next";
import type { CSSProperties } from "react";
import { Archivo, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const archivo = Archivo({
  subsets: ["latin"],
  variable: "--font-archivo",
  display: "swap",
});

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-ibm-plex-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Nil Blanch | Desarrollo web y aplicaciones propias",
  description:
    "Desarrollo páginas web y aplicaciones a medida. Diseño brutalista, software propio y tecnología bajo tu control.",
  icons: { icon: "/favicon.ico", apple: "/favicon.ico" },
  manifest: "/manifest.json",
  alternates: { canonical: "https://blanch.cc" },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const fontVariables = {
    "--f": archivo.style.fontFamily,
    "--m": ibmPlexMono.style.fontFamily,
  } as CSSProperties;

  return (
    <html lang="es" className="js dark">
      <head>
        <meta name="theme-color" content="#0A0D10" />
      </head>
      <body
        className={cn(
          archivo.variable,
          ibmPlexMono.variable,
          "min-h-screen antialiased",
        )}
        style={fontVariables}
      >
        <div className="relative min-h-screen">{children}</div>
      </body>
    </html>
  );
}
