"""
OCR Text Extraction Module
Uses EasyOCR to extract text from screen captures.
"""

import easyocr
import threading
from typing import Optional, List, Tuple
from PIL import Image
import numpy as np
from collections import deque
from datetime import datetime
import time


class OCRExtractor:
    """
    Extracts text from images using EasyOCR.
    Maintains a rolling buffer of extracted text.
    """
    
    def __init__(self, languages: List[str] = ['en'], buffer_duration: int = 60):
        """
        Initialize the OCR extractor.
        
        Args:
            languages: List of language codes for OCR
            buffer_duration: Duration in seconds to keep text in buffer
        """
        self.languages = languages
        self.buffer_duration = buffer_duration
        
        # Rolling buffer for extracted text: (timestamp, text, confidence)
        self.text_buffer = deque(maxlen=200)  # Keep last 200 extractions
        
        # EasyOCR reader (lazy initialization)
        self._reader: Optional[easyocr.Reader] = None
        self._reader_lock = threading.Lock()
        self._buffer_lock = threading.Lock()
        
        # Processing queue
        self._processing = False
        self._last_extraction_time = None
    
    def _get_reader(self) -> easyocr.Reader:
        """Get or create the EasyOCR reader (thread-safe)."""
        if self._reader is None:
            with self._reader_lock:
                if self._reader is None:
                    print("[OCR] Initializing EasyOCR reader (this may take a moment)...")
                    self._reader = easyocr.Reader(
                        self.languages,
                        gpu=False,  # Use CPU for broader compatibility
                        verbose=False
                    )
                    print("[OCR] EasyOCR reader initialized")
        return self._reader
    
    def extract_text(self, image: Image.Image) -> Tuple[str, float]:
        """
        Extract text from a PIL Image.
        
        Args:
            image: PIL Image to extract text from
            
        Returns:
            Tuple of (extracted_text, average_confidence)
        """
        try:
            # Convert PIL Image to numpy array
            img_array = np.array(image)
            
            # Get reader
            reader = self._get_reader()
            
            # Perform OCR
            results = reader.readtext(img_array)
            
            if not results:
                return "", 0.0
            
            # Extract text and calculate average confidence
            texts = []
            confidences = []
            
            for (bbox, text, confidence) in results:
                texts.append(text)
                confidences.append(confidence)
            
            full_text = " ".join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return full_text, avg_confidence
            
        except Exception as e:
            print(f"[OCR] Extraction error: {e}")
            return "", 0.0
    
    def process_frame(self, timestamp: datetime, image: Image.Image) -> Optional[str]:
        """
        Process a frame and add extracted text to buffer.
        
        Args:
            timestamp: Timestamp of the frame
            image: PIL Image to process
            
        Returns:
            Extracted text or None if skipped
        """
        # Skip if already processing or too soon since last extraction
        if self._processing:
            return None
        
        # Rate limit: process at most once per second
        if self._last_extraction_time:
            elapsed = (datetime.now() - self._last_extraction_time).total_seconds()
            if elapsed < 1.0:
                return None
        
        self._processing = True
        try:
            text, confidence = self.extract_text(image)
            
            if text.strip():
                with self._buffer_lock:
                    self.text_buffer.append({
                        'timestamp': timestamp,
                        'text': text,
                        'confidence': confidence
                    })
                
                self._last_extraction_time = datetime.now()
                return text
            
            return None
            
        finally:
            self._processing = False
    
    def get_recent_text(self, seconds: float = 60) -> List[dict]:
        """
        Get text extracted in the last N seconds.
        
        Args:
            seconds: Number of seconds to look back
            
        Returns:
            List of text extraction records
        """
        cutoff = datetime.now().timestamp() - seconds
        
        with self._buffer_lock:
            return [
                record for record in self.text_buffer
                if record['timestamp'].timestamp() >= cutoff
            ]
    
    def get_combined_text(self, seconds: float = 60) -> str:
        """
        Get all text from the last N seconds combined.
        
        Args:
            seconds: Number of seconds to look back
            
        Returns:
            Combined text string
        """
        records = self.get_recent_text(seconds)
        
        # Deduplicate similar text entries
        seen_texts = set()
        unique_texts = []
        
        for record in records:
            # Simple deduplication: check if text is substantially different
            text = record['text'].strip()
            text_key = text[:50].lower()  # Use first 50 chars as key
            
            if text_key not in seen_texts:
                seen_texts.add(text_key)
                unique_texts.append(text)
        
        return "\n".join(unique_texts)
    
    def get_buffer_stats(self) -> dict:
        """Get statistics about the text buffer."""
        with self._buffer_lock:
            if not self.text_buffer:
                return {
                    'entry_count': 0,
                    'total_characters': 0,
                    'avg_confidence': 0.0
                }
            
            total_chars = sum(len(r['text']) for r in self.text_buffer)
            avg_conf = sum(r['confidence'] for r in self.text_buffer) / len(self.text_buffer)
            
            return {
                'entry_count': len(self.text_buffer),
                'total_characters': total_chars,
                'avg_confidence': avg_conf
            }


# Test function
if __name__ == "__main__":
    print("Testing OCR Extractor Module...")
    
    # Create a simple test image with text
    from PIL import Image, ImageDraw, ImageFont
    
    # Create test image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    draw.text((50, 50), "Hello World!", fill='black')
    draw.text((50, 100), "This is a test of the OCR system.", fill='black')
    draw.text((50, 150), "Verification Code: 123456", fill='black')
    draw.text((50, 200), "Email: test@example.com", fill='black')
    
    # Test extraction
    extractor = OCRExtractor()
    text, confidence = extractor.extract_text(img)
    
    print(f"Extracted text: {text}")
    print(f"Confidence: {confidence:.2f}")
    print("Test complete!")
