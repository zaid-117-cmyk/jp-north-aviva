@echo off
title JP North Aviva - 3D Walkthrough Server
cd /d "%~dp0"
echo ========================================================
echo   JP NORTH AVIVA - 3D ARCHITECTURAL WALKTHROUGH
echo   Starting local server at http://localhost:8080
echo ========================================================
echo.

start "" "http://localhost:8080"

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python -m http.server 8080
    goto :eof
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -m http.server 8080
    goto :eof
)

where npx >nul 2>nul
if %ERRORLEVEL% equ 0 (
    npx http-server -p 8080
    goto :eof
)

echo [ERROR] Neither Python nor Node.js was found in your PATH.
echo Please install Python (https://www.python.org/) or Node.js to start the server.
pause
