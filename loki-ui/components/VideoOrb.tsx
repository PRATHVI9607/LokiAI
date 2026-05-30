"use client";

/**
 * VideoOrb — the living Yggdrasil background (Google Flow / Veo footage).
 *
 * Two calm bioluminescent World-Tree clips are stacked and gently cross-faded
 * on a slow loop, so the background breathes between scenes without ever being
 * busy. Reacts to Loki's voice state only subtly: a touch more life when
 * thinking/speaking, dimmed when offline. A soft green-blue scrim keeps the
 * centred chat readable.
 */

import { useEffect, useRef } from "react";
import { type Status } from "@/hooks/useLoki";

const RATE: Record<Status, number> = {
  idle: 0.8, listening: 0.95, thinking: 1.25, speaking: 1.05, offline: 0.4,
};

export default function VideoOrb({ status }: { status: Status }) {
  const aRef = useRef<HTMLVideoElement>(null);
  const bRef = useRef<HTMLVideoElement>(null);

  // ease both clips' playback rate toward the target — calm, never abrupt
  useEffect(() => {
    const target = RATE[status] ?? 0.8;
    let raf = 0;
    const tick = () => {
      let going = false;
      for (const v of [aRef.current, bRef.current]) {
        if (!v) continue;
        v.playbackRate += (target - v.playbackRate) * 0.05;
        if (Math.abs(target - v.playbackRate) > 0.01) going = true;
      }
      if (going) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [status]);

  return (
    <div className={`video-orb-wrap state-${status}`}>
      {/* base scene */}
      <video ref={aRef} className="video-orb video-a" autoPlay loop muted playsInline preload="auto" aria-hidden="true">
        <source src="/videos/yggdrasil-1.mp4" type="video/mp4" />
      </video>
      {/* second scene — opacity oscillates slowly to cross-fade between the two */}
      <video ref={bRef} className="video-orb video-b" autoPlay loop muted playsInline preload="auto" aria-hidden="true">
        <source src="/videos/yggdrasil-3.mp4" type="video/mp4" />
      </video>
      <div className="video-scrim" />
    </div>
  );
}
