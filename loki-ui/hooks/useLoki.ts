"use client";

import { useEffect, useRef, useCallback, useState } from "react";

export type MessageType = "loki_message" | "user_message" | "system_message";

export interface ChatMessage {
  id: string;
  type: MessageType;
  text: string;
  ts: number;
  outcomeId?: string;          // backend outcome-log id — enables 👍/👎 on this turn
  feedback?: "up" | "down";    // local optimistic state once rated
  provider?: string;           // which engine answered (ollama/nvidia/openrouter/fast_path)
}

export interface ProviderStat { samples: number; avg_reward: number }
export interface LokiStats {
  outcomes: {
    total?: number;
    success_rate?: number;
    feedback?: { up: number; down: number; unrated: number };
    by_provider?: Record<string, { n: number; ok: number; avg_latency_ms: number; success_rate: number }>;
  };
  bandit: Record<string, ProviderStat>;
  last_provider: string;
}
export interface AuditEntry {
  ts: string; intent: string; tier: number; tier_label: string;
  success: boolean; result: string;
}

export type Status = "idle" | "listening" | "thinking" | "speaking" | "offline";
export type Personality = "loki" | "jarvis" | "friday";

export interface FileEntry {
  filename: string;
  chunkCount?: number;
}

interface UseLokiReturn {
  messages: ChatMessage[];
  status: Status;
  transcript: string;
  isVisible: boolean;
  isMuted: boolean;
  personality: Personality;
  indexedFiles: FileEntry[];
  ragAvailable: boolean;
  pendingConfirm: string | null;
  sendMessage: (text: string) => void;
  sendFeedback: (messageId: string, outcomeId: string, rating: "up" | "down") => void;
  stopSpeaking: () => void;
  answerConfirm: (yes: boolean) => void;
  fetchStats: () => Promise<LokiStats | null>;
  fetchAudit: (n?: number) => Promise<AuditEntry[]>;
  toggleMute: () => void;
  requestUndo: () => void;
  clearMessages: () => void;
  uploadFile: (file: File) => Promise<void>;
  deleteFile: (filename: string) => Promise<void>;
  setPersonality: (mode: Personality) => Promise<void>;
}

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "http://localhost:7777";
const WS_URL = API_BASE
  .replace(/^https:\/\//, "wss://")
  .replace(/^http:\/\//, "ws://")
  + "/ws";
const RECONNECT_DELAY = 2000;
const FILE_SIZE_LIMIT = 10 * 1024 * 1024; // 10 MB

async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeoutMs = 10_000
): Promise<Response> {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    return await fetch(url, { ...options, signal: ctrl.signal });
  } finally {
    clearTimeout(timer);
  }
}

