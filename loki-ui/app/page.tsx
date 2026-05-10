"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { AnimatePresence } from "framer-motion";
import { useLoki } from "@/hooks/useLoki";
import ChatPanel from "@/components/ChatPanel";
import FilePanel from "@/components/FilePanel";

const RuneCanvas = dynamic(() => import("@/components/RuneCanvas"), { ssr: false });

export default function Home() {
  const {
    messages, status, transcript, isMuted,
    personality, indexedFiles, ragAvailable,
    sendMessage, toggleMute, requestUndo, clearMessages,
    uploadFile, deleteFile, setPersonality,
  } = useLoki();

  const [showFiles, setShowFiles] = useState(false);

  return (
    <div className="app-shell">
      {/* Animated rune particle background */}
      <div className="app-bg">
        <RuneCanvas status={status} />
      </div>

      {/* Depth vignette over canvas */}
      <div className="app-vignette" />

      {/* Corner Norse rune decorations */}
      <div className="rune-glow fixed top-6 left-8 text-5xl pointer-events-none select-none z-[2]" aria-hidden="true">ᚦ</div>
      <div className="rune-glow fixed bottom-8 right-10 text-4xl pointer-events-none select-none z-[2]" aria-hidden="true">ᛟ</div>
      <div className="rune-glow fixed top-12 right-12 text-3xl pointer-events-none select-none z-[2]" aria-hidden="true">ᚱ</div>
      <div className="rune-glow fixed bottom-16 left-12 text-3xl pointer-events-none select-none z-[2]" aria-hidden="true">ᛁ</div>

      {/* Full-height UI layer: sidebar + chat */}
      <div className="app-layer">
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
