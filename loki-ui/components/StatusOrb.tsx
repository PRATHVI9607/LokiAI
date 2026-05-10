"use client";

import { motion, AnimatePresence } from "framer-motion";
import { type Status } from "@/hooks/useLoki";

const STATUS_CONFIG: Record<Status, { label: string; color: string; ring: string; anim: string }> = {
  idle:      { label: "Idle",      color: "#6b6ba8", ring: "#6b6ba8", anim: "animate-orb-idle" },
  listening: { label: "Listening", color: "#c4a45a", ring: "#c4a45a", anim: "animate-orb-listen" },
  thinking:  { label: "Thinking",  color: "#8be9fd", ring: "#8be9fd", anim: "animate-orb-think" },
  speaking:  { label: "Speaking",  color: "#50fa7b", ring: "#50fa7b", anim: "animate-orb-speak" },
  offline:   { label: "Offline",   color: "#ff5555", ring: "#ff5555", anim: "" },
};

export default function StatusOrb({ status }: { status: Status }) {
  const cfg = STATUS_CONFIG[status];

  return (
    <div className="flex flex-col items-center gap-2">
      {/* 3D-ish orb */}
      <div className="relative w-20 h-20">
        {/* Outer ring pulse */}
        <motion.div
          className="absolute inset-0 rounded-full"
          style={{ border: `2px solid ${cfg.ring}` }}
          animate={{ scale: [1, 1.25, 1], opacity: [0.6, 0, 0.6] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        />

        {/* Core orb */}
        <motion.div
          className={`absolute inset-2 rounded-full ${cfg.anim}`}
          style={{
            background: `radial-gradient(circle at 35% 35%, ${cfg.color}cc, ${cfg.color}33 60%, #0d0d1a)`,
            boxShadow: `0 0 24px ${cfg.color}66, 0 0 48px ${cfg.color}22, inset 0 0 16px ${cfg.color}22`,
          }}
          key={status}
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.3 }}
        />

        {/* Highlight spec */}
        <div
          className="absolute rounded-full"
          style={{
            width: 10, height: 10,
            top: 14, left: 18,
            background: "rgba(255,255,255,0.35)",
            filter: "blur(2px)",
          }}
        />
      </div>

      {/* Status label */}
      <AnimatePresence mode="wait">
        <motion.span
          key={status}
          className="text-xs font-medium tracking-widest uppercase"
          style={{ color: cfg.color }}
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -4 }}
          transition={{ duration: 0.2 }}
        >
          {cfg.label}
        </motion.span>
      </AnimatePresence>
    </div>
  );
}
