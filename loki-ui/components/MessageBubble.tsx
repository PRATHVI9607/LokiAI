"use client";

import { motion } from "framer-motion";
import { type ChatMessage } from "@/hooks/useLoki";

export default function MessageBubble({ msg }: { msg: ChatMessage }) {
  if (msg.type === "system_message") {
    return (
      <motion.div
        className="flex justify-center px-4"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.25 }}
      >
        <div className="msg-system px-4 py-2">{msg.text}</div>
      </motion.div>
    );
  }

  const isUser = msg.type === "user_message";

  return (
    <motion.div
      className={`flex ${isUser ? "justify-end" : "justify-start"} px-4`}
      initial={{ opacity: 0, x: isUser ? 20 : -20, y: 8 }}
      animate={{ opacity: 1, x: 0, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      {!isUser && (
        <div
          className="w-7 h-7 rounded-full flex-shrink-0 mr-2 mt-1"
          style={{
            background: "radial-gradient(circle at 35% 35%, #c4a45acc, #2a2a5a)",
            boxShadow: "0 0 10px #c4a45a44",
          }}
        />
      )}
      <div className={`msg-bubble ${isUser ? "msg-user" : "msg-loki"}`}>
        {msg.text}
      </div>
    </motion.div>
  );
}
