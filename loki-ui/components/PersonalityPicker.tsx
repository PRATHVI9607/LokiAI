"use client";

import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { Check } from "lucide-react";
import { type Personality } from "@/hooks/useLoki";

const MODES: { id: Personality; label: string; desc: string }[] = [
  { id: "loki",   label: "Loki",   desc: "Witty Norse trickster" },
  { id: "jarvis", label: "Jarvis", desc: "Formal & precise" },
  { id: "friday", label: "Friday", desc: "Casual & collaborative" },
];

interface Props {
  current: Personality;
  onChange: (mode: Personality) => Promise<void>;
  onClose: () => void;
}

export default function PersonalityPicker({ current, onChange, onClose }: Props) {
  const [error, setError] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Set aria-pressed imperatively — axe static analyzer flags any JSX {expression} in ARIA attrs
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    MODES.forEach((m) => {
      const btn = el.querySelector<HTMLButtonElement>(`[data-personality="${m.id}"]`);
      btn?.setAttribute("aria-pressed", m.id === current ? "true" : "false");
    });
  }, [current]);

  return (
    <motion.div
      ref={containerRef}
      className="personality-picker"
      initial={{ opacity: 0, y: -8, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -8, scale: 0.95 }}
      transition={{ duration: 0.18 }}
    >
      <div className="picker-header">
        <p className="text-xs font-semibold tracking-widest uppercase text-loki-dim">Personality</p>
        {error && <p className="picker-error">{error}</p>}
      </div>

      {MODES.map((m) => (
        <button
          key={m.id}
          type="button"
          data-personality={m.id}
          aria-label={`${m.label}: ${m.desc}`}
          onClick={async () => {
            setError(null);
            try {
              await onChange(m.id);
              onClose();
            } catch (err) {
              setError(err instanceof Error ? err.message : "Failed to change personality");
            }
          }}
          className={`mode-btn w-full flex items-center gap-3 px-3 py-2.5 text-left ${current === m.id ? "mode-btn-active" : ""}`}
        >
          <div className={`w-2 h-2 rounded-full flex-shrink-0 mode-dot ${current === m.id ? "mode-dot-active" : ""}`} />
          <div className="flex-1 min-w-0">
            <p className={`mode-label ${current === m.id ? "mode-label-active" : ""}`}>{m.label}</p>
            <p className="text-xs text-loki-dim">{m.desc}</p>
          </div>
          {current === m.id && <Check size={12} aria-hidden="true" className="flex-shrink-0 mode-check" />}
        </button>
      ))}
    </motion.div>
  );
}
