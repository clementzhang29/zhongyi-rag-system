@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================
echo  中医国学 RAG 系统
echo ==========================================
echo.
echo 启动前请先配置 config.yaml 中的 API key
echo.
python run.py
pause
