"use client";

import { useEffect, useRef } from "react";
import "./GradientASCII.css";

type Props = {
  colors?: string[];
  shape?: "horizon" | "pinch" | "rise" | "eclipse";
  characters?: string;
  cellSize?: number;
  density?: number;
  glyphOpacity?: number;
  flicker?: number;
  flow?: number;
  speed?: number;
  grain?: number;
  variation?: number;
  mouseInteraction?: boolean;
  scrambleRadius?: number;
  clickEffect?: "none" | "wave" | "burst";
  intro?: boolean;
  lightMode?: boolean;
};

export default function GradientASCII({
  colors = ["#1e3fd8", "#f6f8ff", "#a5d8ff", "#38bdf8"],
  shape = "rise",
  characters = " 01",
  cellSize = 12,
  density = 0.8,
  glyphOpacity = 0.84,
  flicker = 1,
  flow = 2,
  speed = 0,
  grain = 0.19,
  variation = 20,
  mouseInteraction = true,
  scrambleRadius = 0.4,
  clickEffect = "wave",
  intro = true,
  lightMode = false
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d", { alpha: true });
    if (!container || !canvas || !ctx) return;

    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const palette = colors.map(value => {
      const color = value.replace("#", "");
      const number = parseInt(color, 16);
      return [(number >> 16) & 255, (number >> 8) & 255, number & 255] as const;
    });
    const chars = [...new Set(characters.split(""))];
    const pointer = { x: -1000, y: -1000, active: false };
    const clicks: { x: number; y: number; at: number }[] = [];
    let width = 1, height = 1, dpr = 1, raf = 0, start = performance.now(), frame = 0;
    let introProgress = intro && !reduce ? 0 : 1;

    const resize = () => {
      const rect = container.getBoundingClientRect();
      width = Math.max(1, rect.width);
      height = Math.max(1, rect.height);
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    const colorAt = (t: number) => {
      const scaled = Math.max(0, Math.min(0.9999, t)) * (palette.length - 1);
      const i = Math.floor(scaled), mix = scaled - i;
      const a = palette[i], b = palette[Math.min(i + 1, palette.length - 1)];
      return a.map((v, k) => Math.round(v + (b[k] - v) * mix));
    };
    const locate = (event: PointerEvent) => {
      const rect = container.getBoundingClientRect();
      pointer.x = event.clientX - rect.left;
      pointer.y = event.clientY - rect.top;
      pointer.active = pointer.x >= 0 && pointer.x <= width && pointer.y >= 0 && pointer.y <= height;
    };
    const onClick = (event: PointerEvent) => {
      if (!mouseInteraction || reduce || clickEffect === "none") return;
      locate(event);
      if (pointer.active) clicks.unshift({ x: pointer.x, y: pointer.y, at: performance.now() });
      clicks.splice(4);
    };
    const draw = (now: number) => {
      const elapsed = (now - start) / 1000;
      if (!reduce) introProgress = Math.min(1, introProgress + (now - (draw as any).last || 16) / 2400);
      (draw as any).last = now;
      ctx.clearRect(0, 0, width, height);
      const cols = Math.ceil(width / cellSize), rows = Math.ceil(height / (cellSize * 1.35));
      const centerX = width * (0.5 + Math.sin(elapsed * 0.12) * 0.025);
      const centerY = height * 0.76;
      const radiusX = width * 0.84, radiusY = height * 0.95;
      ctx.font = `300 ${cellSize}px "Geist Mono", ui-monospace, monospace`;
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      for (let row = 0; row < rows; row++) for (let col = 0; col < cols; col++) {
        const x = col * cellSize + cellSize / 2, y = row * cellSize * 1.35 + cellSize / 2;
        const dx = (x - centerX) / radiusX, dy = (y - centerY) / radiusY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        let value = Math.max(0, 1 - dist);
        if (shape === "horizon") value = Math.max(0, Math.min(1, (y / height - 0.32 + Math.abs(dx) * 0.2) * 2.2));
        if (shape === "pinch") value = Math.exp(-Math.pow((y - height * 0.48) / (height * (0.08 + Math.abs(dx) * 0.2)), 2));
        if (shape === "eclipse") value = Math.max(0, 1 - Math.abs(Math.hypot(dx, dy) - 0.38) * 8);
        value = Math.pow(value, 0.8) * introProgress;
        const age = clicks.find(click => Math.abs(Math.hypot(x - click.x, y - click.y) - (now - click.at) * 0.22) < 18);
        if (age) value = Math.max(value, 0.9);
        if (mouseInteraction && pointer.active && !reduce) {
          const distance = Math.hypot(x - pointer.x, y - pointer.y) / Math.max(1, Math.min(width, height));
          if (distance < scrambleRadius) value = Math.max(value, 0.2 + (1 - distance / scrambleRadius) * 0.8);
        }
        const hash = Math.abs(Math.sin((col + variation) * 127.1 + (row + variation) * 311.7));
        if (hash > density || value < 0.035) continue;
        const flick = reduce ? 0 : (Math.sin(now * 0.009 + hash * 20) * 0.5 + 0.5) * flicker * 0.16;
        const tone = Math.min(1, value + flick);
        const [r, g, b] = colorAt(tone);
        const charIndex = Math.min(chars.length - 1, Math.floor(tone * (chars.length - 1)));
        ctx.globalAlpha = glyphOpacity * Math.min(1, value * 2.4);
        ctx.fillStyle = lightMode ? "#0a1740" : `rgb(${r} ${g} ${b})`;
        ctx.fillText(chars[charIndex] || " ", x, y);
      }
      ctx.globalAlpha = 1;
      if (grain > 0) {
        ctx.globalAlpha = grain * 0.12;
        for (let i = 0; i < Math.min(220, width * height / 9000); i++) {
          const x = Math.random() * width, y = Math.random() * height;
          ctx.fillStyle = "#fff"; ctx.fillRect(x, y, 1, 1);
        }
        ctx.globalAlpha = 1;
      }
      clicks.splice(0, clicks.length, ...clicks.filter(click => now - click.at < 1200));
      frame++;
      if (!reduce || introProgress < 1 || clicks.length) raf = requestAnimationFrame(draw);
    };
    const observer = new ResizeObserver(resize);
    observer.observe(container);
    window.addEventListener("pointermove", locate, { passive: true });
    window.addEventListener("pointerdown", onClick, { passive: true });
    resize();
    raf = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(raf);
      observer.disconnect();
      window.removeEventListener("pointermove", locate);
      window.removeEventListener("pointerdown", onClick);
    };
  }, [colors, shape, characters, cellSize, density, glyphOpacity, flicker, flow, speed, grain, variation, mouseInteraction, scrambleRadius, clickEffect, intro, lightMode]);

  return <div ref={containerRef} className="gradient-ascii-container"><canvas ref={canvasRef} className="gradient-ascii-canvas" aria-hidden="true" /></div>;
}
