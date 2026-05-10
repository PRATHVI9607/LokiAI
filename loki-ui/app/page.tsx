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
    <main className="relative w-screen h-screen overflow-hidden flex items-center justify-center gap-4">
      {/* 2.5D Norse rune particle background */}
      <RuneCanvas status={status} />

      {/* Depth radial gradients — z-[1] keeps them above canvas but below content */}
      <div className="fixed inset-0 pointer-events-none bg-radial-purple z-[1]" />
      <div className="fixed inset-0 pointer-events-none bg-radial-gold z-[1]" />

      {/* File panel (left of chat) */}
      <div className="relative z-10">
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
      </div>

      {/* Main chat panel */}
      <div className="relative z-10">
        <ChatPanel
          messages={messages}
          status={status}
          transcript={transcript}
          isMuted={isMuted}
          personality={personality}
          indexedFiles={indexedFiles}
          ragAvailable={ragAvailable}
          onSend={sendMessage}
          onToggleMute={toggleMute}
          onUndo={requestUndo}
          onClear={clearMessages}
          onFilePanel={() => setShowFiles((v) => !v)}
          onPersonalityChange={setPersonality}
        />
      </div>

      {/* Corner Norse rune decorations */}
      <div className="fixed top-6 left-8 text-5xl rune-glow rune-corner-tl pointer-events-none select-none z-[2]">ᚦ</div>
      <div className="fixed bottom-8 right-10 text-4xl rune-glow rune-corner-br pointer-events-none select-none z-[2]">ᛟ</div>
      <div className="fixed top-12 right-12 text-3xl rune-glow rune-corner-tr pointer-events-none select-none z-[2]">ᚱ</div>
      <div className="fixed bottom-16 left-12 text-3xl rune-glow rune-corner-bl pointer-events-none select-none z-[2]">ᛁ</div>
    </main>
  );
}
