"use client";

import { useMemo } from "react";
import { motion } from "framer-motion";
import { ThumbsUp, ThumbsDown } from "lucide-react";
import { type ChatMessage } from "@/hooks/useLoki";
import { providerLabel } from "@/lib/format";

// Lightweight inline markdown renderer — bold, italic, inline code, links
function inlineRender(text: string): React.ReactNode {
  const parts: React.ReactNode[] = [];
  const re = /(\*\*(.+?)\*\*|\*(.+?)\*|`([^`]+)`|\[([^\]]+)\]\(([^)]+)\))/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) parts.push(text.slice(last, m.index));
    if (m[2])      parts.push(<strong key={m.index}>{m[2]}</strong>);
    else if (m[3]) parts.push(<em key={m.index}>{m[3]}</em>);
    else if (m[4]) parts.push(<code key={m.index} className="msg-inline-code">{m[4]}</code>);
    else if (m[5] && m[6])
      parts.push(<a key={m.index} href={m[6]} target="_blank" rel="noopener noreferrer" className="msg-link">{m[5]}</a>);
    last = m.index + m[0].length;
  }
  if (last < text.length) parts.push(text.slice(last));
  return <>{parts}</>;
}

// Block-level markdown: fenced code, bullet/numbered lists, paragraphs
function renderMarkdown(text: string): React.ReactNode {
  const lines = text.split("\n");
  const nodes: React.ReactNode[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Fenced code block
    if (line.startsWith("```")) {
      const lang = line.slice(3).trim();
      const codeLines: string[] = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      nodes.push(
        <pre key={`code-${i}`} className="msg-code-block">
          {lang && <span className="msg-code-lang">{lang}</span>}
          <code>{codeLines.join("\n")}</code>
        </pre>
      );
      i++;
      continue;
    }

    // Unordered list
    if (/^[-*•]\s/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^[-*•]\s/.test(lines[i])) {
        items.push(lines[i].replace(/^[-*•]\s/, ""));
        i++;
      }
      nodes.push(
        <ul key={`ul-${i}`} className="msg-list">
          {items.map((item, j) => <li key={j}>{inlineRender(item)}</li>)}
        </ul>
      );
      continue;
    }

    // Ordered list
    if (/^\d+\.\s/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\.\s/, ""));
        i++;
      }
      nodes.push(
        <ol key={`ol-${i}`} className="msg-list">
          {items.map((item, j) => <li key={j}>{inlineRender(item)}</li>)}
        </ol>
      );
      continue;
    }

    // Empty line → spacer
    if (!line.trim()) {
      nodes.push(<div key={`sp-${i}`} className="msg-spacer" />);
      i++;
      continue;
    }

    // Normal line
    nodes.push(<p key={`p-${i}`} className="msg-para">{inlineRender(line)}</p>);
    i++;
  }

  return <>{nodes}</>;
}

interface MessageBubbleProps {
  msg: ChatMessage;
  onFeedback?: (messageId: string, outcomeId: string, rating: "up" | "down") => void;
}

export default function MessageBubble({ msg, onFeedback }: MessageBubbleProps) {
  // Hooks must run unconditionally on every render — keep this ABOVE any early
  // return, or React crashes with a hook-count mismatch (client-side exception).
  const isUser = msg.type === "user_message";
  const rendered = useMemo(() => renderMarkdown(msg.text), [msg.text]);
  const canRate = !isUser && msg.type === "loki_message" && !!msg.outcomeId && !!onFeedback;

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

  // Premium stacked layout — Double-Bezel card for Loki, ghost block for user.
  return (
    <motion.div
      className={`msg-block ${isUser ? "msg-block-user" : "msg-block-loki"}`}
      initial={{ opacity: 0, y: 18, filter: "blur(6px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      transition={{ duration: 0.7, ease: [0.32, 0.72, 0, 1] }}
    >
      <div className="msg-head">
        <span className={`msg-dot ${isUser ? "is-user" : "is-loki"}`} aria-hidden="true" />
        <span className="msg-sender">{isUser ? "You" : "Loki"}</span>
        {!isUser && msg.provider && msg.provider !== "none" && (
          <span className="msg-provider" title="Which engine answered">
            {providerLabel(msg.provider)}
          </span>
        )}
      </div>
      <div className="msg-content">
        {isUser ? <p className="msg-para">{msg.text}</p> : rendered}
      </div>

      {canRate && (
        <div className="msg-feedback" aria-label="Rate this response">
          <button
            type="button"
            className={`msg-fb-btn ${msg.feedback === "up" ? "is-active-up" : ""}`}
            aria-label="Good response"
            disabled={!!msg.feedback}
            onClick={() => onFeedback!(msg.id, msg.outcomeId!, "up")}
          >
            <ThumbsUp size={13} aria-hidden="true" />
          </button>
          <button
            type="button"
            className={`msg-fb-btn ${msg.feedback === "down" ? "is-active-down" : ""}`}
            aria-label="Bad response"
            disabled={!!msg.feedback}
            onClick={() => onFeedback!(msg.id, msg.outcomeId!, "down")}
          >
            <ThumbsDown size={13} aria-hidden="true" />
          </button>
        </div>
      )}
    </motion.div>
  );
}
