"use client";

import { useEffect } from "react";

export default function BlogDockHider() {
  useEffect(() => {
    // Ocultar Dock en el blog
    const hideDock = () => {
      const dockElements = document.querySelectorAll('.fixed.bottom-8');
      dockElements.forEach(el => {
        (el as HTMLElement).style.display = 'none';
      });
    };

    // Esperar a que el DOM esté completamente cargado
    if (typeof window !== 'undefined') {
      hideDock();
      
      // Ocultar Dock cuando se monta el componente
      const observer = new MutationObserver(hideDock);
      observer.observe(document.body, { childList: true, subtree: true });

      return () => observer.disconnect();
    }
  }, []);

  return null;
}
