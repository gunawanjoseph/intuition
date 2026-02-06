# Memory Context Overlay

A desktop application designed to help users with ADHD or dementia stay focused by providing context about what they were doing. When you get distracted by a notification or lose focus, simply click the overlay icon to instantly recall your recent activity.

## Features

- **Persistent Overlay Icon**: A small, always-visible brain icon (🧠) in the bottom-left corner of your screen
- **Continuous Screen Monitoring**: Captures screen content at ~3 FPS, maintaining a rolling 1-minute context window
- **Smart Text Extraction**: Uses EasyOCR to extract text from screen captures
- **AI-Powered Context Analysis**: Every ~10 seconds, analyzes screen content to understand what you're doing
- **Multiple FREE LLM Options**: Choose from Google Gemini (free), Groq (free), or OpenAI (paid)
- **Key Information Detection**: Automatically detects and stores important information like:
  - OTP/verification codes
  - Email addresses
  - Phone numbers
  - Names
  - URLs/links
  - Prices
  - Order/tracking numbers
- **Info Panel**: Click the icon to see:
  - Activity Summary: "You were doing: [task] using [app]"
  - Key Information: List of detected important items

## Requirements

- **Python**: 3.9 or higher
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux with X11
- **API Key**: Free options available (see below)
- **Display**: Works best with a single monitor setup

## Installation

### 1. Clone or Download

Download and extract the project files to your preferred location.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key (Easy!)

**Edit the `.env` file** in the project folder. Choose ONE of these FREE options:

#### Option A: Google Gemini (Recommended - FREE)
1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key" (no credit card needed!)
3. Copy the key
4. Paste it in `.env`:
```
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-actual-key-here
```

#### Option B: Groq (FREE)
1. Go to https://console.groq.com/keys
2. Create an account (no credit card needed!)
3. Create a new API key
4. Paste it in `.env`:
```
LLM_PROVIDER=groq
GROQ_API_KEY=your-actual-key-here
```

#### Option C: OpenAI (Paid)
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Paste it in `.env`:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your-actual-key-here
```

## Usage

### Quick Start

**Windows:** Double-click `run_windows.bat`

**macOS/Linux:**
```bash
./run_unix.sh
# or
python run.py
```

### How It Works

1. **Launch**: Start the application using one of the methods above
2. **Look for the Icon**: A 🧠 icon appears in the bottom-left corner of your screen
3. **Continue Working**: The app silently monitors your screen in the background
4. **Get Context**: When you need to remember what you were doing, click the icon
5. **View Info Panel**: See your recent activity and any important information detected

### Info Panel Sections

- **Activity Summary**: Describes what you were doing (e.g., "Writing an email to John about the project deadline")
- **Application**: Shows which app/website you were using (e.g., "Gmail - Chrome")
- **Key Information**: Lists important items with icons:
  - 🔐 OTP/Verification codes
  - 📧 Email addresses
  - 📞 Phone numbers
  - 👤 Names
  - 🔗 URLs/Links
  - 💰 Prices/Amounts
  - 📅 Dates
  - 📦 Order/Tracking numbers

## Configuration

### Environment Variables (.env file)

| Variable | Description | Required |
|----------|-------------|----------|
| `LLM_PROVIDER` | Which AI to use: `gemini`, `groq`, or `openai` | Yes |
| `GEMINI_API_KEY` | Your Google Gemini API key | If using Gemini |
| `GROQ_API_KEY` | Your Groq API key | If using Groq |
| `OPENAI_API_KEY` | Your OpenAI API key | If using OpenAI |

### Advanced Settings (config.py)

```python
# Screen capture frequency
CAPTURE_FPS = 1.0

# How long to keep history
BUFFER_DURATION = 60  # seconds

# How often to analyze context
ANALYSIS_INTERVAL = 30.0  # seconds

# Icon position
ICON_POSITION = "bottom-left"
```

## Project Structure

```
memory_context_overlay/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py               # Main application entry point
│   ├── screen_capture.py     # Screen capture module
│   ├── ocr_extractor.py      # OCR text extraction
│   ├── context_analyzer.py   # LLM context analysis (multi-provider)
│   └── gui_overlay.py        # PyQt6 GUI components
├── tests/                    # Unit tests
├── .env                      # ⬅️ PUT YOUR API KEY HERE
├── .env.example              # Template for .env
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── run.py                    # Python launcher script
├── run_windows.bat           # Windows launcher
├── run_unix.sh               # macOS/Linux launcher
└── README.md                 # This file
```

## Troubleshooting

### "API KEY NOT CONFIGURED"
Edit the `.env` file and add your API key. See the Installation section above.

### Icon not appearing
- Check if another application is using the bottom-left corner
- Try restarting the application
- On Linux, ensure you're running an X11 session (Wayland may have issues)

### OCR is slow
- EasyOCR loads models on first use, which can take 30-60 seconds
- Subsequent extractions are much faster
- Consider reducing `CAPTURE_FPS` in config.py

### High CPU usage
- Reduce `CAPTURE_FPS` to 1.0 or 2.0
- Increase `ANALYSIS_INTERVAL` to 15.0 or 20.0

### Panel shows "Analyzing your activity..."
- Wait for the first analysis cycle (up to 10 seconds)
- Check that your API key is valid in the `.env` file
- Look at the terminal for error messages

## Privacy & Security

- **Local Processing**: Screen captures are processed locally and never uploaded
- **API Calls**: Only extracted text is sent to the LLM for analysis
- **No Storage**: Screenshots are not saved to disk (unless debug mode is enabled)
- **Rolling Buffer**: Old data is automatically discarded after 60 seconds

## LLM Provider Comparison

| Provider | Cost | Speed | Quality | Credit Card Required |
|----------|------|-------|---------|---------------------|
| **Gemini** | FREE | Fast | Excellent | No |
| **Groq** | FREE | Very Fast | Good | No |
| **OpenAI** | ~$0.10-0.50/day | Fast | Excellent | Yes |

## Known Limitations

- Single monitor support (uses primary monitor)
- English text recognition only (can be extended in config)
- Requires active internet connection for LLM analysis
- May not work well with very fast-changing content (videos, games)

## License

This project is provided as-is for personal use. Feel free to modify and extend it for your needs.

---

**Remember**: This tool is designed to help, not to replace good focus habits. Use it as a safety net when you get distracted, and consider combining it with other focus techniques like the Pomodoro method.
