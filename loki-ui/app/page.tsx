"use client";

import { useEffect, useRef, useState } from "react";
import dynamic from "next/dynamic";
import { AnimatePresence, motion } from "framer-motion";
import { useLoki } from "@/hooks/useLoki";
import ChatPanel from "@/components/ChatPanel";
import FilePanel from "@/components/FilePanel";

const VideoOrb = dynamic(() => import("@/components/VideoOrb"), { ssr: false });

export default function Home() {
  const {
    messages, status, transcript, isMuted, isVisible,
    personality, indexedFiles, ragAvailable,
    sendMessage, toggleMute, requestUndo, clearMessages,
    uploadFile, deleteFile, setPersonality,
  } = useLoki();

  const [showFiles, setShowFiles] = useState(false);
  const layerRef = useRef<HTMLDivElement>(null);

  // Set aria-hidden imperatively — JSX {expression} in ARIA attrs is flagged by axe
  useEffect(() => {
    layerRef.current?.setAttribute("aria-hidden", isVisible ? "false" : "true");
  }, [isVisible]);

  // Always render the shell — hiding the component entirely unmounts it, losing
  // WebSocket state and scroll position. When dormant, show an idle overlay instead.
  return (
    <div className="app-shell">
      {/* Living gold-sphere video background — reacts to voice state */}
      <div className="app-bg">
        <VideoOrb status={isVisible ? status : "offline"} />
      </div>

      {/* Depth vignette over canvas */}
      <div className="app-vignette" />

      {/* Corner Norse rune decorations */}
      <div className="rune-glow fixed top-6 left-8 text-5xl pointer-events-none select-none z-[2]" aria-hidden="true">ᚦ</div>
      <div className="rune-glow fixed bottom-8 right-10 text-4xl pointer-events-none select-none z-[2]" aria-hidden="true">ᛟ</div>
      <div className="rune-glow fixed top-12 right-12 text-3xl pointer-events-none select-none z-[2]" aria-hidden="true">ᚱ</div>
      <div className="rune-glow fixed bottom-16 left-12 text-3xl pointer-events-none select-none z-[2]" aria-hidden="true">ᛁ</div>

      {/* Dormant overlay — shown when Loki is in background/idle */}
      <AnimatePresence>
        {!isVisible && (
          <motion.div
            className="dormant-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4 }}
            aria-label="Loki is dormant — say Hey Loki to wake"
          >
            <div className="dormant-rune" aria-hidden="true">ᚠ</div>
            <p className="dormant-label">Dormant</p>
            <p className="dormant-hint">Say &ldquo;Hey Loki&rdquo; to wake</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Full-height UI layer — kept mounted, CSS class controls visibility */}
      <div
        ref={layerRef}
        className={`app-layer${isVisible ? "" : " app-layer--dormant"}`}
      >
        <AnimatePresence>
          {showFiles && (
            <FilePanel
              files={indexedFiles}
              ragAvailable={ragAvailable}
              onUpload={uploadFile}
              onDelete={deleteFile}
              onClose={() => setShowFiles(false)}
            />
          )}
        </AnimatePresence>

        <ChatPanel
          messages={messages}
          status={status}
          transcript={transcript}
          isMuted={isMuted}
          personality={personality}
          indexedFiles={indexedFiles}
          onSend={sendMessage}
          onToggleMute={toggleMute}
          onUndo={requestUndo}
          onClear={clearMessages}
          onFilePanel={() => setShowFiles((v) => !v)}
          onPersonalityChange={setPersonality}
        />
      </div>
    </div>
  );
}
