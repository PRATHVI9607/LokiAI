"use client";

import { useCallback, useEffect, useState } from "react";
import { motion } from "framer-motion";
import { X, Activity, RotateCcw, Brain, ThumbsUp, ThumbsDown } from "lucide-react";
import { type LokiStats, type AuditEntry } from "@/hooks/useLoki";
import { rewardToPct } from "@/lib/format";

interface InsightsPanelProps {
  fetchStats: () => Promise<LokiStats | null>;
  fetchAudit: (n?: number) => Promise<AuditEntry[]>;
  onUndo: () => void;
  onClose: () => void;
}

const TIER_COLOR: Record<number, string> = { 1: "#6b7280", 2: "#5EC8F0", 3: "#ff6b6b" };

export default function InsightsPanel({ fetchStats, fetchAudit, onUndo, onClose }: InsightsPanelProps) {
  const [stats, setStats] = useState<LokiStats | null>(null);
  const [audit, setAudit] = useState<AuditEntry[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    const [s, a] = await Promise.all([fetchStats(), fetchAudit(25)]);
    setStats(s);
    setAudit(a);
    setLoading(false);
  }, [fetchStats, fetchAudit]);

  useEffect(() => { refresh(); }, [refresh]);

  const out = stats?.outcomes ?? {};
  const fb = out.feedback ?? { up: 0, down: 0, unrated: 0 };
  const bandit = stats?.bandit ?? {};
  const banditRows = Object.entries(bandit).sort((a, b) => b[1].avg_reward - a[1].avg_reward);

  return (
    <motion.div
      className="file-sidebar"
      initial={{ opacity: 0, x: -24 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -24 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
    >
      <div className="sidebar-header">
        <div className="flex items-center gap-2">
          <Activity size={14} className="text-loki-gold" />
          <span className="text-sm font-semibold text-loki-text">Insights</span>
        </div>
        <div className="flex items-center gap-1">
          <button type="button" onClick={refresh} aria-label="Refresh insights"
            className="text-loki-dim hover:text-loki-text transition-colors p-1 rounded">
            <RotateCcw size={13} />
          </button>
          <button type="button" onClick={onClose} aria-label="Close insights"
            className="text-loki-dim hover:text-loki-text transition-colors p-1 rounded">
            <X size={15} />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-3 py-3 space-y-5">
        {loading && <p className="text-xs text-loki-dim text-center py-6">Loading…</p>}

        {!loading && (
          <>
            {/* ── Learning summary ─────────────────────────── */}
            <section>
              <h3 className="insights-h">
                <Brain size={12} className="text-loki-gold" /> Learning
              </h3>
              <div className="insights-grid">
                <div className="insights-stat">
                  <span className="insights-stat-n">{out.total ?? 0}</span>
                  <span className="insights-stat-l">interactions</span>
                </div>
                <div className="insights-stat">
                  <span className="insights-stat-n">
                    {out.success_rate != null ? `${Math.round(out.success_rate * 100)}%` : "—"}
                  </span>
                  <span className="insights-stat-l">success</span>
                </div>
                <div className="insights-stat">
                  <span className="insights-stat-n insights-up">
                    <ThumbsUp size={11} /> {fb.up}
                  </span>
                  <span className="insights-stat-l">liked</span>
                </div>
                <div className="insights-stat">
                  <span className="insights-stat-n insights-down">
                    <ThumbsDown size={11} /> {fb.down}
                  </span>
                  <span className="insights-stat-l">disliked</span>
                </div>
              </div>
            </section>

            {/* ── What the bandit has learned ──────────────── */}
            <section>
              <h3 className="insights-h">Provider reward (bandit)</h3>
              {banditRows.length === 0 ? (
                <p className="text-xs text-loki-dim py-1">
                  No data yet — Loki learns as you use it.
                </p>
              ) : (
                <div className="space-y-1.5">
                  {banditRows.map(([name, s]) => {
                    const pct = rewardToPct(s.avg_reward);
                    return (
                      <div key={name} className="insights-bar-row">
                        <span className="insights-bar-label">{name}</span>
                        <div className="insights-bar-track">
                          <div className="insights-bar-fill"
                            ref={(el) => { if (el) el.style.width = `${pct}%`; }} />
                        </div>
                        <span className="insights-bar-val">{s.avg_reward.toFixed(2)}</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </section>

            {/* ── Recent actions (audit) ───────────────────── */}
            <section>
              <div className="flex items-center justify-between mb-1.5">
                <h3 className="insights-h mb-0">Recent actions</h3>
                <button type="button" onClick={onUndo}
                  className="insights-undo" aria-label="Undo last action">
                  <RotateCcw size={11} /> Undo last
                </button>
              </div>
              {audit.length === 0 ? (
                <p className="text-xs text-loki-dim py-1">No tracked actions yet.</p>
              ) : (
                <div className="space-y-1">
                  {audit.map((e, i) => (
                    <div key={i} className="insights-audit-row">
                      <span className="insights-audit-dot"
                        ref={(el) => { if (el) el.style.background = TIER_COLOR[e.tier] ?? "#6b7280"; }} />
                      <span className="insights-audit-intent">{e.intent}</span>
                      <span className={`insights-audit-status ${e.success ? "ok" : "fail"}`}>
                        {e.success ? "✓" : "✗"}
                      </span>
                      <span className="insights-audit-result">{e.result}</span>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </div>

      <div className="sidebar-footer">
        Loki learns from every interaction · ratings sharpen its choices
      </div>
    </motion.div>
  );
}
