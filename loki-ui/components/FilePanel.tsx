"use client";

import { useCallback, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, Trash2, X, Database } from "lucide-react";
import { type FileEntry } from "@/hooks/useLoki";

interface FilePanelProps {
  files: FileEntry[];
  ragAvailable: boolean;
  onUpload: (file: File) => Promise<void>;
  onDelete: (filename: string) => Promise<void>;
  onClose: () => void;
}

export default function FilePanel({ files, ragAvailable, onUpload, onDelete, onClose }: FilePanelProps) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const uploadingRef = useRef(false);

  const handleFiles = useCallback(async (fileList: FileList | null) => {
    if (!fileList || uploadingRef.current) return;
    uploadingRef.current = true;
    for (const file of Array.from(fileList)) {
      setUploading(file.name);
      try {
        await onUpload(file);
      } catch {
        // error surfaced via system_message inside onUpload
      } finally {
        setUploading(null);
      }
    }
    uploadingRef.current = false;
  }, [onUpload]);

  const onDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    await handleFiles(e.dataTransfer.files);
  }, [handleFiles]);

  const onDragOver = (e: React.DragEvent) => { e.preventDefault(); setDragging(true); };
  const onDragLeave = () => setDragging(false);

  return (
    <motion.div
      className="glass-strong rounded-2xl flex flex-col overflow-hidden"
      style={{ width: 300, maxHeight: 500 }}
      initial={{ opacity: 0, x: 20, scale: 0.95 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 20, scale: 0.95 }}
      transition={{ duration: 0.25 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-loki-purple/40">
        <div className="flex items-center gap-2">
          <Database size={14} className="text-loki-gold" />
          <span className="text-sm font-medium text-loki-text">File Knowledge</span>
          {!ragAvailable && (
            <span className="text-xs text-loki-error bg-loki-error/10 px-2 py-0.5 rounded-full">
              No embed model
            </span>
          )}
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close file panel"
          className="text-loki-muted hover:text-loki-text transition-colors"
        >
          <X size={14} />
        </button>
      </div>

      {/* Hidden file input — outside drop zone to avoid nested interactive controls */}
      <input
        ref={inputRef}
        id="loki-file-input"
        type="file"
        multiple
        aria-label="Upload files for indexing"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
        accept=".py,.js,.ts,.tsx,.jsx,.go,.rs,.java,.cpp,.c,.h,.md,.txt,.yaml,.yml,.json,.toml,.pdf,.sql,.sh"
      />

      {/* Drop zone */}
      <div
        role="button"
        tabIndex={0}
        aria-label="Drop files here or click to upload"
        className={`mx-3 mt-3 rounded-xl border-2 border-dashed p-4 text-center cursor-pointer transition-all duration-200
          ${dragging
            ? "border-loki-gold bg-loki-gold/10"
            : "border-loki-purple-light/50 hover:border-loki-gold/50 hover:bg-loki-purple/20"
          }`}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            inputRef.current?.click();
          }
        }}
      >
        <Upload size={20} className={`mx-auto mb-1 ${dragging ? "text-loki-gold" : "text-loki-muted"}`} />
        <p className="text-xs text-loki-muted">
          {uploading ? `Indexing ${uploading}…` : "Drop files or click to upload"}
        </p>
        <p className="text-xs text-loki-muted/60 mt-0.5">py, js, ts, md, txt, pdf, yaml…</p>
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto px-3 py-2">
        <AnimatePresence>
          {files.length === 0 ? (
            <p className="text-xs text-loki-muted/60 text-center py-4">No files indexed yet.</p>
          ) : (
            files.map((f) => (
              <motion.div
                key={f.filename}
                className="flex items-center justify-between py-2 px-2 rounded-lg hover:bg-loki-purple/20 group"
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -10 }}
              >
                <div className="flex items-center gap-2 min-w-0">
                  <FileText size={12} className="text-loki-gold flex-shrink-0" />
                  <span className="text-xs text-loki-text truncate">{f.filename}</span>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  {f.chunkCount !== undefined && (
                    <span className="text-xs text-loki-muted/60">{f.chunkCount}c</span>
                  )}
                  <button
                    type="button"
                    onClick={() => onDelete(f.filename)}
                    aria-label={`Remove ${f.filename}`}
                    className="opacity-0 group-hover:opacity-100 focus-visible:opacity-100 text-loki-muted hover:text-loki-error transition-all"
                  >
                    <Trash2 size={11} />
                  </button>
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>

      {files.length > 0 && (
        <div className="px-4 pb-3 text-xs text-loki-muted/60 text-center">
          {files.length} file{files.length !== 1 ? "s" : ""} indexed — Loki reads them for context
        </div>
      )}
    </motion.div>
  );
}
