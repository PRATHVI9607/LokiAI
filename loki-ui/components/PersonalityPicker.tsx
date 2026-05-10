"use client";

import { motion } from "framer-motion";
import { type Personality } from "@/hooks/useLoki";

const MODES: { id: Personality; label: string; desc: string; color: string }[] = [
  { id: "loki",   label: "Loki",   desc: "Witty Norse trickster", color: "#c4a45a" },
  { id: "jarvis", label: "Jarvis", desc: "Formal & precise",       color: "#8be9fd" },
  { id: "friday", label: "Friday", desc: "Casual & collaborative", color: "#50fa7b" },
];

interface Props {
  current: Personality;
  onChange: (mode: Personality) => Promise<void>;
  onClose: () => void;
}

export default function PersonalityPicker({ current, onChange, onClose }: Props) {
  return (
    <motion.div
      className="glass-strong rounded-xl overflow-hidden"
      style={{ width: 220 }}
      initial={{ opacity: 0, y: -8, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -8, scale: 0.95 }}
      transition={{ duration: 0.2 }}
    >
      <div className="px-3 py-2 border-b border-loki-purple/40">
        <p className="text-xs text-loki-muted font-medium tracking-wider uppercase">Personality</p>
      </div>
      {MODES.map((m) => (
        <button
          key={m.id}
          onClick={() => { onChange(m.id); onClose(); }}
          className={`w-full flex items-center gap-3 px-3 py-2.5 text-left hover:bg-loki-purple/30 transition-colors
            ${current === m.id ? "bg-loki-purple/40" : ""}`}
        >
          <div
            className="w-2 h-2 rounded-full flex-shrink-0"
            style={{ background: m.color, boxShadow: current === m.id ? `0 0 8px ${m.color}` : "none" }}
          />
          <div>
            <p className="text-xs font-medium text-loki-text">{m.label}</p>
            <p className="text-xs text-loki-muted">{m.desc}</p>
          </div>
          {current === m.id && (
            <div className="ml-auto w-1.5 h-1.5 rounded-full" style={{ background: m.color }} />
          )}
        </button>
      ))}
    </motion.div>
  );
}
