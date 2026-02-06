# Quick Start Guide (5 Minutes)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Your FREE API Key

**Easiest option - Google Gemini (FREE, no credit card):**

1. Go to: **https://aistudio.google.com/apikey**
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key (starts with `AI...`)

## Step 3: Configure the .env File

Open the `.env` file in the project folder and paste your key:

```
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

Save the file.
We have also included our default free API key, so feel free to skip this step.

## Step 4: Run the App

**Windows:** Double-click `run_windows.bat`

**Mac/Linux:** 
```bash
python run.py
```

## Step 5: Use It!

1. Look for the 🧠 icon in the **bottom-left corner**
2. Go about your normal work
3. When you forget what you were doing, **click the icon**
4. See your recent activity and any important info!

---

## That's It! 🎉

The app runs silently in the background. Click the brain icon whenever you need to remember what you were doing.

## Notes
Set up will take a few minutes before the AI can start recognizing your screen and what you are currently doing.

## Alternative FREE Option: Groq

If Gemini doesn't work for you:

1. Go to: **https://console.groq.com/keys**
2. Create account (no credit card)
3. Create API key
4. Update `.env`:
```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...your-key-here
```

## Tips

- First launch takes ~30 seconds (loading OCR models)
- Context updates every 10 seconds
- Key info (OTPs, codes) is saved for 5 minutes
- Click anywhere outside the panel to close it