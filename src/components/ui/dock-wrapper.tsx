"use client";
import { usePathname } from "next/navigation";
import { Dock } from "./dock";

export const DockWrapper = () => {
  const pathname = usePathname();
  
  // Solo mostrar dock en la página principal
  const showDock = pathname === "/";
  
  if (!showDock) return null;
  
  return <Dock />;
};
