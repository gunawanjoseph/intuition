"""
Memory Context Overlay - Main Application
Integrates screen capture, OCR, LLM analysis, and GUI overlay.
"""

import sys
import os
import signal
import threading
from datetime import datetime
from typing import Optional

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from screen_capture import ScreenCapture
from ocr_extractor import OCRExtractor
from context_analyzer import ContextAnalyzer
from gui_overlay import OverlayManager

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer


class MemoryContextApp:
    """
    Main application class that coordinates all components.
    """
    
    def __init__(self):
        # Configuration
        self.capture_fps = 3.0
        self.buffer_duration = 60  # seconds
        self.analysis_interval = 10.0  # seconds
        
        # Components
        self.screen_capture: Optional[ScreenCapture] = None
        self.ocr_extractor: Optional[OCRExtractor] = None
        self.context_analyzer: Optional[ContextAnalyzer] = None
        self.overlay_manager: Optional[OverlayManager] = None
        
        # State
        self._running = False
        self._frame_count = 0
        self._ocr_count = 0
    
    def initialize(self):
        """Initialize all components."""
        print("=" * 50)
        print("Memory Context Overlay")
        print("Helping you remember what you were doing")
        print("=" * 50)
        print()
        
        # Initialize screen capture
        print("[Main] Initializing screen capture...")
        self.screen_capture = ScreenCapture(
            fps=self.capture_fps,
            buffer_duration=self.buffer_duration
        )
        
        # Initialize OCR extractor
        print("[Main] Initializing OCR extractor...")
        self.ocr_extractor = OCRExtractor(
            languages=['en'],
            buffer_duration=self.buffer_duration
        )
        
        # Initialize context analyzer
        print("[Main] Initializing context analyzer...")
        self.context_analyzer = ContextAnalyzer(
            analysis_interval=self.analysis_interval
        )
        
        # Set up callbacks
        self.screen_capture.set_frame_callback(self._on_frame_captured)
        self.context_analyzer.set_text_callback(self._get_recent_text)
        
        # Initialize GUI overlay
        print("[Main] Initializing GUI overlay...")
        self.overlay_manager = OverlayManager()
        self.overlay_manager.initialize()
        self.overlay_manager.set_context_callback(self._get_current_context)
        
        print("[Main] All components initialized")
        print()
    
    def _on_frame_captured(self, timestamp: datetime, image):
        """Callback when a new frame is captured."""
        self._frame_count += 1
        
        # Process every 3rd frame for OCR (approximately 1 per second at 3 FPS)
        if self._frame_count % 3 == 0:
            # Run OCR in a separate thread to avoid blocking
            threading.Thread(
                target=self._process_frame_ocr,
                args=(timestamp, image),
                daemon=True
            ).start()
    
    def _process_frame_ocr(self, timestamp: datetime, image):
        """Process a frame through OCR."""
        try:
            result = self.ocr_extractor.process_frame(timestamp, image)
            if result:
                self._ocr_count += 1
        except Exception as e:
            print(f"[Main] OCR processing error: {e}")
    
    def _get_recent_text(self) -> str:
        """Get recent text for context analysis."""
        if self.ocr_extractor:
            return self.ocr_extractor.get_combined_text(seconds=30)
        return ""
    
    def _get_current_context(self) -> dict:
        """Get current context for the GUI panel."""
        if self.context_analyzer:
            return self.context_analyzer.get_current_context()
        return {
            'activity': 'Initializing...',
            'application': 'Unknown',
            'key_events': [],
            'last_analysis': None
        }
    
    def start(self):
        """Start all background services."""
        print("[Main] Starting services...")
        
        # Start screen capture
        self.screen_capture.start()
        
        # Start context analyzer
        self.context_analyzer.start()
        
        # Show overlay
        self.overlay_manager.show()
        
        self._running = True
        print("[Main] All services started")
        print()
        print("=" * 50)
        print("Application is running!")
        print("Look for the 🧠 icon in the bottom-left corner")
        print("Click it to see what you were doing")
        print("Press Ctrl+C to exit")
        print("=" * 50)
        print()
    
    def stop(self):
        """Stop all services."""
        print()
        print("[Main] Stopping services...")
        
        self._running = False
        
        if self.screen_capture:
            self.screen_capture.stop()
        
        if self.context_analyzer:
            self.context_analyzer.stop()
        
        if self.overlay_manager:
            self.overlay_manager.hide()
        
        print("[Main] All services stopped")
        print()
        print("Statistics:")
        print(f"  Frames captured: {self._frame_count}")
        print(f"  OCR extractions: {self._ocr_count}")
        
        if self.ocr_extractor:
            stats = self.ocr_extractor.get_buffer_stats()
            print(f"  Text entries in buffer: {stats['entry_count']}")
        
        if self.context_analyzer:
            context = self.context_analyzer.get_current_context()
            print(f"  Key events detected: {len(context['key_events'])}")
    
    def run(self):
        """Run the application."""
        self.initialize()
        self.start()
        
        # Run Qt event loop
        return self.overlay_manager.run()


def main():
    """Main entry point."""
    app = MemoryContextApp()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n[Main] Interrupt received, shutting down...")
        app.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        return app.run()
    except KeyboardInterrupt:
        app.stop()
        return 0
    except Exception as e:
        print(f"[Main] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        app.stop()
        return 1


if __name__ == "__main__":
    sys.exit(main())
