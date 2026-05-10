"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Wifi, WifiOff } from "lucide-react";
import StatusOrb from "./StatusOrb";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";
import { type ChatMessage, type Status } from "@/hooks/useLoki";

interface ChatPanelProps {
  messages: ChatMessage[];
  status: Status;
  transcript: string;
  isMuted: boolean;
  onSend: (text: string) => void;
  onToggleMute: () => void;
  onUndo: () => void;
  onClear: () => void;
}

export default function ChatPanel({
  messages,
  status,
  transcript,
  isMuted,
  onSend,
  onToggleMute,
  onUndo,
  onClear,
}: ChatPanelProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new message
  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  const isOffline = status === "offline";

  return (
    <motion.div
      className="glass-strong rounded-2xl flex flex-col overflow-hidden shadow-2xl"
      style={{
        width: 440,
        height: 640,
        boxShadow: "0 0 60px rgba(196,164,90,0.08), 0 25px 60px rgba(0,0,0,0.6)",
      }}
      initial={{ opacity: 0, scale: 0.92, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between px-5 py-4 border-b border-loki-purple/40"
        style={{
          background: "linear-gradient(180deg, rgba(42,42,90,0.5) 0%, transparent 100%)",
        }}
      >
        <div className="flex flex-col">
          <h1 className="gold-text text-xl font-bold tracking-wide">LOKI</h1>
          <p className="text-loki-muted text-xs tracking-widest">NORSE AI ASSISTANT</p>
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
          </AnimatePresence>
          <StatusOrb status={status} />
        </div>
      </div>

      {/* Chat messages */}
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
                style={{
                  background: "radial-gradient(circle at 35% 35%, #c4a45acc, #2a2a5a)",
                  boxShadow: "0 0 10px #c4a45a44",
                }}
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
            <motion.div
              className="px-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div
                className="text-xs text-loki-muted italic px-3 py-2 rounded-lg"
                style={{ background: "rgba(107,107,168,0.1)", border: "1px dashed rgba(107,107,168,0.3)" }}
              >
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
        isMuted={isMuted}
        status={status}
      />
    </motion.div>
  );
}
