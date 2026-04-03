"""
Minimal status window for Yuki AI voice assistant.

Simple text-based window showing conversation history and current status.
Replaces the complex overlay UI for voice-only architecture.
"""

import re
import logging
from typing import Optional
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QIcon, QTextCursor, QFont, QAction

logger = logging.getLogger(__name__)


class StatusWindow(QMainWindow):
    """
    Minimal status window for Yuki voice assistant.
    
    Features:
    - Simple text display of conversation history
    - Status indicator (Listening/Thinking/Speaking)
    - Mute and Undo buttons
    - System tray integration
    - Auto-hide on conversation timeout
    - Draggable window
    - Live transcription display
    
    Signals:
        mute_toggled: Emitted when mute button is clicked (bool: is_muted)
        undo_requested: Emitted when undo button is clicked
        window_closing: Emitted when window is being closed (not just hidden)
        transcript_updated: Emitted when live transcript changes (str: text)
    """
    
    # Qt Signals
    mute_toggled = pyqtSignal(bool)  # is_muted
    undo_requested = pyqtSignal()
    window_closing = pyqtSignal()
    transcript_updated = pyqtSignal(str)  # live transcript text
    
    def __init__(
        self,
        width: int = 400,
        height: int = 300,
        position: str = "bottom_right",
        start_hidden: bool = True,
        always_on_top: bool = False
    ):
        """
        Initialize status window.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            position: Window position ("bottom_right", "bottom_left", "top_right", "top_left", "center")
            start_hidden: Start with window hidden
            always_on_top: Keep window always on top
        """
        super().__init__()
        
        self._width = width
        self._height = height
        self._position = position
        self._always_on_top = always_on_top
        self._is_muted = False
        self._dragging = False
        self._drag_position = QPoint()
        
        # Setup UI
        self._setup_window()
        self._setup_ui()
        self._setup_system_tray()
        
        # Position window
        self._position_window()
        
        # Hide if configured
        if start_hidden:
            self.hide()
        
        logger.info(f"Status window initialized ({width}x{height}, position: {position})")
    
    def _setup_window(self):
        """Configure main window properties."""
        self.setWindowTitle("Yuki AI")
        self.resize(self._width, self._height)
        self.setMinimumSize(380, 280)
        
        # Window flags - frameless with rounded corners
        flags = Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
        if self._always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        
        # Transparent background for rounded corners
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Enable mouse tracking for dragging
        self.setMouseTracking(True)
    
    def _setup_ui(self):
        """Create UI components - glassy white/sky blue design."""
        # Central widget with glassmorphism effect
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        central_widget.setStyleSheet("""
            #centralWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.95),
                    stop: 0.5 rgba(240, 248, 255, 0.9),
                    stop: 1 rgba(224, 242, 254, 0.95)
                );
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
        """)
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 16, 20, 20)
        layout.setSpacing(14)
        central_widget.setLayout(layout)
        
        # Title bar - glassy
        title_bar = QHBoxLayout()
        title_bar.setSpacing(12)
        
        # App title
        title_label = QLabel("Yuki AI")
        title_label.setStyleSheet("""
            color: #0369a1;
            font-size: 15pt;
            font-weight: 600;
            letter-spacing: 1px;
        """)
        title_bar.addWidget(title_label)
        
        title_bar.addStretch()
        
        # Minimize button - glassy
        minimize_btn = QPushButton("—")
        minimize_btn.setFixedSize(28, 28)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.5);
                border: 1px solid rgba(148, 163, 184, 0.3);
                border-radius: 14px;
                color: #64748b;
                font-size: 10pt;
            }
            QPushButton:hover {
                background: rgba(241, 245, 249, 0.8);
                border-color: rgba(148, 163, 184, 0.5);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        title_bar.addWidget(minimize_btn)
        
        # Close button - glassy red
        close_btn = QPushButton("×")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(254, 226, 226, 0.6);
                border: 1px solid rgba(252, 165, 165, 0.4);
                border-radius: 14px;
                color: #dc2626;
                font-size: 14pt;
            }
            QPushButton:hover {
                background: rgba(254, 202, 202, 0.8);
                border-color: rgba(248, 113, 113, 0.5);
            }
        """)
        close_btn.clicked.connect(self.hide)
        title_bar.addWidget(close_btn)
        
        layout.addLayout(title_bar)
        
        # Divider - subtle gradient
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(186, 230, 253, 0.2),
                stop: 0.5 rgba(125, 211, 252, 0.5),
                stop: 1 rgba(186, 230, 253, 0.2)
            );
        """)
        layout.addWidget(divider)
        
        # Status indicator - glassy pill
        self._status_label = QLabel("Idle")
        self._status_label.setObjectName("statusLabel")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("""
            color: #475569;
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(241, 245, 249, 0.7),
                stop: 1 rgba(226, 232, 240, 0.7)
            );
            border: 1px solid rgba(203, 213, 225, 0.5);
            border-radius: 16px;
            padding: 10px 20px;
            font-size: 10pt;
            font-weight: 600;
        """)
        layout.addWidget(self._status_label)
        
        # Live transcription display - glassy subtle
        self._transcript_label = QLabel("")
        self._transcript_label.setObjectName("transcriptLabel")
        self._transcript_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._transcript_label.setWordWrap(True)
        self._transcript_label.setStyleSheet("""
            color: #64748b;
            font-size: 9pt;
            font-style: italic;
            background: rgba(248, 250, 252, 0.5);
            border-radius: 8px;
            padding: 8px 12px;
        """)
        self._transcript_label.hide()
        layout.addWidget(self._transcript_label)
        
        # Conversation history - glassy card
        self._history_text = QTextEdit()
        self._history_text.setObjectName("historyText")
        self._history_text.setReadOnly(True)
        self._history_text.setPlaceholderText("Conversation will appear here...")
        self._history_text.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.8),
                    stop: 1 rgba(248, 250, 252, 0.7)
                );
                border: 1px solid rgba(203, 213, 225, 0.4);
                border-radius: 12px;
                padding: 12px;
                font-size: 10pt;
                color: #334155;
            }
            QTextEdit::placeholder {
                color: #94a3b8;
            }
            QScrollBar:vertical {
                background: rgba(241, 245, 249, 0.5);
                width: 8px;
                border-radius: 4px;
                margin: 4px 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(148, 163, 184, 0.5);
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(100, 116, 139, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        layout.addWidget(self._history_text, stretch=1)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Mute button - glassy
        self._mute_button = QPushButton("Mute")
        self._mute_button.setObjectName("muteButton")
        self._mute_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.8),
                    stop: 1 rgba(241, 245, 249, 0.7)
                );
                border: 1px solid rgba(203, 213, 225, 0.5);
                border-radius: 10px;
                color: #475569;
                padding: 10px 24px;
                font-size: 10pt;
                font-weight: 500;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(240, 249, 255, 0.9),
                    stop: 1 rgba(224, 242, 254, 0.8)
                );
                border-color: rgba(125, 211, 252, 0.5);
            }
            QPushButton:pressed {
                background: rgba(224, 242, 254, 0.9);
            }
        """)
        self._mute_button.clicked.connect(self._on_mute_clicked)
        button_layout.addWidget(self._mute_button)
        
        # Undo button - glassy sky blue
        self._undo_button = QPushButton("Undo")
        self._undo_button.setObjectName("undoButton")
        self._undo_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(224, 242, 254, 0.8),
                    stop: 1 rgba(186, 230, 253, 0.7)
                );
                border: 1px solid rgba(125, 211, 252, 0.4);
                border-radius: 10px;
                color: #0369a1;
                padding: 10px 24px;
                font-size: 10pt;
                font-weight: 500;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(186, 230, 253, 0.9),
                    stop: 1 rgba(125, 211, 252, 0.7)
                );
                border-color: rgba(56, 189, 248, 0.5);
            }
            QPushButton:pressed {
                background: rgba(125, 211, 252, 0.8);
            }
        """)
        self._undo_button.clicked.connect(self._on_undo_clicked)
        button_layout.addWidget(self._undo_button)
        
        layout.addLayout(button_layout)
    
    def _setup_system_tray(self):
        """Setup system tray icon and menu."""
        self._tray_icon = QSystemTrayIcon(self)
        
        # Use a default icon (you can replace with custom icon)
        # For now, using the application icon
        icon = self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon)
        self._tray_icon.setIcon(icon)
        self._tray_icon.setToolTip("Yuki AI Assistant")
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self._show_window)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Hide Window", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        mute_action = QAction("Toggle Mute", self)
        mute_action.triggered.connect(self._on_mute_clicked)
        tray_menu.addAction(mute_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._on_quit)
        tray_menu.addAction(quit_action)
        
        self._tray_icon.setContextMenu(tray_menu)
        self._tray_icon.activated.connect(self._on_tray_activated)
        self._tray_icon.show()
        
        logger.info("System tray icon created")
    
    def _position_window(self):
        """Position window based on configuration."""
        screen = self.screen().availableGeometry()
        
        if self._position == "bottom_right":
            x = screen.width() - self._width - 20
            y = screen.height() - self._height - 50
        elif self._position == "bottom_left":
            x = 20
            y = screen.height() - self._height - 50
        elif self._position == "top_right":
            x = screen.width() - self._width - 20
            y = 50
        elif self._position == "top_left":
            x = 20
            y = 50
        elif self._position == "center":
            x = (screen.width() - self._width) // 2
            y = (screen.height() - self._height) // 2
        else:
            x = screen.width() - self._width - 20
            y = screen.height() - self._height - 50
        
        self.move(x, y)
    
    def _apply_styles(self):
        """Apply glassy white/sky blue theme."""
        pass  # All styles inline in _setup_ui
    
    # Public API
    
    def set_status(self, status: str):
        """Update status indicator with glassy style."""
        status_lower = status.lower()
        
        if status_lower == "idle":
            self._status_label.setText("Idle")
            self._status_label.setStyleSheet("""
                color: #475569;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(241, 245, 249, 0.7),
                    stop:1 rgba(226, 232, 240, 0.7));
                border: 1px solid rgba(203, 213, 225, 0.5);
                border-radius: 16px; padding: 10px 20px;
                font-size: 10pt; font-weight: 600;
            """)
        elif status_lower == "listening":
            self._status_label.setText("Listening...")
            self._status_label.setStyleSheet("""
                color: #047857;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(209, 250, 229, 0.8),
                    stop:1 rgba(167, 243, 208, 0.7));
                border: 1px solid rgba(110, 231, 183, 0.5);
                border-radius: 16px; padding: 10px 20px;
                font-size: 10pt; font-weight: 600;
            """)
        elif status_lower == "thinking":
            self._status_label.setText("Thinking...")
            self._status_label.setStyleSheet("""
                color: #b45309;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(254, 243, 199, 0.8),
                    stop:1 rgba(253, 230, 138, 0.7));
                border: 1px solid rgba(252, 211, 77, 0.5);
                border-radius: 16px; padding: 10px 20px;
                font-size: 10pt; font-weight: 600;
            """)
        elif status_lower == "speaking":
            self._status_label.setText("Speaking...")
            self._status_label.setStyleSheet("""
                color: #0369a1;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(224, 242, 254, 0.8),
                    stop:1 rgba(186, 230, 253, 0.7));
                border: 1px solid rgba(125, 211, 252, 0.5);
                border-radius: 16px; padding: 10px 20px;
                font-size: 10pt; font-weight: 600;
            """)
        elif status_lower == "muted":
            self._status_label.setText("Muted")
            self._status_label.setStyleSheet("""
                color: #b91c1c;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(254, 226, 226, 0.8),
                    stop:1 rgba(254, 202, 202, 0.7));
                border: 1px solid rgba(252, 165, 165, 0.5);
                border-radius: 16px; padding: 10px 20px;
                font-size: 10pt; font-weight: 600;
            """)
        else:
            self._status_label.setText(status)
            self._status_label.setStyleSheet("""
                color: #475569;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(248, 250, 252, 0.7),
                    stop:1 rgba(241, 245, 249, 0.7));
                border: 1px solid rgba(226, 232, 240, 0.5);
                border-radius: 16px; padding: 10px 20px;
                font-size: 10pt; font-weight: 600;
            """)
        
        logger.debug(f"Status updated: {status}")
    
    def update_transcript(self, text: str, highlight_keywords: bool = True):
        """Update the live transcription display."""
        if not text or not text.strip():
            self._transcript_label.hide()
            return
        
        display_text = text.strip()
        
        if highlight_keywords:
            keywords = ['yuki', 'hey yuki', 'ok yuki', 'okay yuki']
            for keyword in keywords:
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                display_text = pattern.sub(
                    f'<b style="color: #0284c7;">{keyword.title()}</b>',
                    display_text
                )
        
        self._transcript_label.setText(f'"{display_text}"')
        self._transcript_label.show()
        self.transcript_updated.emit(text)
        logger.debug(f"Transcript: {text}")
    
    def clear_transcript(self):
        """Clear the live transcription display."""
        self._transcript_label.setText("")
        self._transcript_label.hide()
    
    def add_user_message(self, message: str):
        """Add user message to conversation history."""
        timestamp = datetime.now().strftime("%H:%M")
        html = f'''<div style="text-align: right; margin: 8px 0;">
            <span style="background: linear-gradient(135deg, #0ea5e9, #0284c7); 
                         color: #fff; 
                         padding: 10px 14px; 
                         border-radius: 14px 14px 4px 14px; 
                         display: inline-block; 
                         max-width: 80%;
                         font-size: 10pt;">
                <span style="font-size: 8pt; opacity: 0.8;">{timestamp}</span><br>{message}
            </span>
        </div>'''
        self._history_text.append(html)
        self._scroll_to_bottom()
    
    def add_yuki_message(self, message: str):
        """Add Yuki's message to conversation history."""
        timestamp = datetime.now().strftime("%H:%M")
        html = f'''<div style="text-align: left; margin: 8px 0;">
            <span style="background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(241,245,249,0.8)); 
                         color: #334155; 
                         padding: 10px 14px; 
                         border-radius: 14px 14px 14px 4px; 
                         display: inline-block; 
                         max-width: 80%;
                         font-size: 10pt;
                         border: 1px solid rgba(203, 213, 225, 0.5);">
                <span style="font-size: 8pt; color: #0369a1;">{timestamp} · Yuki</span><br>{message}
            </span>
        </div>'''
        self._history_text.append(html)
        self._scroll_to_bottom()
    
    def add_system_message(self, message: str):
        """Add system message to conversation history."""
        timestamp = datetime.now().strftime("%H:%M")
        html = f'''<div style="text-align: center; margin: 10px 0;">
            <span style="color: #64748b; font-size: 8pt;">
                {timestamp} · {message}
            </span>
        </div>'''
        self._history_text.append(html)
        self._scroll_to_bottom()
    
    def clear_history(self):
        """Clear conversation history."""
        self._history_text.clear()
        logger.info("Conversation history cleared")
    
    def set_mute_state(self, is_muted: bool):
        """Set mute button state."""
        self._is_muted = is_muted
        if is_muted:
            self._mute_button.setText("Unmute")
            self._mute_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(254, 226, 226, 0.8),
                        stop:1 rgba(254, 202, 202, 0.7));
                    border: 1px solid rgba(252, 165, 165, 0.5);
                    border-radius: 10px;
                    color: #b91c1c;
                    padding: 10px 24px;
                    font-size: 10pt;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(254, 202, 202, 0.9),
                        stop:1 rgba(252, 165, 165, 0.8));
                }
            """)
        else:
            self._mute_button.setText("Mute")
            self._mute_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.8),
                        stop:1 rgba(241, 245, 249, 0.7));
                    border: 1px solid rgba(203, 213, 225, 0.5);
                    border-radius: 10px;
                    color: #475569;
                    padding: 10px 24px;
                    font-size: 10pt;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(240, 249, 255, 0.9),
                        stop:1 rgba(224, 242, 254, 0.8));
                    border-color: rgba(125, 211, 252, 0.5);
                }
            """)
    
    def show_window(self):
        """Show window and bring to front."""
        self.show()
        self.raise_()
        self.activateWindow()
        logger.info("Window shown")
    
    def hide_window(self):
        """Hide window."""
        self.hide()
        logger.info("Window hidden")
    
    # Event handlers
    
    def _on_mute_clicked(self):
        """Handle mute button click."""
        self._is_muted = not self._is_muted
        self.set_mute_state(self._is_muted)
        self.mute_toggled.emit(self._is_muted)
        logger.info(f"Mute toggled: {self._is_muted}")
    
    def _on_undo_clicked(self):
        """Handle undo button click."""
        self.undo_requested.emit()
        logger.info("Undo requested")
    
    def _on_tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()
    
    def _show_window(self):
        """Show window from tray menu."""
        self.show_window()
    
    def _on_quit(self):
        """Handle quit action."""
        logger.info("Quit requested from tray menu")
        self.window_closing.emit()
        self._tray_icon.hide()
        self.close()
    
    def _scroll_to_bottom(self):
        """Scroll conversation history to bottom."""
        cursor = self._history_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self._history_text.setTextCursor(cursor)
    
    # Window dragging
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging."""
        if self._dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release for window dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            event.accept()
    
    # Override close event
    
    def closeEvent(self, event):
        """
        Override close event to hide instead of quit.
        
        Clicking X hides the window (app continues in tray).
        Use tray menu "Quit" to actually exit.
        """
        event.ignore()
        self.hide()
        logger.info("Window hidden (not closed)")


def create_status_window(config: dict) -> StatusWindow:
    """
    Factory function to create status window from config.
    
    Args:
        config: Configuration dictionary with UI settings
    
    Returns:
        Initialized StatusWindow instance
    """
    ui_config = config.get('ui', {})
    
    window = StatusWindow(
        width=ui_config.get('width', 400),
        height=ui_config.get('height', 300),
        position=ui_config.get('position', 'bottom_right'),
        start_hidden=ui_config.get('start_hidden', True),
        always_on_top=ui_config.get('always_on_top', False)
    )
    
    return window
