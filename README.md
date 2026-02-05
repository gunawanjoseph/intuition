# MindTrace

**MindTrace** is a desktop accessibility tool designed to help users with ADHD, dementia, or high cognitive load stay focused. It acts as a persistent digital memory, providing instant context about your recent activities with a single click.


## The Problem

In today's digital world, a single notification can derail a task, leading to a 23-minute struggle to refocus. For individuals with ADHD or dementia, this problem is magnified, turning simple digital tasks like online banking or booking appointments into frustrating challenges. The constant need to switch between apps (e.g., for a one-time password) breaks concentration and leads to task abandonment.

## The Solution

MindTrace provides a **cognitive safety net**. It runs quietly in the background, observing your on-screen activity. When you get distracted and lose your train of thought, a single click on the persistent MindTrace icon brings up a panel summarizing exactly what you were doing and highlighting key information like OTPs, names, or confirmation numbers.

## Key Features

- **Persistent Overlay**: A small, non-intrusive 🧠 icon is always visible in the corner of your screen.
- **Continuous Screen Monitoring**: Captures screen content at ~3 FPS, maintaining a rolling 1-minute context window.
- **Smart Context Analysis**: Uses an LLM (like Google Gemini, Groq, or OpenAI) to analyze extracted text every 10-60 seconds, identifying the current task and key information.
- **Instant Recall Panel**: On-click panel displays:
    - **Activity Summary**: "You were doing: [task description] using [app name]"
    - **Key Information**: A list of detected OTPs, verification codes, names, links, prices, etc.
- **Privacy-First**: All screen capture and OCR processing happens locally on your device.
- **Multi-Provider LLM Support**: Easily switch between free (Gemini, Groq) and paid (OpenAI) language models.

## Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **GUI / Overlay** | PyQt6 | For the cross-platform persistent icon and info panel. |
| **Screen Capture** | `mss` | High-performance, low-overhead screen grabbing. |
| **Text Extraction** | `EasyOCR` | Local, offline-capable OCR to read text from images. |
| **AI Context** | `google-genai`, `groq`, `openai` | Flexible LLM integration for context analysis. |
| **Configuration** | `python-dotenv` | Easy management of API keys and settings. |
| **Language** | Python 3.9+ | The core language of the application. |

---

## Setup and Installation

Follow these steps to get MindTrace running on your system.

### 1. Prerequisites

- **Python 3.9+**: Ensure you have Python installed. On macOS, you will likely use the `python3` command. You can download it from [python.org](https://python.org/downloads/).

### 2. Clone the Repository

First, get the project files onto your local machine.

```bash
# Example: If you have the files in a zip, unzip them first.
# Or if it's a git repository:
# git clone https://github.com/your-repo/mindtrace.git
# cd mindtrace
```

### 3. Set Up a Virtual Environment (Recommended)

Using a virtual environment prevents conflicts with system-wide packages. This is **required on modern macOS**.

```bash
# Navigate to the project directory
cd /path/to/your/project

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 4. Install Dependencies

Once the virtual environment is active, install the required Python packages.

```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key

MindTrace needs an LLM API key to understand your context.

1.  **Copy the example `.env` file**:
    ```bash
    cp .env.example .env
    ```
2.  **Get a FREE API Key**:
    - **Groq (Recommended)**: Go to [console.groq.com/keys](https://console.groq.com/keys). It's extremely fast and has a generous free tier.
    - **Google Gemini**: Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
3.  **Edit the `.env` file** and add your key:

    ```ini
    # LLM_PROVIDER can be 'groq', 'gemini', or 'openai'
    LLM_PROVIDER=groq

    # --- API KEYS (only fill the one you are using) ---
    GROQ_API_KEY=gsk_your_groq_api_key_here
    GEMINI_API_KEY=AIzaSy_your_gemini_api_key_here
    OPENAI_API_KEY=
    ```

---

## Usage

With your virtual environment active and `.env` file configured, run the application:

```bash
python run.py
```

- The first time you run it, EasyOCR may need to download its language models (this can take a few minutes).
- Once initialized, you will see the 🧠 icon in the bottom-left corner of your screen.
- Click the icon at any time to see your current context!
- To quit the application, press `Ctrl+C` in the terminal.

## Configuration

You can customize the app's behavior by editing `config.py`:

- `CAPTURE_FPS`: How many times per second to capture the screen (default: `3.0`).
- `ANALYSIS_INTERVAL`: How often (in seconds) to send screen text to the LLM for analysis (default: `10.0`). Increase this to reduce API usage.

## File Architecture

```
. (root)
├── .env                  # Your private API keys and settings
├── .env.example          # Template for the .env file
├── README.md             # This file
├── QUICKSTART.md         # A shorter guide to get started
├── config.py             # Application settings (FPS, intervals)
├── requirements.txt      # List of Python dependencies
├── run.py                # Main executable script to launch the app
├── run_unix.sh           # Launcher script for macOS/Linux
└── run_windows.bat       # Launcher script for Windows
│
└── src/                  # Source code directory
    ├── __init__.py
    ├── context_analyzer.py # Handles LLM communication and context analysis
    ├── gui_overlay.py      # Manages the PyQt6 icon and info panel
    ├── main.py             # Integrates all components and runs the main app loop
    ├── ocr_extractor.py    # Extracts text from screen captures using EasyOCR
    └── screen_capture.py   # Manages the screen capture thread

```
