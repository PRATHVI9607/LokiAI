"use client";

import { useState, useRef, type KeyboardEvent } from "react";
import { Send, Mic, MicOff, RotateCcw, Trash2, Paperclip } from "lucide-react";
import { type Status } from "@/hooks/useLoki";

interface InputBarProps {
  onSend: (text: string) => void;
  onToggleMute: () => void;
  onUndo: () => void;
  onClear: () => void;
  onFileClick: () => void;
  isMuted: boolean;
  status: Status;
  filesCount: number;
}

export default function InputBar({
  onSend, onToggleMute, onUndo, onClear, onFileClick,
  isMuted, status, filesCount,
}: InputBarProps) {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const isOffline = status === "offline";
  const isListening = status === "listening";

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
      {/* Main input row */}
      <div className="input-row">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKey}
          placeholder={isOffline ? "Connecting to Loki…" : isListening ? "Listening… or type here" : "Speak or type…"}
          disabled={isOffline}
          aria-label="Message input"
          className="input-field"
        />
        <button
          type="button"
          onClick={submit}
          disabled={!value.trim() || isOffline}
          aria-label="Send message"
          className="send-btn"
        >
          <Send size={15} />
          Send
        </button>
      </div>

      {/* Action row */}
      <div className="action-row">
        <button
          type="button"
          onClick={onFileClick}
          aria-label="Toggle file panel"
          className={`action-btn ${filesCount > 0 ? "action-btn-gold" : ""}`}
        >
          <Paperclip size={12} />
          Files{filesCount > 0 ? ` · ${filesCount}` : ""}
        </button>

        <button
          type="button"
          onClick={onToggleMute}
          aria-label={isMuted ? "Unmute microphone" : "Mute microphone"}
          className={`action-btn ${isListening ? "action-btn-mic-live" : isMuted ? "action-btn-red" : ""}`}
        >
          {isMuted ? <MicOff size={12} /> : <Mic size={12} />}
          {isListening ? "Listening…" : isMuted ? "Muted" : "Mic"}
        </button>

        <button
          type="button"
          onClick={onUndo}
          aria-label="Undo last action"
          className="action-btn"
        >
          <RotateCcw size={12} />
          Undo
        </button>

        <button
          type="button"
          onClick={onClear}
          aria-label="Clear chat"
          className="action-btn action-btn-red ml-auto"
        >
          <Trash2 size={12} />
          Clear
        </button>
      </div>
    </div>
  );
}
