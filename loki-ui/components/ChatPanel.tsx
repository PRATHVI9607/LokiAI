"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
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
  onSend: (text: string) => void;
  onToggleMute: () => void;
  onUndo: () => void;
  onClear: () => void;
  onFilePanel: () => void;
  onPersonalityChange: (mode: Personality) => Promise<void>;
}

export default function ChatPanel({
  messages, status, transcript, isMuted, personality,
  indexedFiles,
  onSend, onToggleMute, onUndo, onClear, onFilePanel, onPersonalityChange,
}: ChatPanelProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const personalityBtnRef = useRef<HTMLButtonElement>(null);
  const [showPersonality, setShowPersonality] = useState(false);
  const [dropdownPos, setDropdownPos] = useState({ top: 0, left: 0 });
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  const handlePersonalityToggle = useCallback(() => {
    setShowPersonality((prev) => {
      if (!prev && personalityBtnRef.current) {
        const r = personalityBtnRef.current.getBoundingClientRect();
        setDropdownPos({ top: r.bottom + 4, left: r.left });
      }
      return !prev;
    });
  }, []);

  const pColor = PERSONALITY_COLORS[personality];

  // CSS custom properties drive all personality-color CSS classes.
  // This single style prop (CSS vars) is the accepted pattern for dynamic theming.
  const personalityVars = {
    "--p-color": pColor,
    "--p-glow": `${pColor}22`,
    "--p-mid": `${pColor}44`,
  } as React.CSSProperties;

  const isOffline = status === "offline";

  return (
    <motion.div
      className="chat-panel glass-strong rounded-2xl flex flex-col overflow-hidden relative"
      style={personalityVars}
      initial={{ opacity: 0, scale: 0.92, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Header */}
      <div className="chat-header-bg flex items-center justify-between px-5 py-4 border-b border-loki-purple/40">
        <div className="flex flex-col">
          <h1 className="gold-text text-xl font-bold tracking-wide">LOKI</h1>
          {/* Personality badge */}
          <button
            ref={personalityBtnRef}
            type="button"
            className="flex items-center gap-1 mt-0.5 group"
            onClick={handlePersonalityToggle}
            aria-expanded={showPersonality}
            aria-label="Select personality mode"
          >
            <div className="personality-dot w-1.5 h-1.5 rounded-full" />
            <span className="personality-label text-xs tracking-widest">
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
                className="rag-badge text-xs px-2 py-0.5 rounded-full"
              >
                RAG: {indexedFiles.length}f
              </motion.div>
            )}
          </AnimatePresence>
          <StatusOrb status={status} />
        </div>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto py-4 flex flex-col gap-3 scroll-smooth"
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
              <div className="thinking-avatar w-7 h-7 rounded-full flex-shrink-0" />
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
              <div className="transcript-preview text-xs text-loki-muted italic px-3 py-2 rounded-lg">
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

      {/* Personality picker — portal into document.body to escape overflow:hidden */}
      {mounted && createPortal(
        <AnimatePresence>
          {showPersonality && (
            <div
              className="personality-dropdown-portal"
              style={{ "--dt": `${dropdownPos.top}px`, "--dl": `${dropdownPos.left}px` } as React.CSSProperties}
            >
              <PersonalityPicker
                current={personality}
                onChange={onPersonalityChange}
                onClose={() => setShowPersonality(false)}
              />
            </div>
          )}
        </AnimatePresence>,
        document.body
      )}
    </motion.div>
  );
}
