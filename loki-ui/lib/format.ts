// Pure formatting helpers — kept framework-free so they're trivially unit-testable.

/** Human-friendly label for the LLM provider that answered a turn. */
export function providerLabel(p: string): string {
  if (!p) return "";
  if (p === "fast_path") return "instant";
  if (p === "ollama") return "local";
  if (p.startsWith("openrouter")) return "openrouter";
  return p;
}

/** Map a bandit avg-reward in [-0.5, 1.5] to a 2–100% bar width. */
export function rewardToPct(avgReward: number): number {
  return Math.max(2, Math.min(100, ((avgReward + 0.5) / 2) * 100));
}

/** Compact latency label: 840 → "840ms", 1840 → "1.8s". */
export function formatLatency(ms: number): string {
  if (!Number.isFinite(ms) || ms < 0) return "—";
  return ms < 1000 ? `${Math.round(ms)}ms` : `${(ms / 1000).toFixed(1)}s`;
}
