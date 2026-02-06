"""
Memory Context Overlay - Component Tests
Run with: python -m pytest tests/test_components.py -v
"""

import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch
from PIL import Image, ImageDraw

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestScreenCapture:
    """Tests for the ScreenCapture module."""
    
    def test_initialization(self):
        """Test ScreenCapture initialization."""
        from screen_capture import ScreenCapture
        
        capture = ScreenCapture(fps=3.0, buffer_duration=60)
        
        assert capture.fps == 3.0
        assert capture.buffer_duration == 60
        assert capture.frame_interval == 1.0 / 3.0
        assert len(capture.frame_buffer) == 0
    
    def test_buffer_stats_empty(self):
        """Test buffer stats when empty."""
        from screen_capture import ScreenCapture
        
        capture = ScreenCapture()
        stats = capture.get_buffer_stats()
        
        assert stats['frame_count'] == 0
        assert stats['duration_seconds'] == 0
        assert stats['oldest_timestamp'] is None
        assert stats['newest_timestamp'] is None
    
    def test_callback_setting(self):
        """Test frame callback setting."""
        from screen_capture import ScreenCapture
        
        capture = ScreenCapture()
        callback = Mock()
        capture.set_frame_callback(callback)
        
        assert capture._frame_callback == callback


class TestOCRExtractor:
    """Tests for the OCRExtractor module."""
    
    def test_initialization(self):
        """Test OCRExtractor initialization."""
        from ocr_extractor import OCRExtractor
        
        extractor = OCRExtractor(languages=['en'], buffer_duration=60)
        
        assert extractor.languages == ['en']
        assert extractor.buffer_duration == 60
        assert len(extractor.text_buffer) == 0
    
    def test_buffer_stats_empty(self):
        """Test buffer stats when empty."""
        from ocr_extractor import OCRExtractor
        
        extractor = OCRExtractor()
        stats = extractor.get_buffer_stats()
        
        assert stats['entry_count'] == 0
        assert stats['total_characters'] == 0
        assert stats['avg_confidence'] == 0.0
    
    def test_get_recent_text_empty(self):
        """Test getting recent text when buffer is empty."""
        from ocr_extractor import OCRExtractor
        
        extractor = OCRExtractor()
        records = extractor.get_recent_text(seconds=60)
        
        assert records == []
    
    def test_get_combined_text_empty(self):
        """Test getting combined text when buffer is empty."""
        from ocr_extractor import OCRExtractor
        
        extractor = OCRExtractor()
        text = extractor.get_combined_text(seconds=60)
        
        assert text == ""


class TestContextAnalyzer:
    """Tests for the ContextAnalyzer module."""
    
    def test_initialization(self):
        """Test ContextAnalyzer initialization."""
        from context_analyzer import ContextAnalyzer
        
        analyzer = ContextAnalyzer(analysis_interval=10.0, max_history=50)
        
        assert analyzer.analysis_interval == 10.0
        assert analyzer.max_history == 50
        assert analyzer.current_activity == "Starting up..."
        assert analyzer.current_app == "Unknown"
        assert len(analyzer.key_events) == 0
    
    def test_get_current_context(self):
        """Test getting current context."""
        from context_analyzer import ContextAnalyzer
        
        analyzer = ContextAnalyzer()
        context = analyzer.get_current_context()
        
        assert 'activity' in context
        assert 'application' in context
        assert 'key_events' in context
        assert 'last_analysis' in context
    
    def test_get_recent_key_events_empty(self):
        """Test getting recent key events when empty."""
        from context_analyzer import ContextAnalyzer
        
        analyzer = ContextAnalyzer()
        events = analyzer.get_recent_key_events(minutes=5)
        
        assert events == []
    
    def test_callback_setting(self):
        """Test text callback setting."""
        from context_analyzer import ContextAnalyzer
        
        analyzer = ContextAnalyzer()
        callback = Mock(return_value="test text")
        analyzer.set_text_callback(callback)
        
        assert analyzer._get_text_callback == callback


class TestIntegration:
    """Integration tests for the full application."""
    
    def test_create_test_image(self):
        """Test creating a test image with text."""
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        draw.text((50, 50), "Hello World!", fill='black')
        draw.text((50, 100), "Verification Code: 123456", fill='black')
        
        assert img.size == (800, 600)
        assert img.mode == 'RGB'
    
    def test_module_imports(self):
        """Test that all modules can be imported."""
        from screen_capture import ScreenCapture
        from ocr_extractor import OCRExtractor
        from context_analyzer import ContextAnalyzer
        from gui_overlay import OverlayManager, ContextIcon, InfoPanel
        
        assert ScreenCapture is not None
        assert OCRExtractor is not None
        assert ContextAnalyzer is not None
        assert OverlayManager is not None


def run_basic_tests():
    """Run basic tests without pytest."""
    print("Running basic component tests...")
    print()
    
    # Test imports
    print("Testing imports...")
    try:
        from screen_capture import ScreenCapture
        from ocr_extractor import OCRExtractor
        from context_analyzer import ContextAnalyzer
        from gui_overlay import OverlayManager
        print("  ✓ All modules imported successfully")
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False
    
    # Test ScreenCapture
    print("Testing ScreenCapture...")
    try:
        capture = ScreenCapture(fps=3.0, buffer_duration=60)
        assert capture.fps == 3.0
        print("  ✓ ScreenCapture initialized correctly")
    except Exception as e:
        print(f"  ✗ ScreenCapture error: {e}")
        return False
    
    # Test OCRExtractor
    print("Testing OCRExtractor...")
    try:
        extractor = OCRExtractor(languages=['en'])
        stats = extractor.get_buffer_stats()
        assert stats['entry_count'] == 0
        print("  ✓ OCRExtractor initialized correctly")
    except Exception as e:
        print(f"  ✗ OCRExtractor error: {e}")
        return False
    
    # Test ContextAnalyzer
    print("Testing ContextAnalyzer...")
    try:
        analyzer = ContextAnalyzer(analysis_interval=10.0)
        context = analyzer.get_current_context()
        assert 'activity' in context
        print("  ✓ ContextAnalyzer initialized correctly")
    except Exception as e:
        print(f"  ✗ ContextAnalyzer error: {e}")
        return False
    
    print()
    print("All basic tests passed! ✓")
    return True


if __name__ == "__main__":
    # Run basic tests if executed directly
    success = run_basic_tests()
    sys.exit(0 if success else 1)
