"use client";

import { useState, useRef, type KeyboardEvent } from "react";
import { motion } from "framer-motion";
import { Send, Mic, MicOff, RotateCcw, Trash2 } from "lucide-react";
import { type Status } from "@/hooks/useLoki";

interface InputBarProps {
  onSend: (text: string) => void;
  onToggleMute: () => void;
  onUndo: () => void;
  onClear: () => void;
  isMuted: boolean;
  status: Status;
}

export default function InputBar({
  onSend,
  onToggleMute,
  onUndo,
  onClear,
  isMuted,
  status,
}: InputBarProps) {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
    inputRef.current?.focus();
  };

  const onKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  const isOffline = status === "offline";

  return (
    <div className="px-4 py-3 border-t border-loki-purple/40 flex flex-col gap-2">
      {/* Text input row */}
      <div className="flex gap-2 items-center">
        <input
          ref={inputRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKey}
          placeholder={isOffline ? "Connecting to Loki…" : "Speak or type…"}
          disabled={isOffline}
          className="
            flex-1 bg-loki-purple/30 border border-loki-purple/50 rounded-xl
            px-4 py-2.5 text-sm text-loki-text placeholder-loki-muted
            focus:outline-none focus:border-loki-gold/60 focus:bg-loki-purple/50
            disabled:opacity-40 disabled:cursor-not-allowed
            transition-all duration-200
          "
        />
        <motion.button
          onClick={submit}
          disabled={!value.trim() || isOffline}
          whileTap={{ scale: 0.9 }}
          className="
            p-2.5 rounded-xl bg-loki-gold/20 border border-loki-gold/40
            text-loki-gold hover:bg-loki-gold/30 disabled:opacity-30
            disabled:cursor-not-allowed transition-all duration-200
          "
          title="Send"
        >
          <Send size={16} />
        </motion.button>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2 justify-end">
        <motion.button
          onClick={onToggleMute}
          whileTap={{ scale: 0.9 }}
          className={`
            flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium
            border transition-all duration-200
            ${isMuted
              ? "bg-loki-error/20 border-loki-error/40 text-loki-error"
              : "bg-loki-purple/40 border-loki-purple-light/50 text-loki-muted hover:text-loki-text"
            }
          `}
          title={isMuted ? "Unmute mic" : "Mute mic"}
        >
          {isMuted ? <MicOff size={13} /> : <Mic size={13} />}
          {isMuted ? "Muted" : "Mic"}
        </motion.button>

        <motion.button
          onClick={onUndo}
          whileTap={{ scale: 0.9 }}
          className="
            flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium
            bg-loki-purple/40 border border-loki-purple-light/50
            text-loki-muted hover:text-loki-text transition-all duration-200
          "
          title="Undo last action"
        >
          <RotateCcw size={13} />
          Undo
        </motion.button>

        <motion.button
          onClick={onClear}
          whileTap={{ scale: 0.9 }}
          className="
            flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium
            bg-loki-purple/40 border border-loki-purple-light/50
            text-loki-muted hover:text-loki-error hover:border-loki-error/40
            transition-all duration-200
          "
          title="Clear chat"
        >
          <Trash2 size={13} />
        </motion.button>
      </div>
    </div>
  );
}
