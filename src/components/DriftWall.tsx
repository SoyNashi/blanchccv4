"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import "./DriftWall.css";

export type DriftWallItem = {
  image: string;
  title: string;
  href?: string;
};

type DriftWallProps = {
  items: DriftWallItem[];
  columns?: number;
  tileWidth?: number;
  tileHeight?: number;
  gap?: number;
  tilt?: number;
  turn?: number;
  perspective?: number;
  depth?: number;
  speed?: number;
  direction?: "up" | "down";
  variance?: number;
  parallax?: number;
  lift?: number;
  fade?: number;
  dim?: number;
  overlayColor?: string;
  radius?: number;
  roll?: number;
  pauseOnHover?: boolean;
  grayscale?: boolean;
};

const columnFactor = (index: number, variance: number) => {
  const pseudo = ((index * 0.6180339887 + 0.35) % 1) * 2 - 1;
  return 1 + variance * pseudo;
};

export default function DriftWall({
  items,
  columns = 3,
  tileWidth = 152,
  tileHeight = 150,
  gap = 16,
  tilt = 1,
  turn = -30,
  roll = 6,
  perspective = 600,
  depth = 270,
  speed = 54,
  variance = 0.5,
  parallax = 1,
  pauseOnHover = false,
  lift = 64,
  fade = 0.45,
  dim = 1,
  grayscale = false,
  overlayColor = "#060010",
  radius = 14
}: DriftWallProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const planeRef = useRef<HTMLDivElement>(null);
  const trackRefs = useRef<(HTMLDivElement | null)[]>([]);
  const offsetsRef = useRef<number[]>([]);
  const velocitiesRef = useRef<number[]>([]);
  const hoveredColRef = useRef(-1);
  const wallHoveredRef = useRef(false);
  const pointerRef = useRef({ x: 0, y: 0 });
  const pointerDampedRef = useRef({ x: 0, y: 0 });
  const lastTsRef = useRef<number | null>(null);
  const [containerHeight, setContainerHeight] = useState(600);
  const [containerWidth, setContainerWidth] = useState(1200);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [reduced, setReduced] = useState(false);

  // Cada columna contiene el conjunto completo de logos en un orden distinto.
  // La semilla cambia al montar para mezclar la composición en cada recarga
  // sin provocar diferencias de hidratación entre servidor y cliente.
  const [shuffleSeed, setShuffleSeed] = useState(0);
  const responsiveColumns = containerWidth <= 520 ? Math.min(2, columns) : containerWidth <= 900 ? Math.min(3, columns) : columns;

  useEffect(() => {
    setShuffleSeed(Math.floor(Math.random() * 1_000_000) + 1);
  }, []);

  const shuffle = (source: DriftWallItem[], seed: number) => {
    const result = [...source];
    let value = seed >>> 0;
    const random = () => { value = (value * 1664525 + 1013904223) >>> 0; return value / 4294967296; };
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  };

  const columnItems = useMemo(() =>
    Array.from({ length: responsiveColumns }, (_, column) => shuffle(items, shuffleSeed + (column + 1) * 7919)),
  [items, responsiveColumns, shuffleSeed]);

  const columnPasses = useMemo(() => columnItems.map((col, column) => {
    let previous: DriftWallItem[] = [];
    return Array.from({ length: columnMeta[column].copies }, (_, copy) => {
      let next = shuffle(col, shuffleSeed + (column + 1) * 7919 + (copy + 1) * 15485863);
      if (copy > 0 && next.length > 1 && next.every((item, index) => item === previous[index])) {
        next = [...next.slice(1), next[0]];
      }
      previous = next;
      return next;
    });
  }), [columnItems, columnMeta, shuffleSeed]);
  const columnMeta = useMemo(() => {
    const unit = tileHeight + gap;
    return columnItems.map((col) => {
      const copyHeight = Math.max(unit, col.length * unit);
      const copies = Math.max(2, Math.ceil((containerHeight * 1.6) / copyHeight) + 1);
      return { copyHeight, copies };
    });
  }, [columnItems, tileHeight, gap, containerHeight]);

  const baseVelocities = useMemo(() => columnItems.map((_, column) => {
    let value = (shuffleSeed + (column + 1) * 104729) >>> 0;
    value = (value * 1664525 + 1013904223) >>> 0;
    const random = value / 4294967296;
    const magnitude = speed * (0.58 + random * 0.82) * columnFactor(column, variance);
    return magnitude * (random > 0.5 ? 1 : -1);
  }), [columnItems, speed, variance, shuffleSeed]);

  const applyPlaneTransform = useCallback((px: number, py: number) => {
    const plane = planeRef.current;
    if (!plane) return;
    plane.style.transform =
      `translate(-50%, -50%) scale(1.18) rotateX(${tilt + py}deg) rotateY(${turn + px}deg) rotateZ(${roll}deg) translateZ(${-depth}px)`;
  }, [tilt, turn, roll, depth]);

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduced(media.matches);
    update();
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);

  useEffect(() => {
    const node = containerRef.current;
    if (!node) return;
    const observer = new ResizeObserver(([entry]) => {
      setContainerHeight(entry.contentRect.height || 600);
      setContainerWidth(entry.contentRect.width || 1200);
    });
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    offsetsRef.current = columnMeta.map((meta, column) => meta.copyHeight * (((shuffleSeed + column * 37) % 100) / 100));
    velocitiesRef.current = columnItems.map(() => 0);
  }, [columnMeta, columnItems, shuffleSeed]);

  useEffect(() => {
    let raf = 0;
    const animate = (timestamp: number) => {
      if (lastTsRef.current === null) lastTsRef.current = timestamp;
      const dt = Math.min(0.05, Math.max(0, timestamp - lastTsRef.current) / 1000);
      lastTsRef.current = timestamp;

      const maxTilt = parallax * 8;
      const targetX = reduced ? 0 : pointerRef.current.x * maxTilt;
      const targetY = reduced ? 0 : -pointerRef.current.y * maxTilt;
      const damp = 1 - Math.exp(-dt / 0.12);
      pointerDampedRef.current.x += (targetX - pointerDampedRef.current.x) * damp;
      pointerDampedRef.current.y += (targetY - pointerDampedRef.current.y) * damp;
      applyPlaneTransform(pointerDampedRef.current.x, pointerDampedRef.current.y);

      columnMeta.forEach((meta, column) => {
        const el = trackRefs.current[column];
        if (!el) return;
        if (!reduced) {
          const paused = (wallHoveredRef.current && pauseOnHover) || hoveredColRef.current === column;
          const target = baseVelocities[column] * (paused ? 0 : 1);
          const ease = 1 - Math.exp(-dt / (target === 0 ? 0.16 : 0.28));
          velocitiesRef.current[column] += (target - velocitiesRef.current[column]) * ease;
          let next = (offsetsRef.current[column] ?? 0) + velocitiesRef.current[column] * dt;
          next = ((next % meta.copyHeight) + meta.copyHeight) % meta.copyHeight;
          offsetsRef.current[column] = next;
        }
        el.style.transform = `translate3d(0, ${-(offsetsRef.current[column] ?? 0)}px, 0)`;
      });
      raf = window.requestAnimationFrame(animate);
    };
    raf = window.requestAnimationFrame(animate);
    return () => {
      window.cancelAnimationFrame(raf);
      lastTsRef.current = null;
    };
  }, [baseVelocities, columnMeta, pauseOnHover, parallax, reduced, applyPlaneTransform]);

  const handlePointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    if (parallax > 0 && !reduced) {
      pointerRef.current = {
        x: (event.clientX - rect.left) / rect.width - 0.5,
        y: (event.clientY - rect.top) / rect.height - 0.5
      };
    }
    const tile = (event.target as HTMLElement).closest<HTMLElement>("[data-tile-id]");
    if (!tile) return;
    const column = Number(tile.dataset.col);
    hoveredColRef.current = column;
    setActiveId(tile.dataset.tileId ?? null);
  };

  const release = () => {
    hoveredColRef.current = -1;
    setActiveId(null);
  };

  if (!items.length) return null;

  return (
    <div
      ref={containerRef}
      className={`drift-wall${reduced ? " drift-wall--reduced" : ""}`}
      style={{
        "--dw-tile-w": `${tileWidth}px`,
        "--dw-tile-h": `${tileHeight}px`,
        "--dw-gap": `${gap}px`,
        "--dw-radius": `${radius}px`,
        "--dw-perspective": `${perspective}px`,
        "--dw-lift": `${lift}px`,
        "--dw-dim": dim,
        "--dw-gray": grayscale ? 1 : 0,
        "--dw-overlay": overlayColor,
        "--dw-edge": `${Math.max(0, (1 - fade) * 100)}%`
      } as React.CSSProperties}
      onPointerMove={handlePointerMove}
      onPointerEnter={() => { wallHoveredRef.current = true; }}
      onPointerLeave={() => {
        wallHoveredRef.current = false;
        pointerRef.current = { x: 0, y: 0 };
        release();
      }}
      role="group"
      aria-label="Logotipos de proyectos y colaboradores"
    >
      <div ref={planeRef} className="drift-wall__plane">
        {columnItems.map((col, column) => {
          const meta = columnMeta[column];
          return (
            <div className="drift-wall__col" key={`column-${column}`}>
              <div className="drift-wall__track" ref={(el) => { trackRefs.current[column] = el; }}>
                {columnPasses[column].flatMap((pass, copy) =>
                  pass.map((item, index) => {
                    const id = `${column}-${copy}-${index}`;
                    const tile = (
                      <span className="drift-wall__inner">
                        <img src={item.image} alt={item.title} loading="lazy" decoding="async" draggable={false} />
                        <span className="drift-wall__overlay" aria-hidden="true" />
                      </span>
                    );
                    const common = {
                      key: id,
                      className: `drift-wall__tile${activeId === id ? " is-active" : ""}`,
                      "data-tile-id": id,
                      "data-col": column,
                      onFocus: () => { hoveredColRef.current = column; setActiveId(id); },
                      onBlur: release
                    };
                    return item.href ? (
                      <a {...common} href={item.href} target="_blank" rel="noreferrer noopener" aria-label={`Abrir ${item.title}`}>{tile}</a>
                    ) : (
                      <div {...common} tabIndex={0} role="img" aria-label={item.title}>{tile}</div>
                    );
                  })
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
