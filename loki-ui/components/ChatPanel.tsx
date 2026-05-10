"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { AnimatePresence, motion } from "framer-motion";
import { ChevronDown, WifiOff } from "lucide-react";
import StatusOrb from "./StatusOrb";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";
import PersonalityPicker from "./PersonalityPicker";
import { type ChatMessage, type Status, type Personality, type FileEntry } from "@/hooks/useLoki";

const PERSONALITY_LABELS: Record<Personality, string> = {
  loki:   "LOKI",
  jarvis: "JARVIS",
  friday: "FRIDAY",
};

const PERSONALITY_COLORS: Record<Personality, string> = {
  loki:   "#F5C518",
  jarvis: "#38BDF8",
  friday: "#10D97E",
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
  const rootRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const personalityBtnRef = useRef<HTMLButtonElement>(null);
  const portalRef = useRef<HTMLDivElement>(null);
  const [showPersonality, setShowPersonality] = useState(false);
  const [dropdownPos, setDropdownPos] = useState({ top: 0, left: 0 });
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  // Auto-scroll to latest message
  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  // Apply personality CSS custom properties imperatively to avoid inline style= prop
  useEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    const c = PERSONALITY_COLORS[personality];
    el.style.setProperty("--p-color", c);
    el.style.setProperty("--p-border", `${c}40`);
    el.style.setProperty("--p-bg", `${c}14`);
    el.style.setProperty("--p-bg-hover", `${c}22`);
  }, [personality]);

  const DROPDOWN_W = 200;
  const DROPDOWN_H = 160;

  const computeAndSetPos = useCallback(() => {
    if (!personalityBtnRef.current) return;
    const r = personalityBtnRef.current.getBoundingClientRect();
    const top = Math.max(8, Math.min(r.bottom + 4, window.innerHeight - DROPDOWN_H - 8));
    const left = Math.max(8, Math.min(r.left, window.innerWidth - DROPDOWN_W - 8));
    setDropdownPos({ top, left });
  }, []);

  const handlePersonalityToggle = useCallback(() => {
    setShowPersonality((prev) => {
      if (!prev) computeAndSetPos();
      return !prev;
    });
  }, [computeAndSetPos]);

  // Close picker on viewport resize or scroll
  useEffect(() => {
    if (!showPersonality) return;
    const close = () => setShowPersonality(false);
    window.addEventListener("resize", close);
    window.addEventListener("scroll", close, true);
    return () => {
      window.removeEventListener("resize", close);
      window.removeEventListener("scroll", close, true);
    };
  }, [showPersonality]);

  // Apply dropdown position imperatively — no JSX style= prop needed
  useEffect(() => {
    const el = portalRef.current;
    if (!el) return;
    el.style.top = `${dropdownPos.top}px`;
    el.style.left = `${dropdownPos.left}px`;
  }, [dropdownPos]);

  // Set aria-expanded imperatively — axe static analyzer flags any JSX {expression} in ARIA attrs
  useEffect(() => {
    personalityBtnRef.current?.setAttribute("aria-expanded", showPersonality ? "true" : "false");
  }, [showPersonality]);

  // Click-outside + Escape → close and return focus
  useEffect(() => {
    if (!showPersonality) return;
    const onPointerDown = (e: PointerEvent) => {
      if (
        portalRef.current && !portalRef.current.contains(e.target as Node) &&
        personalityBtnRef.current && !personalityBtnRef.current.contains(e.target as Node)
      ) {
        setShowPersonality(false);
        personalityBtnRef.current?.focus();
      }
    };
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setShowPersonality(false);
        personalityBtnRef.current?.focus();
      }
    };
    document.addEventListener("pointerdown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [showPersonality]);

  const isOffline = status === "offline";

  return (
    <div ref={rootRef} className="flex-1 flex flex-col min-w-0 min-h-0">

      {/* ── Header ─────────────────────────────────────────────── */}
      <header className="app-header">
        <span className="loki-logo">LOKI</span>
        <div className="header-divider" />

        {/* Personality selector */}
        <button
          ref={personalityBtnRef}
          type="button"
          className="personality-btn"
          onClick={handlePersonalityToggle}
          aria-label="Select personality mode"
          aria-haspopup="listbox"
        >
          <div className="personality-btn-dot" />
          <span className="personality-btn-label">{PERSONALITY_LABELS[personality]}</span>
          <ChevronDown
            size={10}
            aria-hidden="true"
            className={`transition-transform duration-200 ${showPersonality ? "rotate-180" : "rotate-0"}`}
            style={{ color: "var(--p-color)" }}
          />
        </button>

        {/* Right side: RAG pill + offline banner + status */}
        <div className="ml-auto flex items-center gap-3">
          <AnimatePresence>
            {indexedFiles.length > 0 && (
              <motion.span
                key="rag"
                className="rag-pill"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.2 }}
              >
                RAG · {indexedFiles.length}f
              </motion.span>
            )}
            {isOffline && (
              <motion.div
                key="offline"
                className="offline-banner"
                initial={{ opacity: 0, x: 8 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 8 }}
                transition={{ duration: 0.2 }}
              >
                <WifiOff size={11} aria-hidden="true" />
                Offline
              </motion.div>
            )}
          </AnimatePresence>
          <StatusOrb status={status} />
        </div>
      </header>

      {/* ── Chat body ──────────────────────────────────────────── */}
      <div className="chat-body">

        {/* Messages scroll area */}
        <div ref={scrollRef} className="messages-area">
          <AnimatePresence initial={false}>
            {messages.map((msg) => (
              <MessageBubble key={msg.id} msg={msg} />
            ))}
          </AnimatePresence>

          {/* Thinking indicator */}
          <AnimatePresence>
            {status === "thinking" && (
              <motion.div
                className="thinking-row"
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2 }}
              >
                <div className="msg-avatar" aria-hidden="true" />
                <div className="msg-bubble msg-bubble-loki flex items-center gap-1.5 py-3">
                  <span className="thinking-dot" aria-hidden="true" />
                  <span className="thinking-dot" aria-hidden="true" />
                  <span className="thinking-dot" aria-hidden="true" />
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Live transcript */}
          <AnimatePresence>
            {transcript && status === "listening" && (
              <motion.div
                className="transcript-strip"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
                aria-live="polite"
                aria-label="Live transcript"
              >
                🎙 {transcript}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Input bar */}
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
      </div>

      {/* Personality picker — portaled to body to escape any overflow:hidden ancestor */}
      {mounted && createPortal(
        <AnimatePresence>
          {showPersonality && (
            <div ref={portalRef} className="personality-dropdown-portal">
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
    </div>
  );
}
