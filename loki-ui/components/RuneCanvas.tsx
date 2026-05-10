"use client";

import { useEffect, useRef } from "react";
import { type Status } from "@/hooks/useLoki";

interface Rune {
  x: number;
  y: number;
  z: number; // depth for 2.5D parallax
  vx: number;
  vy: number;
  char: string;
  alpha: number;
  size: number;
  rotation: number;
  rotSpeed: number;
  glowing: boolean;
}

const RUNE_CHARS = "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ";
const PARTICLE_COUNT = 55;

function lerp(a: number, b: number, t: number) {
  return a + (b - a) * t;
}

export default function RuneCanvas({ status }: { status: Status }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const runesRef = useRef<Rune[]>([]);
  const rafRef = useRef<number>(0);
  const statusRef = useRef(status);

  useEffect(() => {
    statusRef.current = status;
  }, [status]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d")!;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    // Initialise runes
    runesRef.current = Array.from({ length: PARTICLE_COUNT }, () => spawnRune(canvas));

    let lastTime = 0;

    const tick = (now: number) => {
      const dt = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      const st = statusRef.current;
      const speedMul =
        st === "speaking" ? 2.2 :
        st === "listening" ? 1.6 :
        st === "thinking" ? 1.8 :
        st === "offline" ? 0.3 : 0.8;

      // Clear with dark trail
      ctx.fillStyle = "rgba(13,13,26,0.18)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (const r of runesRef.current) {
        // 2.5D: depth affects speed and size
        const depthFactor = 0.3 + r.z * 0.7;

        r.x += r.vx * speedMul * depthFactor * dt * 60;
        r.y += r.vy * speedMul * depthFactor * dt * 60;
        r.rotation += r.rotSpeed * speedMul * dt;

        // Wrap around edges
        if (r.x < -60) r.x = canvas.width + 40;
        if (r.x > canvas.width + 60) r.x = -40;
        if (r.y < -60) r.y = canvas.height + 40;
        if (r.y > canvas.height + 60) r.y = -40;

        // Pulse alpha
        r.alpha = lerp(r.alpha, r.glowing ? 0.9 : 0.12, 0.04);
        if (Math.random() < 0.002) r.glowing = !r.glowing;

        const s = r.size * (0.5 + r.z * 0.8); // smaller = further back

        ctx.save();
        ctx.translate(r.x, r.y);
        ctx.rotate(r.rotation);

        // Gold glow for close runes
        if (r.z > 0.65 && r.glowing) {
          ctx.shadowColor = "#c4a45a";
          ctx.shadowBlur = 18 + Math.sin(now * 0.003) * 6;
        } else if (r.z > 0.4) {
          ctx.shadowColor = "#7a5fcf";
          ctx.shadowBlur = 8;
        } else {
          ctx.shadowBlur = 0;
        }

        const colorR = r.z > 0.65 ? "#c4a45a" : r.z > 0.35 ? "#8b6fd4" : "#3d3d7a";
        ctx.fillStyle = colorR;
        ctx.globalAlpha = r.alpha * depthFactor;
        ctx.font = `${s}px serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(r.char, 0, 0);
        ctx.restore();
      }

      rafRef.current = requestAnimationFrame(tick);
    };

    rafRef.current = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(rafRef.current);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 0 }}
    />
  );
}

function spawnRune(canvas: HTMLCanvasElement): Rune {
  const angle = Math.random() * Math.PI * 2;
  const speed = 0.15 + Math.random() * 0.4;
  return {
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    z: Math.random(), // 0 = far, 1 = close
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed,
    char: RUNE_CHARS[Math.floor(Math.random() * RUNE_CHARS.length)],
    alpha: Math.random() * 0.3,
    size: 12 + Math.random() * 22,
    rotation: Math.random() * Math.PI * 2,
    rotSpeed: (Math.random() - 0.5) * 0.015,
    glowing: Math.random() < 0.2,
  };
}
