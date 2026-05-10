"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { type Status } from "@/hooks/useLoki";

const STATUS: Record<Status, { label: string; color: string; dotClass: string }> = {
  idle:      { label: "Idle",      color: "#64748B", dotClass: "" },
  listening: { label: "Listening", color: "#F5C518", dotClass: "status-dot-pulse" },
  thinking:  { label: "Thinking",  color: "#38BDF8", dotClass: "status-dot-spin" },
  speaking:  { label: "Speaking",  color: "#10D97E", dotClass: "status-dot-beat" },
  offline:   { label: "Offline",   color: "#F87171", dotClass: "" },
};

export default function StatusOrb({ status }: { status: Status }) {
  const cfg = STATUS[status];
  const pillRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    pillRef.current?.style.setProperty("--s-color", cfg.color);
  }, [cfg.color]);

  return (
    <div ref={pillRef} className="status-pill">
      <div className={`status-dot ${cfg.dotClass}`} />
      <AnimatePresence mode="wait">
        <motion.span
          key={status}
          className="status-label"
          initial={{ opacity: 0, y: 3 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -3 }}
          transition={{ duration: 0.18 }}
        >
          {cfg.label}
        </motion.span>
      </AnimatePresence>
    </div>
  );
}