export function useLoki(): UseLokiReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<Status>("offline");
  const [transcript, setTranscript] = useState("");
  const [isVisible, setIsVisible] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [personality, setPersonalityState] = useState<Personality>("loki");
  const [indexedFiles, setIndexedFiles] = useState<FileEntry[]>([]);
  const [ragAvailable, setRagAvailable] = useState(false);
  const [pendingConfirm, setPendingConfirm] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const msgIdRef = useRef(0);

  const addMessage = useCallback((type: MessageType, text: string, outcomeId?: string, provider?: string) => {
    const msg: ChatMessage = {
      id: `${++msgIdRef.current}`,
      type,
      text,
      ts: Date.now(),
      outcomeId,
      provider,
    };
    setMessages((prev) => [...prev.slice(-200), msg]);
  }, []);

  const refreshFiles = useCallback(async () => {
    try {
      const res = await fetchWithTimeout(`${API_BASE}/files`);
      if (!res.ok) return;
      const data = await res.json();
      setRagAvailable(data.available ?? false);
      if (Array.isArray(data.files)) {
        setIndexedFiles(data.files.map((f: string) => ({ filename: f })));
      }
    } catch {
      // backend not ready yet
    }
  }, []);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus("idle");
      refreshFiles();
    };

    ws.onclose = () => {
      setStatus("offline");
      wsRef.current = null;
      reconnectRef.current = setTimeout(connect, RECONNECT_DELAY);
    };

    ws.onerror = () => ws.close();

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        switch (msg.type) {
          case "loki_message":      addMessage("loki_message", msg.text, msg.outcome_id, msg.provider); break;
          case "user_message":      addMessage("user_message", msg.text); break;
          case "confirm":           setPendingConfirm(msg.text ?? "Confirm this action?"); break;
          case "system_message":    addMessage("system_message", msg.text); break;
          case "status":            setStatus(msg.status as Status); break;
          case "transcript":        setTranscript(msg.text); break;
          case "clear_transcript":  setTranscript(""); break;
          case "show":              setIsVisible(true); break;
          case "hide":              setIsVisible(false); break;
          case "personality_changed": setPersonalityState(msg.mode as Personality); break;
          case "file_indexed":
            setIndexedFiles((prev) => {
              const exists = prev.find((f) => f.filename === msg.filename);
              if (exists) return prev.map((f) => f.filename === msg.filename
                ? { ...f, chunkCount: msg.chunk_count } : f);
              return [...prev, { filename: msg.filename, chunkCount: msg.chunk_count }];
            });
            break;
        }
      } catch {
        // ignore malformed
      }
    };
  }, [addMessage, refreshFiles]);

  useEffect(() => {
    connect();
    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
      wsRef.current?.close();
    };
  }, [connect]);

  const send = useCallback((payload: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(payload));
    }
  }, []);

  const sendMessage = useCallback((text: string) => {
    send({ type: "user_message", text });
  }, [send]);

  const sendFeedback = useCallback((messageId: string, outcomeId: string, rating: "up" | "down") => {
    send({ type: "feedback", id: outcomeId, rating });
    // optimistic local state so the button reflects the choice immediately
    setMessages((prev) =>
      prev.map((m) => (m.id === messageId ? { ...m, feedback: rating } : m))
    );
  }, [send]);

  const stopSpeaking = useCallback(() => {
    send({ type: "stop_speaking" });
  }, [send]);

  const answerConfirm = useCallback((yes: boolean) => {
    setPendingConfirm(null);
    send({ type: "user_message", text: yes ? "yes" : "no" });
  }, [send]);

  const fetchStats = useCallback(async (): Promise<LokiStats | null> => {
    try {
      const res = await fetchWithTimeout(`${API_BASE}/stats`);
      if (!res.ok) return null;
      return (await res.json()) as LokiStats;
    } catch {
      return null;
    }
  }, []);

  const fetchAudit = useCallback(async (n = 25): Promise<AuditEntry[]> => {
    try {
      const res = await fetchWithTimeout(`${API_BASE}/audit?n=${n}`);
      if (!res.ok) return [];
      const data = await res.json();
      return Array.isArray(data.entries) ? data.entries : [];
    } catch {
      return [];
    }
  }, []);

  const toggleMute = useCallback(() => {
    setIsMuted((prev) => {
      const next = !prev;
      send({ type: "mute_toggle", muted: next });
      return next;
    });
  }, [send]);

  const requestUndo = useCallback(() => {
    send({ type: "undo" });
  }, [send]);

  const clearMessages = useCallback(() => setMessages([]), []);

  const uploadFile = useCallback(async (file: File) => {
    if (file.size > FILE_SIZE_LIMIT) {
      addMessage("system_message", `File too large: ${file.name} (max 10 MB)`);
      return;
    }
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await fetchWithTimeout(
        `${API_BASE}/upload`,
        { method: "POST", body: form },
        30_000
      );
      if (!res.ok) {
        const text = await res.text().catch(() => res.statusText);
        addMessage("system_message", `Upload failed: ${text}`);
        return;
      }
      const data = await res.json();
      if (!data.success) {
        addMessage("system_message", `Upload failed: ${data.message}`);
      } else {
        addMessage("system_message", data.message);
      }
    } catch {
      addMessage("system_message", "Upload failed — backend unreachable.");
    }
  }, [addMessage]);

  const deleteFile = useCallback(async (filename: string) => {
    try {
      const res = await fetchWithTimeout(
        `${API_BASE}/upload/${encodeURIComponent(filename)}`,
        { method: "DELETE" }
      );
      if (!res.ok) {
        addMessage("system_message", "Failed to remove file.");
        return;
      }
      setIndexedFiles((prev) => prev.filter((f) => f.filename !== filename));
      addMessage("system_message", `Removed: ${filename}`);
    } catch {
      addMessage("system_message", "Failed to remove file.");
    }
  }, [addMessage]);

  const setPersonality = useCallback(async (mode: Personality) => {
    const res = await fetchWithTimeout(`${API_BASE}/brain/personality`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error((body as { detail?: string }).detail ?? `HTTP ${res.status}`);
    }
    setPersonalityState(mode);
  }, [setPersonalityState]);

  return {
    messages, status, transcript, isVisible, isMuted,
    personality, indexedFiles, ragAvailable, pendingConfirm,
    sendMessage, sendFeedback, stopSpeaking, answerConfirm,
    fetchStats, fetchAudit,
    toggleMute, requestUndo, clearMessages,
    uploadFile, deleteFile, setPersonality,
  };
}
