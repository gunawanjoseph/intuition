"""
GUI Overlay Module
PyQt6-based overlay with persistent icon and info panel.
"""

import sys
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush


class ContextIcon(QWidget):
    """
    Persistent clickable icon that stays in the bottom-left corner.
    """
    
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Icon size
        self.icon_size = 48
        self.setFixedSize(self.icon_size + 10, self.icon_size + 10)
        
        # Hover state
        self._hovered = False
        
        # Tooltip
        self.setToolTip("Click to see what you were doing")
    
    def paintEvent(self, event):
        """Draw the icon."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background circle
        if self._hovered:
            color = QColor(70, 130, 180, 230)  # Steel blue, slightly brighter
        else:
            color = QColor(70, 130, 180, 200)  # Steel blue
        
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(5, 5, self.icon_size, self.icon_size)
        
        # Draw brain/memory icon (simplified)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont('Arial', 24))
        painter.drawText(5, 5, self.icon_size, self.icon_size, 
                        Qt.AlignmentFlag.AlignCenter, "🧠")
        
        painter.end()
    
    def enterEvent(self, event):
        """Handle mouse enter."""
        self._hovered = True
        self.update()
    
    def leaveEvent(self, event):
        """Handle mouse leave."""
        self._hovered = False
        self.update()
    
    def mousePressEvent(self, event):
        """Handle mouse click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
    
    def position_bottom_left(self):
        """Position the icon in the bottom-left corner of the screen."""
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            x = geometry.left() + 20
            y = geometry.bottom() - self.height() - 20
            self.move(x, y)


