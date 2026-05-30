"use client";

import { useState, useRef, type KeyboardEvent } from "react";
import { ArrowUp, Mic, MicOff, RotateCcw, Trash2, Paperclip, Square, BarChart3 } from "lucide-react";
import { type Status } from "@/hooks/useLoki";

interface InputBarProps {
  onSend: (text: string) => void;
  onToggleMute: () => void;
  onUndo: () => void;
  onClear: () => void;
  onFileClick: () => void;
  onStopSpeaking: () => void;
  onInsights: () => void;
  isMuted: boolean;
  status: Status;
  filesCount: number;
}

// thin precise lines (skill: no thick lucide)
const ICON = { strokeWidth: 1.5 };

export default function InputBar({
  onSend, onToggleMute, onUndo, onClear, onFileClick, onStopSpeaking, onInsights,
  isMuted, status, filesCount,
}: InputBarProps) {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const isOffline = status === "offline";
  const isListening = status === "listening";
  const isSpeaking = status === "speaking";

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
    inputRef.current?.focus();
  };

  const onKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(); }
  };

  return (
    <div className="input-bar">
      {/* Double-Bezel island: outer shell + inner core */}
      <div className="composer-shell">
        <div className="composer-core">
          <input
            ref={inputRef}
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={onKey}
            placeholder={isOffline ? "Connecting to Loki…" : isListening ? "Listening…" : "Message Loki…"}
            disabled={isOffline}
            aria-label="Message input"
            className="composer-input"
          />
          <button
            type="button"
            onClick={submit}
            disabled={!value.trim() || isOffline}
            aria-label="Send message"
            className="composer-send group"
          >
            <ArrowUp size={17} {...ICON} className="transition-transform duration-500 ease-[cubic-bezier(0.32,0.72,0,1)] group-hover:-translate-y-[2px]" />
          </button>
        </div>
      </div>

      {/* Action rail — thin ghost pills */}
      <div className="action-row">
        <button type="button" onClick={onFileClick} aria-label="Toggle file panel"
          className={`pill ${filesCount > 0 ? "pill-active" : ""}`}>
          <Paperclip size={13} {...ICON} />
          <span>Files{filesCount > 0 ? ` · ${filesCount}` : ""}</span>
        </button>

        <button type="button" onClick={onToggleMute}
          aria-label={isMuted ? "Unmute microphone" : "Mute microphone"}
          className={`pill ${isListening ? "pill-live" : isMuted ? "pill-danger" : ""}`}>
          {isMuted ? <MicOff size={13} {...ICON} /> : <Mic size={13} {...ICON} />}
          <span>{isListening ? "Listening" : isMuted ? "Muted" : "Voice"}</span>
        </button>

        <button type="button" onClick={onUndo} aria-label="Undo last action" className="pill">
          <RotateCcw size={13} {...ICON} />
          <span>Undo</span>
        </button>

        {isSpeaking && (
          <button type="button" onClick={onStopSpeaking} aria-label="Stop speaking"
            className="pill pill-stop">
            <Square size={12} {...ICON} />
            <span>Stop</span>
          </button>
        )}

        <button type="button" onClick={onInsights} aria-label="Open insights"
          className={`pill ${isSpeaking ? "" : "ml-auto"}`}>
          <BarChart3 size={13} {...ICON} />
          <span>Insights</span>
        </button>

        <button type="button" onClick={onClear} aria-label="Clear chat" className="pill pill-danger">
          <Trash2 size={13} {...ICON} />
          <span>Clear</span>
        </button>
      </div>
    </div>
  );
}
