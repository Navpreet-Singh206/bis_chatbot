@echo off
echo === BIS Chatbot Backend Setup - Groq Fix ===
REM Ensure venv exists and activate
if not exist venv (
    echo Creating new virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Virtual environment activated.

REM Upgrade pip and install requirements with force for groq
echo Installing/upgrading dependencies (forcing groq)...
pip install --upgrade pip
pip install -r requirements.txt --upgrade
pip install groq --force-reinstall --no-cache-dir
pip install fastapi uvicorn python-dotenv scikit-learn numpy google-generativeai --upgrade
echo Dependencies complete.

REM Verify groq installed
pip list | findstr groq
if errorlevel 1 (
    echo FATAL: groq installation failed! Install manually: pip install groq
    pause
    exit /b 1
)
echo Groq verified OK!

REM Run FastAPI from backend dir
cd /d backend
echo Starting server from backend/: http://localhost:8000
echo Test health: curl http://localhost:8000/health
uvicorn api.main_fixed:app --host 0.0.0.0 --port 8000 --reload
pause
