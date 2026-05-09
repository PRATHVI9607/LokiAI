"""
Loki main window — Norse-themed dark UI with chat and voice input.
"""

import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QSystemTrayIcon, QMenu, QSizePolicy, QFrame,
)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QTextCursor, QFont, QAction, QKeySequence, QPainter, QColor

logger = logging.getLogger(__name__)

STATUS_STYLES = {
    "idle":      ("#8888cc", "#1e1e3e"),
    "listening": ("#50fa7b", "#0a2010"),
    "thinking":  ("#c4a45a", "#20180a"),
    "speaking":  ("#8be9fd", "#082020"),
    "muted":     ("#ff5555", "#200808"),
    "error":     ("#ff5555", "#200808"),
}

STATUS_TEXT = {
    "idle": "⬡  LOKI — IDLE",
    "listening": "◉  LISTENING...",
    "thinking": "◈  THINKING...",
    "speaking": "▶  SPEAKING...",
    "muted": "✕  MUTED",
    "error": "⚠  ERROR",
}


class LokiWindow(QMainWindow):
    """Loki's main UI window — dark Norse aesthetic."""

    mute_toggled = pyqtSignal(bool)
    undo_requested = pyqtSignal()
    user_text_submitted = pyqtSignal(str)
    window_closing = pyqtSignal()
    transcript_updated = pyqtSignal(str)

    def __init__(self, config: dict):
        super().__init__()
        self._cfg = config.get("ui", {})
        self._width = self._cfg.get("width", 480)
        self._height = self._cfg.get("height", 620)
        self._position = self._cfg.get("position", "bottom_right")
        self._always_on_top = self._cfg.get("always_on_top", True)
        self._is_muted = False
        self._dragging = False
        self._drag_pos = QPoint()
        self._current_status = "idle"
        self._mic_active = False

        self._setup_window()
        self._load_stylesheet()
        self._setup_ui()
        self._setup_tray()
        self._position_window()

        if not self._cfg.get("start_hidden", False):
            self.show()

        logger.info("Loki window initialized")

    def _setup_window(self) -> None:
        self.setWindowTitle("Loki")
        self.resize(self._width, self._height)
        self.setMinimumSize(420, 500)

        flags = Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
        if self._always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

    def _load_stylesheet(self) -> None:
        qss_path = Path(__file__).parent / "themes" / "dark.qss"
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def _setup_ui(self) -> None:
        central = QWidget()
        central.setObjectName("loki_panel")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(16, 14, 16, 16)
        root.setSpacing(10)

        # Title bar
        root.addLayout(self._build_title_bar())

        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: #1e1e3e;")
        root.addWidget(divider)

        # Status
        self._status_label = QLabel(STATUS_TEXT["idle"])
        self._status_label.setObjectName("status_label")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setFixedHeight(36)
        root.addWidget(self._status_label)

        # Live transcript
        self._transcript_label = QLabel("")
        self._transcript_label.setObjectName("transcript_label")
        self._transcript_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._transcript_label.setWordWrap(True)
        self._transcript_label.setStyleSheet("color: #4a4a7a; font-size: 8pt; font-style: italic;")
        self._transcript_label.hide()
        root.addWidget(self._transcript_label)

        # Chat area
        self._chat_area = QTextEdit()
        self._chat_area.setObjectName("chat_area")
        self._chat_area.setReadOnly(True)
        self._chat_area.setPlaceholderText('Say "Hey Loki" or type below...')
        root.addWidget(self._chat_area, stretch=1)

        # Input area
        root.addLayout(self._build_input_bar())

        # Action buttons
        root.addLayout(self._build_action_bar())

    def _build_title_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(8)

        # Icon + title
        title_v = QVBoxLayout()
        title_v.setSpacing(0)

        title = QLabel("LOKI")
        title.setObjectName("loki_title")
        title_v.addWidget(title)

        subtitle = QLabel("AI DESKTOP ASSISTANT")
        subtitle.setObjectName("loki_subtitle")
        title_v.addWidget(subtitle)

        layout.addLayout(title_v)
        layout.addStretch()

        # Window controls
        min_btn = QPushButton("—")
        min_btn.setObjectName("min_btn")
        min_btn.setToolTip("Minimize")
        min_btn.clicked.connect(self.showMinimized)
        layout.addWidget(min_btn)

        close_btn = QPushButton("×")
        close_btn.setObjectName("close_btn")
        close_btn.setToolTip("Hide to tray")
        close_btn.clicked.connect(self.hide)
        layout.addWidget(close_btn)

        return layout

    def _build_input_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(8)

        self._input_field = QLineEdit()
        self._input_field.setObjectName("input_field")
        self._input_field.setPlaceholderText('Type a command or question...')
        self._input_field.returnPressed.connect(self._on_text_submit)
        layout.addWidget(self._input_field, stretch=1)

        self._mic_btn = QPushButton("🎙")
        self._mic_btn.setObjectName("mic_btn")
        self._mic_btn.setToolTip("Voice input (or say 'Hey Loki')")
        self._mic_btn.setCheckable(True)
        self._mic_btn.clicked.connect(self._on_mic_clicked)
        layout.addWidget(self._mic_btn)

        send_btn = QPushButton("Send")
        send_btn.setObjectName("send_btn")
        send_btn.clicked.connect(self._on_text_submit)
        layout.addWidget(send_btn)

        return layout

    def _build_action_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(8)

        mute_btn = QPushButton("Mute")
        mute_btn.setObjectName("mute_btn")
        mute_btn.setToolTip("Toggle microphone")
        mute_btn.clicked.connect(self._on_mute_clicked)
        self._mute_btn = mute_btn
        layout.addWidget(mute_btn)

        undo_btn = QPushButton("Undo")
        undo_btn.setObjectName("undo_btn")
        undo_btn.setToolTip("Undo last action")
        undo_btn.clicked.connect(self.undo_requested.emit)
        layout.addWidget(undo_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("clear_btn")
        clear_btn.setToolTip("Clear chat")
        clear_btn.clicked.connect(self._chat_area.clear)
        layout.addWidget(clear_btn)

        return layout

    def _setup_tray(self) -> None:
        self._tray = QSystemTrayIcon(self)
        icon = self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon)
        self._tray.setIcon(icon)
        self._tray.setToolTip("Loki AI Assistant")

        menu = QMenu()

        show_action = QAction("Show Loki", self)
        show_action.triggered.connect(self.show_window)
        menu.addAction(show_action)

        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)
        menu.addAction(hide_action)

        menu.addSeparator()

        mute_action = QAction("Toggle Mute", self)
        mute_action.triggered.connect(self._on_mute_clicked)
        menu.addAction(mute_action)

        menu.addSeparator()

        quit_action = QAction("Quit Loki", self)
        quit_action.triggered.connect(self._on_quit)
        menu.addAction(quit_action)

        self._tray.setContextMenu(menu)
        self._tray.activated.connect(self._on_tray_click)
        self._tray.show()

    def _position_window(self) -> None:
        try:
            screen = self.screen().availableGeometry()
        except Exception:
            return

        w, h = self._width, self._height
        p = self._position

        positions = {
            "bottom_right": (screen.width() - w - 20, screen.height() - h - 50),
            "bottom_left":  (20, screen.height() - h - 50),
            "top_right":    (screen.width() - w - 20, 50),
            "top_left":     (20, 50),
            "center":       ((screen.width() - w) // 2, (screen.height() - h) // 2),
        }
        x, y = positions.get(p, positions["bottom_right"])
        self.move(x, y)

    # --- Public API ---

    def set_status(self, status: str) -> None:
        self._current_status = status
        text = STATUS_TEXT.get(status, status.upper())
        self._status_label.setText(text)

        color, bg = STATUS_STYLES.get(status, ("#8888cc", "#1e1e3e"))
        self._status_label.setStyleSheet(
            f"color: {color}; background: {bg}; border: 1px solid {color}; "
            f"border-radius: 14px; padding: 6px 16px; font-size: 9pt; "
            f"font-weight: 600; letter-spacing: 1px;"
        )
        self._status_label.setProperty("status", status)

    def add_user_message(self, text: str) -> None:
        ts = datetime.now().strftime("%H:%M")
        html = (
            f'<div style="text-align:right;margin:8px 0;">'
            f'<span style="background:#1e1e4a;color:#cdd6f4;padding:9px 13px;'
            f'border-radius:12px 12px 3px 12px;display:inline-block;'
            f'max-width:85%;font-size:10pt;border:1px solid #2a2a6a;">'
            f'<span style="font-size:7pt;color:#4a4a8a;">{ts}</span><br>{text}'
            f'</span></div>'
        )
        self._chat_area.append(html)
        self._scroll_bottom()

    def add_loki_message(self, text: str) -> None:
        ts = datetime.now().strftime("%H:%M")
        # Escape HTML in text
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe = safe.replace("\n", "<br>")
        html = (
            f'<div style="text-align:left;margin:8px 0;">'
            f'<span style="background:#0d0d22;color:#c4a45a;padding:9px 13px;'
            f'border-radius:12px 12px 12px 3px;display:inline-block;'
            f'max-width:85%;font-size:10pt;border:1px solid #2a1f5a;">'
            f'<span style="font-size:7pt;color:#6b6ba8;">{ts} · LOKI</span><br>{safe}'
            f'</span></div>'
        )
        self._chat_area.append(html)
        self._scroll_bottom()

    def add_system_message(self, text: str) -> None:
        ts = datetime.now().strftime("%H:%M")
        html = (
            f'<div style="text-align:center;margin:6px 0;">'
            f'<span style="color:#2a2a5a;font-size:8pt;">{ts} · {text}</span>'
            f'</div>'
        )
        self._chat_area.append(html)

    def update_transcript(self, text: str) -> None:
        if text and text.strip():
            preview = text.strip()[:80]
            self._transcript_label.setText(f'"{preview}"')
            self._transcript_label.show()
            self.transcript_updated.emit(text)
        else:
            self.clear_transcript()

    def clear_transcript(self) -> None:
        self._transcript_label.setText("")
        self._transcript_label.hide()

    def show_window(self) -> None:
        self.show()
        self.raise_()
        self.activateWindow()

    def hide_window(self) -> None:
        self.hide()

    # --- Event handlers ---

    def _on_text_submit(self) -> None:
        text = self._input_field.text().strip()
        if text:
            self._input_field.clear()
            self.user_text_submitted.emit(text)

    def _on_mic_clicked(self) -> None:
        self._mic_active = not self._mic_active
        self._mic_btn.setProperty("active", "true" if self._mic_active else "false")
        self._mic_btn.style().unpolish(self._mic_btn)
        self._mic_btn.style().polish(self._mic_btn)

    def _on_mute_clicked(self) -> None:
        self._is_muted = not self._is_muted
        self._mute_btn.setText("Unmute" if self._is_muted else "Mute")
        self.mute_toggled.emit(self._is_muted)
        if self._is_muted:
            self.set_status("muted")

    def _on_tray_click(self, reason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()

    def _on_quit(self) -> None:
        self.window_closing.emit()
        self._tray.hide()
        self.close()

    def _scroll_bottom(self) -> None:
        cursor = self._chat_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self._chat_area.setTextCursor(cursor)

    # --- Window dragging ---

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self._dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()


def create_loki_window(config: dict) -> LokiWindow:
    return LokiWindow(config)
