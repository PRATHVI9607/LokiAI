"use client";

import dynamic from "next/dynamic";
import { useLoki } from "@/hooks/useLoki";
import ChatPanel from "@/components/ChatPanel";

// Canvas must be client-only (uses browser APIs)
const RuneCanvas = dynamic(() => import("@/components/RuneCanvas"), { ssr: false });

export default function Home() {
  const {
    messages,
    status,
    transcript,
    isMuted,
    sendMessage,
    toggleMute,
    requestUndo,
    clearMessages,
  } = useLoki();

  return (
    <main className="relative w-screen h-screen overflow-hidden flex items-center justify-center">
      {/* 2.5D Norse rune particle background */}
      <RuneCanvas status={status} />

      {/* Depth layers for 3D feel */}
      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse 80% 60% at 50% 50%, rgba(42,42,90,0.18) 0%, transparent 70%)",
          zIndex: 1,
        }}
      />
      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse 40% 40% at 50% 50%, rgba(196,164,90,0.06) 0%, transparent 60%)",
          zIndex: 1,
        }}
      />

      {/* Main chat panel */}
      <div className="relative" style={{ zIndex: 10 }}>
        <ChatPanel
          messages={messages}
          status={status}
          transcript={transcript}
          isMuted={isMuted}
          onSend={sendMessage}
          onToggleMute={toggleMute}
          onUndo={requestUndo}
          onClear={clearMessages}
        />
      </div>

      {/* Corner Norse rune decoration */}
      <div
        className="fixed top-6 left-8 text-5xl rune-glow pointer-events-none select-none"
        style={{ color: "rgba(196,164,90,0.15)", zIndex: 2, transform: "rotate(-15deg)" }}
      >
        ᚦ
      </div>
      <div
        className="fixed bottom-8 right-10 text-4xl rune-glow pointer-events-none select-none"
        style={{ color: "rgba(196,164,90,0.12)", zIndex: 2, transform: "rotate(20deg)" }}
      >
        ᛟ
      </div>
      <div
        className="fixed top-12 right-12 text-3xl rune-glow pointer-events-none select-none"
        style={{ color: "rgba(107,107,168,0.2)", zIndex: 2, transform: "rotate(10deg)" }}
      >
        ᚱ
      </div>
      <div
        className="fixed bottom-16 left-12 text-3xl rune-glow pointer-events-none select-none"
        style={{ color: "rgba(107,107,168,0.15)", zIndex: 2, transform: "rotate(-8deg)" }}
      >
        ᛁ
      </div>
    </main>
  );
}
