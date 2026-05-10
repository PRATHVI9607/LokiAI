"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { WifiOff, ChevronDown } from "lucide-react";
import StatusOrb from "./StatusOrb";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";
import PersonalityPicker from "./PersonalityPicker";
import { type ChatMessage, type Status, type Personality, type FileEntry } from "@/hooks/useLoki";

const PERSONALITY_LABELS: Record<Personality, string> = {
  loki: "LOKI",
  jarvis: "JARVIS",
  friday: "FRIDAY",
};

const PERSONALITY_COLORS: Record<Personality, string> = {
  loki: "#c4a45a",
  jarvis: "#8be9fd",
  friday: "#50fa7b",
};

interface ChatPanelProps {
  messages: ChatMessage[];
  status: Status;
  transcript: string;
  isMuted: boolean;
  personality: Personality;
  indexedFiles: FileEntry[];
  ragAvailable: boolean;
  onSend: (text: string) => void;
  onToggleMute: () => void;
  onUndo: () => void;
  onClear: () => void;
  onFilePanel: () => void;
  onPersonalityChange: (mode: Personality) => Promise<void>;
}

export default function ChatPanel({
  messages, status, transcript, isMuted, personality,
  indexedFiles, ragAvailable,
  onSend, onToggleMute, onUndo, onClear, onFilePanel, onPersonalityChange,
}: ChatPanelProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [showPersonality, setShowPersonality] = useState(false);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  const isOffline = status === "offline";
  const pColor = PERSONALITY_COLORS[personality];

  return (
    <motion.div
      className="glass-strong rounded-2xl flex flex-col overflow-hidden shadow-2xl relative"
      style={{
        width: 440, height: 640,
        boxShadow: `0 0 60px rgba(196,164,90,0.08), 0 25px 60px rgba(0,0,0,0.6), 0 0 1px ${pColor}22`,
      }}
      initial={{ opacity: 0, scale: 0.92, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between px-5 py-4 border-b border-loki-purple/40"
        style={{ background: "linear-gradient(180deg, rgba(42,42,90,0.5) 0%, transparent 100%)" }}
      >
        <div className="flex flex-col">
          <h1 className="gold-text text-xl font-bold tracking-wide">LOKI</h1>
          {/* Personality badge */}
          <button
            className="flex items-center gap-1 mt-0.5 group"
            onClick={() => setShowPersonality((v) => !v)}
          >
            <div className="w-1.5 h-1.5 rounded-full" style={{ background: pColor }} />
            <span className="text-xs tracking-widest" style={{ color: pColor }}>
              {PERSONALITY_LABELS[personality]}
            </span>
            <ChevronDown
              size={10}
              className="text-loki-muted group-hover:text-loki-text transition-colors"
              style={{ transform: showPersonality ? "rotate(180deg)" : "rotate(0)", transition: "transform 0.2s" }}
            />
          </button>
        </div>

        <div className="flex items-center gap-3">
          <AnimatePresence>
            {isOffline && (
              <motion.div
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0 }}
                className="flex items-center gap-1 text-loki-error text-xs"
              >
                <WifiOff size={12} />
                <span>Offline</span>
              </motion.div>
            )}
            {indexedFiles.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-xs px-2 py-0.5 rounded-full"
                style={{ background: `${pColor}22`, color: pColor, border: `1px solid ${pColor}44` }}
              >
                RAG: {indexedFiles.length}f
              </motion.div>
            )}
          </AnimatePresence>
          <StatusOrb status={status} />
        </div>
      </div>

      {/* Personality dropdown */}
      <AnimatePresence>
        {showPersonality && (
          <div className="absolute top-16 left-4 z-50">
            <PersonalityPicker
              current={personality}
              onChange={onPersonalityChange}
              onClose={() => setShowPersonality(false)}
            />
          </div>
        )}
      </AnimatePresence>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto py-4 flex flex-col gap-3 scroll-smooth"
        style={{ scrollbarWidth: "thin" }}
      >
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <MessageBubble key={msg.id} msg={msg} />
          ))}
        </AnimatePresence>

        {/* Thinking indicator */}
        <AnimatePresence>
          {status === "thinking" && (
            <motion.div
              className="flex items-center gap-2 px-4"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
            >
              <div
                className="w-7 h-7 rounded-full flex-shrink-0"
                style={{ background: "radial-gradient(circle at 35% 35%, #c4a45acc, #2a2a5a)", boxShadow: "0 0 10px #c4a45a44" }}
              />
              <div className="msg-bubble msg-loki flex items-center gap-1.5 py-3 px-4">
                <span className="typing-dot w-2 h-2 rounded-full bg-loki-gold inline-block" />
                <span className="typing-dot w-2 h-2 rounded-full bg-loki-gold inline-block" />
                <span className="typing-dot w-2 h-2 rounded-full bg-loki-gold inline-block" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Live transcript */}
        <AnimatePresence>
          {transcript && status === "listening" && (
            <motion.div className="px-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="text-xs text-loki-muted italic px-3 py-2 rounded-lg"
                style={{ background: "rgba(107,107,168,0.1)", border: "1px dashed rgba(107,107,168,0.3)" }}>
                🎙 {transcript}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Input */}
      <InputBar
        onSend={onSend}
        onToggleMute={onToggleMute}
        onUndo={onUndo}
        onClear={onClear}
        onFileClick={onFilePanel}
        isMuted={isMuted}
        status={status}
        filesCount={indexedFiles.length}
      />
    </motion.div>
  );
}
