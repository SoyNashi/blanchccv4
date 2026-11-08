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
  grayscale?: boolean;
};

const columnFactor = (index: number, variance: number) => {
  const pseudo = ((index * 0.6180339887 + 0.35) % 1) * 2 - 1;
  return 1 + variance * pseudo;
};

export default function DriftWall({
  items,
  columns = 4,
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
  const pointerRef = useRef({ x: 0, y: 0 });
  const pointerDampedRef = useRef({ x: 0, y: 0 });
  const lastTsRef = useRef<number | null>(null);
  const [containerHeight, setContainerHeight] = useState(600);
  const [containerWidth, setContainerWidth] = useState(1200);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [reduced, setReduced] = useState(false);

  // Deduplicamos por archivo de imagen: un logo solo puede entrar una vez en el conjunto.
  // Después cada columna conserva un orden fijo y repite el ciclo completo sin reordenar
  // tarjetas a mitad del movimiento, evitando saltos visuales.
  const [shuffleSeed, setShuffleSeed] = useState(0);
  const compactLayout = containerWidth <= 760;
  const responsiveColumns = Math.max(1, Math.floor(columns));
  const renderedTileWidth = compactLayout ? Math.min(tileWidth, 108) : tileWidth;
  const renderedTileHeight = compactLayout ? Math.min(tileHeight, 104) : tileHeight;
  const renderedGap = compactLayout ? Math.min(gap, 10) : gap;

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

  const uniqueItems = useMemo(() => {
    const seen = new Set<string>();
    return items.filter((item) => {
      const key = item.image.trim().toLowerCase() || item.href?.trim().toLowerCase() || item.title.trim().toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }, [items]);

  const shuffledItems = useMemo(
    () => shuffle(uniqueItems, shuffleSeed),
    [uniqueItems, shuffleSeed]
  );

  // Cada columna contiene el catálogo completo en un orden aleatorio independiente.
  // Al repetir una permutación sin duplicados, nunca aparecen dos logos iguales seguidos,
  // tampoco en el salto entre el final y el principio del ciclo.
  const columnItems = useMemo(
    () => Array.from({ length: responsiveColumns }, (_, column) =>
      shuffle(uniqueItems, shuffleSeed + (column + 1) * 104729)
    ),
    [uniqueItems, responsiveColumns, shuffleSeed]
  );

  const columnMeta = useMemo(() => {
    const unit = renderedTileHeight + renderedGap;
    return columnItems.map((col) => {
      const copyHeight = Math.max(unit, col.length * unit);
      const copies = Math.max(2, Math.ceil((containerHeight * 1.6) / copyHeight) + 1);
      return { copyHeight, copies };
    });
  }, [columnItems, renderedTileHeight, renderedGap, containerHeight]);

  const baseVelocities = useMemo(() => columnItems.map((_, column) => {
    let value = (shuffleSeed + (column + 1) * 104729) >>> 0;
    value = (value * 1664525 + 1013904223) >>> 0;
    const random = value / 4294967296;
    const magnitude = speed * (0.58 + random * 0.82) * columnFactor(column, variance);
    return magnitude * (random > 0.5 ? 1 : -1);
  }), [columnItems, speed, variance, shuffleSeed]);

  const applyPlaneTransform = useCallback((px: number, py: number, compact: boolean) => {
    const plane = planeRef.current;
    if (!plane) return;
    plane.style.transform = compact
      ? `translate(-50%, -50%) scale(.94) rotateX(0deg) rotateY(-7deg) rotateZ(0deg) translateZ(-35px)`
      : `translate(-50%, -50%) scale(1.18) rotateX(${tilt + py}deg) rotateY(${turn + px}deg) rotateZ(${roll}deg) translateZ(${-depth}px)`;
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
      applyPlaneTransform(pointerDampedRef.current.x, pointerDampedRef.current.y, compactLayout);

      columnMeta.forEach((meta, column) => {
        const el = trackRefs.current[column];
        if (!el) return;
        if (!reduced) {
          const target = baseVelocities[column];
          let next = (offsetsRef.current[column] ?? 0) + target * dt;
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
  }, [baseVelocities, columnMeta, parallax, reduced, compactLayout, applyPlaneTransform]);

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
    setActiveId(tile.dataset.tileId ?? null);
  };

  const release = () => {
    setActiveId(null);
  };

  if (!items.length) return null;

  return (
    <div
      ref={containerRef}
      className={`drift-wall${reduced ? " drift-wall--reduced" : ""}`}
      style={{
        "--dw-tile-w": `${renderedTileWidth}px`,
        "--dw-tile-h": `${renderedTileHeight}px`,
        "--dw-gap": `${renderedGap}px`,
        "--dw-radius": `${radius}px`,
        "--dw-perspective": `${perspective}px`,
        "--dw-lift": `${lift}px`,
        "--dw-dim": dim,
        "--dw-gray": grayscale ? 1 : 0,
        "--dw-overlay": overlayColor,
        "--dw-edge": `${Math.max(0, (1 - fade) * 100)}%`
      } as React.CSSProperties}
      onPointerMove={handlePointerMove}
      onPointerLeave={() => {
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
                {Array.from({ length: meta.copies }, (_, copy) =>
                  col.map((item, index) => {
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
                      onFocus: () => { setActiveId(id); },
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
