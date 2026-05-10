"use client";

import { useEffect, useRef, useCallback, useState } from "react";

export type MessageType = "loki_message" | "user_message" | "system_message";

export interface ChatMessage {
  id: string;
  type: MessageType;
  text: string;
  ts: number;
}

export type Status = "idle" | "listening" | "thinking" | "speaking" | "offline";

interface UseLokiReturn {
  messages: ChatMessage[];
  status: Status;
  transcript: string;
  isVisible: boolean;
  isMuted: boolean;
  sendMessage: (text: string) => void;
  toggleMute: () => void;
  requestUndo: () => void;
  clearMessages: () => void;
}

const WS_URL = "ws://localhost:7777/ws";
const RECONNECT_DELAY = 2000;

export function useLoki(): UseLokiReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<Status>("offline");
  const [transcript, setTranscript] = useState("");
  const [isVisible, setIsVisible] = useState(true);
  const [isMuted, setIsMuted] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const msgIdRef = useRef(0);

  const addMessage = useCallback((type: MessageType, text: string) => {
    const msg: ChatMessage = {
      id: `${++msgIdRef.current}`,
      type,
      text,
      ts: Date.now(),
    };
    setMessages((prev) => [...prev.slice(-200), msg]); // cap at 200 messages
  }, []);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      setStatus("idle");
    };

    ws.onclose = () => {
      setStatus("offline");
      wsRef.current = null;
      reconnectRef.current = setTimeout(connect, RECONNECT_DELAY);
    };

    ws.onerror = () => {
      ws.close();
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        switch (msg.type) {
          case "loki_message":
            addMessage("loki_message", msg.text);
            break;
          case "user_message":
            addMessage("user_message", msg.text);
            break;
          case "system_message":
            addMessage("system_message", msg.text);
            break;
          case "status":
            setStatus(msg.status as Status);
            break;
          case "transcript":
            setTranscript(msg.text);
            break;
          case "clear_transcript":
            setTranscript("");
            break;
          case "show":
            setIsVisible(true);
            break;
          case "hide":
            setIsVisible(false);
            break;
        }
      } catch {
        // ignore malformed
      }
    };
  }, [addMessage]);

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

  const sendMessage = useCallback(
    (text: string) => {
      send({ type: "user_message", text });
    },
    [send]
  );

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

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    status,
    transcript,
    isVisible,
    isMuted,
    sendMessage,
    toggleMute,
    requestUndo,
    clearMessages,
  };
}
