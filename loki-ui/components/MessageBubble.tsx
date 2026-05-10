"use client";

import { motion } from "framer-motion";
import { type ChatMessage } from "@/hooks/useLoki";

export default function MessageBubble({ msg }: { msg: ChatMessage }) {
  if (msg.type === "system_message") {
    return (
      <motion.div
        className="msg-row msg-row-system"
        initial={{ opacity: 0, scale: 0.92 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.2 }}
      >
        <span className="msg-system">{msg.text}</span>
      </motion.div>
    );
  }

  const isUser = msg.type === "user_message";

  return (
    <motion.div
      className={`msg-row ${isUser ? "msg-row-user" : "msg-row-loki"}`}
      initial={{ opacity: 0, x: isUser ? 16 : -16, y: 6 }}
      animate={{ opacity: 1, x: 0, y: 0 }}
      transition={{ duration: 0.28, ease: "easeOut" }}
    >
      {!isUser && <div className="msg-avatar" aria-hidden="true" />}
      <div className={`msg-bubble ${isUser ? "msg-bubble-user" : "msg-bubble-loki"}`}>
        {msg.text}
      </div>
    </motion.div>
  );
}
