"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Check } from "lucide-react";
import { type Personality } from "@/hooks/useLoki";

const MODES: { id: Personality; label: string; desc: string }[] = [
  { id: "loki",   label: "Loki",   desc: "Witty Norse trickster" },
  { id: "jarvis", label: "Jarvis", desc: "Formal & precise"       },
  { id: "friday", label: "Friday", desc: "Casual & collaborative" },
];

interface Props {
  current: Personality;
  onChange: (mode: Personality) => Promise<void>;
  onClose: () => void;
}

export default function PersonalityPicker({ current, onChange, onClose }: Props) {
  const [error, setError] = useState<string | null>(null);

  return (
    <motion.div
      className="personality-picker glass-strong rounded-xl overflow-hidden"
      initial={{ opacity: 0, y: -8, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -8, scale: 0.95 }}
      transition={{ duration: 0.2 }}
    >
      <div className="px-3 py-2 border-b border-loki-purple/40">
        <p className="text-xs text-loki-muted font-medium tracking-wider uppercase">Personality</p>
        {error && <p className="text-xs text-loki-error mt-1">{error}</p>}
      </div>
      {MODES.map((m) => (
        <button
          key={m.id}
          type="button"
          data-personality={m.id}
          aria-pressed={current === m.id ? "true" : "false"}
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
          className={`mode-btn w-full flex items-center gap-3 px-3 py-2.5 text-left hover:bg-loki-purple/30 transition-colors
            ${current === m.id ? "bg-loki-purple/40" : ""}`}
        >
          <div
            className={`mode-dot w-2 h-2 rounded-full flex-shrink-0 ${current === m.id ? "mode-dot-active" : ""}`}
          />
          <div>
            <p className="text-xs font-medium text-loki-text">{m.label}</p>
            <p className="text-xs text-loki-muted">{m.desc}</p>
          </div>
          {current === m.id && (
            <Check size={12} className="mode-check ml-auto flex-shrink-0" aria-hidden="true" />
          )}
        </button>
      ))}
    </motion.div>
  );
}
