"use client";

/**
 * VideoOrb — the living gold-sphere background (Google Flow / Veo footage).
 *
 * A looping, muted video of the sentient data-sphere fills the view. It stays
 * calm by default and subtly reacts to Loki's voice state via playback rate +
 * a warm gold scrim that breathes brighter when listening/thinking/speaking.
 */

import { useEffect, useRef } from "react";
import { type Status } from "@/hooks/useLoki";

const RATE: Record<Status, number> = {
  idle: 0.85, listening: 1.0, thinking: 1.45, speaking: 1.15, offline: 0.4,
};

export default function VideoOrb({ status }: { status: Status }) {
  const ref = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const v = ref.current;
    if (!v) return;
    // ease the playback rate toward the target so changes feel calm, not abrupt
    const target = RATE[status] ?? 0.85;
    let raf = 0;
    const tick = () => {
      v.playbackRate += (target - v.playbackRate) * 0.06;
      if (Math.abs(target - v.playbackRate) > 0.01) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [status]);

  return (
    <div className={`video-orb-wrap state-${status}`}>
      <video
        ref={ref}
        className="video-orb"
        autoPlay
        loop
        muted
        playsInline
        preload="auto"
        aria-hidden="true"
      >
        <source src="/videos/loki-orb-1.mp4" type="video/mp4" />
      </video>
      {/* warm gold scrim — breathes with state, keeps text readable */}
      <div className="video-scrim" />
    </div>
  );
}
