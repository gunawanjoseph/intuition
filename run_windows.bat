@echo off
REM Memory Context Overlay - Windows Launcher
REM Double-click this file to start the application

echo ================================================
echo Memory Context Overlay
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

REM Check for API key
if "%OPENAI_API_KEY%"=="" (
    echo WARNING: OPENAI_API_KEY environment variable not set!
    echo.
    echo Please set your OpenAI API key before running:
    echo   set OPENAI_API_KEY=your-api-key-here
    echo.
    echo Or set it permanently in System Environment Variables.
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 0
)

REM Run the application
cd /d "%~dp0"
python run.py

pause
