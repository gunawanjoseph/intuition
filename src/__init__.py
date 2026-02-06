"""
Memory Context Overlay
A desktop application to help users with ADHD or dementia stay focused.
"""

__version__ = "1.0.0"
__author__ = "Memory Context Team"

from .screen_capture import ScreenCapture
from .ocr_extractor import OCRExtractor
from .context_analyzer import ContextAnalyzer
from .gui_overlay import OverlayManager, ContextIcon, InfoPanel

__all__ = [
    'ScreenCapture',
    'OCRExtractor', 
    'ContextAnalyzer',
    'OverlayManager',
    'ContextIcon',
    'InfoPanel'
]