class InfoPanel(QWidget):
    """
    Information panel that shows activity summary and key information.
    """
    
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.Popup
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Panel size
        self.panel_width = 400
        self.panel_height = 450
        self.setFixedSize(self.panel_width, self.panel_height)
        
        # Setup UI
        self._setup_ui()
        
        # Track if mouse is inside
        self._mouse_inside = False
    
    def _setup_ui(self):
        """Setup the panel UI."""
        # Main container with rounded corners
        self.container = QFrame(self)
        self.container.setGeometry(0, 0, self.panel_width, self.panel_height)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 40, 245);
                border-radius: 15px;
                border: 2px solid rgba(70, 130, 180, 150);
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("🧠 Memory Context")
        header.setStyleSheet("""
            QLabel {
                color: #4A90D9;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(header)
        
        # Divider
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setStyleSheet("background-color: rgba(70, 130, 180, 100); border: none;")
        divider1.setFixedHeight(1)
        layout.addWidget(divider1)
        
        # Activity Section
        activity_header = QLabel("📋 You were doing:")
        activity_header.setStyleSheet("""
            QLabel {
                color: #87CEEB;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(activity_header)
        
        self.activity_label = QLabel("Analyzing your activity...")
        self.activity_label.setWordWrap(True)
        self.activity_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                background: transparent;
                border: none;
                padding: 5px;
            }
        """)
        layout.addWidget(self.activity_label)
        
        self.app_label = QLabel("Using: Unknown")
        self.app_label.setStyleSheet("""
            QLabel {
                color: #B0B0B0;
                font-size: 12px;
                background: transparent;
                border: none;
                padding-left: 5px;
            }
        """)
        layout.addWidget(self.app_label)
        
        # Divider
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet("background-color: rgba(70, 130, 180, 100); border: none;")
        divider2.setFixedHeight(1)
        layout.addWidget(divider2)
        
        # Key Information Section
        key_info_header = QLabel("🔑 Key Information:")
        key_info_header.setStyleSheet("""
            QLabel {
                color: #87CEEB;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(key_info_header)
        
        # Scrollable area for key info
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(50, 50, 60, 100);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(70, 130, 180, 150);
                border-radius: 4px;
            }
        """)
        
        self.key_info_container = QWidget()
        self.key_info_container.setStyleSheet("background: transparent;")
        self.key_info_layout = QVBoxLayout(self.key_info_container)
        self.key_info_layout.setContentsMargins(0, 0, 0, 0)
        self.key_info_layout.setSpacing(8)
        self.key_info_layout.addStretch()
        
        scroll_area.setWidget(self.key_info_container)
        layout.addWidget(scroll_area, 1)
        
        # Footer with timestamp
        self.timestamp_label = QLabel("Last updated: --")
        self.timestamp_label.setStyleSheet("""
            QLabel {
                color: #707070;
                font-size: 10px;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(self.timestamp_label)
    
    def update_context(self, context: Dict[str, Any]):
        """
        Update the panel with new context information.
        
        Args:
            context: Dictionary with activity, application, and key_events
        """
        # Update activity
        activity = context.get('activity', 'Unknown activity')
        self.activity_label.setText(activity)
        
        # Update application
        app = context.get('application', 'Unknown')
        self.app_label.setText(f"Using: {app}")
        
        # Update key information
        self._update_key_info(context.get('key_events', []))
        
        # Update timestamp
        last_analysis = context.get('last_analysis')
        if last_analysis:
            self.timestamp_label.setText(f"Last updated: {last_analysis.strftime('%H:%M:%S')}")
    
    def _update_key_info(self, key_events: list):
        """Update the key information display."""
        # Clear existing items (except stretch)
        while self.key_info_layout.count() > 1:
            item = self.key_info_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not key_events:
            no_info_label = QLabel("No key information detected yet")
            no_info_label.setStyleSheet("""
                QLabel {
                    color: #707070;
                    font-size: 12px;
                    font-style: italic;
                    background: transparent;
                    border: none;
                }
            """)
            self.key_info_layout.insertWidget(0, no_info_label)
            return
        
        # Add key info items (most recent first)
        for event in reversed(key_events[-10:]):  # Show last 10 items
            item_widget = self._create_key_info_item(event)
            self.key_info_layout.insertWidget(
                self.key_info_layout.count() - 1, 
                item_widget
            )
    
    def _create_key_info_item(self, event: Dict) -> QWidget:
        """Create a widget for a single key info item."""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background-color: rgba(50, 50, 60, 150);
                border-radius: 8px;
                padding: 5px;
            }
        """)
        
        layout = QVBoxLayout(item)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(3)
        
        # Type icon mapping
        type_icons = {
            'otp': '🔐',
            'code': '🔐',
            'verification': '🔐',
            'email': '📧',
            'phone': '📞',
            'name': '👤',
            'url': '🔗',
            'link': '🔗',
            'price': '💰',
            'amount': '💰',
            'date': '📅',
            'time': '⏰',
            'order': '📦',
            'tracking': '📦',
            'info': 'ℹ️'
        }
        
        event_type = event.get('type', 'info').lower()
        icon = type_icons.get(event_type, 'ℹ️')
        
        # Value line
        value_label = QLabel(f"{icon} {event.get('value', '')}")
        value_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(value_label)
        
        # Context line
        context = event.get('context', '')
        if context:
            context_label = QLabel(context)
            context_label.setStyleSheet("""
                QLabel {
                    color: #909090;
                    font-size: 11px;
                    background: transparent;
                    border: none;
                }
            """)
            layout.addWidget(context_label)
        
        # Timestamp
        timestamp = event.get('timestamp')
        if timestamp:
            time_str = timestamp.strftime('%H:%M:%S')
            time_label = QLabel(time_str)
            time_label.setStyleSheet("""
                QLabel {
                    color: #606060;
                    font-size: 10px;
                    background: transparent;
                    border: none;
                }
            """)
            layout.addWidget(time_label)
        
        return item
    
    def position_above_icon(self, icon_pos: QPoint):
        """Position the panel above the icon."""
        x = icon_pos.x()
        y = icon_pos.y() - self.panel_height - 10
        
        # Ensure panel stays on screen
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            
            # Adjust horizontal position
            if x + self.panel_width > geometry.right():
                x = geometry.right() - self.panel_width - 10
            if x < geometry.left():
                x = geometry.left() + 10
            
            # Adjust vertical position
            if y < geometry.top():
                y = icon_pos.y() + 60  # Show below icon instead
        
        self.move(x, y)
    
    def focusOutEvent(self, event):
        """Close panel when focus is lost."""
        self.hide()
        self.closed.emit()


class OverlayManager:
    """
    Manages the overlay icon and info panel.
    """
    
    def __init__(self):
        self.app: Optional[QApplication] = None
        self.icon: Optional[ContextIcon] = None
        self.panel: Optional[InfoPanel] = None
        
        # Context callback
        self._get_context_callback: Optional[Callable] = None
        
        # Update timer
        self._update_timer: Optional[QTimer] = None
    
    def set_context_callback(self, callback: Callable):
        """
        Set callback to get current context.
        Callback should return a dict with activity, application, key_events.
        """
        self._get_context_callback = callback
    
    def initialize(self):
        """Initialize the Qt application and widgets."""
        # Create application if needed
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        
        # Create icon
        self.icon = ContextIcon()
        self.icon.clicked.connect(self._on_icon_clicked)
        self.icon.position_bottom_left()
        
        # Create panel
        self.panel = InfoPanel()
        self.panel.closed.connect(self._on_panel_closed)
        
        # Setup update timer
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_panel)
        
        print("[OverlayManager] Initialized")
    
    def show(self):
        """Show the overlay icon."""
        if self.icon:
            self.icon.show()
            print("[OverlayManager] Icon shown")
    
    def hide(self):
        """Hide all overlay elements."""
        if self.icon:
            self.icon.hide()
        if self.panel:
            self.panel.hide()
    
    def _on_icon_clicked(self):
        """Handle icon click - show/toggle panel."""
        if self.panel:
            if self.panel.isVisible():
                self.panel.hide()
                self._update_timer.stop()
            else:
                # Update and show panel
                self._update_panel()
                self.panel.position_above_icon(self.icon.pos())
                self.panel.show()
                self.panel.setFocus()
                
                # Start periodic updates while panel is open
                self._update_timer.start(2000)  # Update every 2 seconds
    
    def _on_panel_closed(self):
        """Handle panel close."""
        self._update_timer.stop()
    
    def _update_panel(self):
        """Update panel with current context."""
        if self._get_context_callback and self.panel:
            try:
                context = self._get_context_callback()
                self.panel.update_context(context)
            except Exception as e:
                print(f"[OverlayManager] Update error: {e}")
    
    def run(self):
        """Run the Qt event loop."""
        if self.app:
            return self.app.exec()
        return 0


# Test function
if __name__ == "__main__":
    print("Testing GUI Overlay Module...")
    
    # Create manager
    manager = OverlayManager()
    manager.initialize()
    
    # Test context
    test_context = {
        'activity': 'Writing an email to John about the project deadline',
        'application': 'Gmail - Chrome',
        'key_events': [
            {
                'timestamp': datetime.now(),
                'type': 'otp',
                'value': '847291',
                'context': 'Verification code from Gmail'
            },
            {
                'timestamp': datetime.now(),
                'type': 'email',
                'value': 'john.smith@company.com',
                'context': 'Recipient email'
            },
            {
                'timestamp': datetime.now(),
                'type': 'name',
                'value': 'John Smith',
                'context': 'Contact name'
            }
        ],
        'last_analysis': datetime.now()
    }
    
    manager.set_context_callback(lambda: test_context)
    manager.show()
    
    print("GUI test running. Click the icon to see the panel.")
    print("Press Ctrl+C to exit.")
    
    manager.run()
