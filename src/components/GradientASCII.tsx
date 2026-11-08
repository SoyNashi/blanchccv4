"use client";
import { useEffect, useRef } from "react";
import "./GradientASCII.css";

const COLORS = ["#C3CAD2", "#E4E8EC", "#FF4A1C"];
const hash = (x: number, y: number) => {
  const value = Math.sin(x * 127.1 + y * 311.7) * 43758.5453;
  return value - Math.floor(value);
};

export default function GradientASCII() {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d", { alpha: true });
    if (!container || !canvas || !ctx) return;

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let width = 1, height = 1, dpr = 1, raf = 0, start = 0, lastDraw = 0;

    const resize = () => {
      const rect = container.getBoundingClientRect();
      width = Math.max(1, rect.width);
      height = Math.max(1, rect.height);
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    const draw = (now: number) => {
      if (!start) start = now;
      if (!reduceMotion && now - lastDraw < 32) {
        raf = requestAnimationFrame(draw);
        return;
      }
      lastDraw = now;
      const time = reduceMotion ? 0 : (now - start) / 1000;
      ctx.clearRect(0, 0, width, height);

      const cellW = width < 700 ? 11 : 13;
      const cellH = cellW * 1.42;
      const cols = Math.ceil(width / cellW);
      const rows = Math.ceil(height / cellH);
      ctx.font = `500 ${cellW}px "Geist Mono", ui-monospace, monospace`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      // Una fractura diagonal deja una estela de bits que se desprenden del bloque.
      const front = cols * 0.76 - time * 0.7;
      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          const seed = hash(col, row);
          const edge = col + row * 0.34 - front;
          const wake = Math.max(0, Math.min(1, (edge + 8) / 18));
          const fracture = Math.exp(-Math.pow(edge / 5.5, 2));
          const sparse = seed > 0.28 + wake * 0.42;
          if (edge < -11 || (sparse && fracture < 0.12)) continue;

          const x = col * cellW + cellW / 2;
          const drift = Math.max(0, edge) * 0.34;
          const y = row * cellH + cellH / 2 + Math.sin(time * 0.55 + seed * 8) * drift * 0.18;
          const opacity = Math.min(0.64, (0.12 + fracture * 0.42 + wake * 0.22) * (0.55 + seed * 0.45));
          const orange = seed > 0.94 && (fracture > 0.18 || wake > 0.55);
          ctx.globalAlpha = opacity;
          ctx.fillStyle = COLORS[orange ? 2 : seed > 0.58 ? 1 : 0];
          ctx.fillText(hash(col + 19, row + 7) > 0.5 ? "1" : "0",
            x + (seed - 0.5) * drift * 0.7,
            y - drift * (0.12 + seed * 0.18));
        }
      }
      ctx.globalAlpha = 1;
      if (!reduceMotion) raf = requestAnimationFrame(draw);
    };

    const observer = new ResizeObserver(resize);
    observer.observe(container);
    resize();
    raf = requestAnimationFrame(draw);
    return () => { cancelAnimationFrame(raf); observer.disconnect(); };
  }, []);

  return <div ref={containerRef} className="gradient-ascii-container"><canvas ref={canvasRef} className="gradient-ascii-canvas" aria-hidden="true" /></div>;
}
