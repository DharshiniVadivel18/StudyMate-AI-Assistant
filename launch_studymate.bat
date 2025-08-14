@echo off
title StudyMate - AI Academic Assistant
color 0A

echo.
echo  ========================================
echo   🎓 StudyMate - AI Academic Assistant
echo  ========================================
echo.
echo  Starting StudyMate server...
echo  Please wait while the application loads...
echo.

cd /d "%~dp0"

echo  📂 Current directory: %CD%
echo  🚀 Launching Streamlit server...
echo.

python -m streamlit run app.py --server.port 8501 --server.headless false --browser.gatherUsageStats false

echo.
echo  ✅ StudyMate has been launched!
echo  🌐 Access at: http://localhost:8501
echo.
echo  Press any key to close this window...
pause >nul
