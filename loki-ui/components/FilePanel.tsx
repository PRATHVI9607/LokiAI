"use client";

import { useCallback, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, Trash2, X, Layers } from "lucide-react";
import { type FileEntry } from "@/hooks/useLoki";

const FILE_SIZE_LIMIT = 10 * 1024 * 1024;

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
      if (file.size > FILE_SIZE_LIMIT) continue;
      setUploading(file.name);
      try { await onUpload(file); } catch { /* surfaced via system_message */ } finally { setUploading(null); }
    }
    uploadingRef.current = false;
  }, [onUpload]);

  const onDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault(); setDragging(false);
    await handleFiles(e.dataTransfer.files);
  }, [handleFiles]);

  return (
    <motion.div
      className="file-sidebar"
      initial={{ opacity: 0, x: -24 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -24 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
    >
      {/* Header */}
      <div className="sidebar-header">
        <div className="flex items-center gap-2">
          <Layers size={14} className="text-loki-gold" />
          <span className="text-sm font-semibold text-loki-text">File Knowledge</span>
          {!ragAvailable && (
            <span className="sidebar-badge-error">No embed model</span>
          )}
        </div>
        <button type="button" onClick={onClose} aria-label="Close file panel"
          className="text-loki-dim hover:text-loki-text transition-colors p-1 rounded">
          <X size={15} />
        </button>
      </div>

      {/* Hidden input */}
      <input ref={inputRef} type="file" multiple className="hidden" id="loki-file-input"
        aria-label="Upload files for indexing"
        accept=".py,.js,.ts,.tsx,.jsx,.go,.rs,.java,.cpp,.c,.h,.md,.txt,.yaml,.yml,.json,.toml,.pdf,.sql,.sh"
        onChange={(e) => handleFiles(e.target.files)} />

      {/* Drop zone */}
      <div
        role="button" tabIndex={0}
        aria-label="Drop files here or click to upload"
        className={`dropzone ${dragging ? "dropzone-active" : ""}`}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); inputRef.current?.click(); } }}
        onDrop={onDrop}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
      >
        <Upload size={22} className={`mx-auto mb-2 ${dragging ? "text-loki-gold" : "text-loki-dim"}`} />
        <p className="text-xs text-loki-muted font-medium">
          {uploading ? `Indexing ${uploading}…` : "Drop files or click to upload"}
        </p>
        <p className="text-xs text-loki-dim mt-1">py · js · ts · md · txt · pdf · yaml</p>
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto py-2">
        <AnimatePresence>
          {files.length === 0 ? (
            <p className="text-xs text-loki-dim text-center py-6">No files indexed yet</p>
          ) : (
            files.map((f) => (
              <motion.div key={f.filename} className="file-list-item group"
                initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, x: -8 }}>
                <div className="flex items-center gap-2 min-w-0">
                  <FileText size={12} className="text-loki-gold flex-shrink-0" />
                  <span className="text-xs text-loki-text truncate">{f.filename}</span>
                  {f.chunkCount !== undefined && (
                    <span className="text-xs text-loki-dim flex-shrink-0">{f.chunkCount}c</span>
                  )}
                </div>
                <button type="button" onClick={() => onDelete(f.filename)}
                  aria-label={`Remove ${f.filename}`}
                  className="opacity-0 group-hover:opacity-100 focus-visible:opacity-100 text-loki-dim hover:text-loki-red transition-all p-1 rounded">
                  <Trash2 size={11} />
                </button>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>

      {files.length > 0 && (
        <div className="sidebar-footer">
          {files.length} file{files.length !== 1 ? "s" : ""} · Loki reads them for context
        </div>
      )}
    </motion.div>
  );
}
