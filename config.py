"""
Memory Context Overlay - Configuration
Modify these settings to customize the application behavior.
"""

# Screen Capture Settings
CAPTURE_FPS = 3.0  # Frames per second for screen capture
BUFFER_DURATION = 60  # Seconds of screen history to keep

# OCR Settings
OCR_LANGUAGES = ['en']  # Languages for text recognition
OCR_PROCESS_INTERVAL = 1.0  # Seconds between OCR processing

# LLM Analysis Settings
ANALYSIS_INTERVAL = 10.0  # Seconds between LLM context analysis
LLM_MODEL = "gpt-4.1-mini"  # OpenAI model to use
LLM_TEMPERATURE = 0.3  # Lower = more focused responses
LLM_MAX_TOKENS = 500  # Maximum response length

# GUI Settings
ICON_SIZE = 48  # Size of the overlay icon in pixels
ICON_POSITION = "bottom-left"  # Position: bottom-left, bottom-right, top-left, top-right
PANEL_WIDTH = 400  # Width of the info panel
PANEL_HEIGHT = 450  # Height of the info panel
KEY_EVENTS_DISPLAY_COUNT = 10  # Number of key events to show in panel

# Colors (RGBA format)
ICON_COLOR = (70, 130, 180, 200)  # Steel blue
PANEL_BACKGROUND = (30, 30, 40, 245)  # Dark blue-gray
PANEL_BORDER = (70, 130, 180, 150)  # Steel blue border
TEXT_PRIMARY = (255, 255, 255, 255)  # White
TEXT_SECONDARY = (176, 176, 176, 255)  # Light gray
TEXT_ACCENT = (135, 206, 235, 255)  # Sky blue

# Key Information Types to Detect
KEY_INFO_TYPES = [
    'otp',  # One-time passwords, verification codes
    'email',  # Email addresses
    'phone',  # Phone numbers
    'name',  # Names of people or companies
    'url',  # URLs and links
    'price',  # Prices and monetary amounts
    'date',  # Dates and times
    'order',  # Order numbers, tracking numbers
    'code',  # Various codes (promo, reference, etc.)
]

# Debug Settings
DEBUG_MODE = False  # Enable verbose logging
SAVE_SCREENSHOTS = False  # Save captured screenshots (for debugging)
SCREENSHOT_DIR = "debug_screenshots"  # Directory for saved screenshots
