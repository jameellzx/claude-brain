@echo off
title Save Telegram Token
echo.
echo  1. In Telegram, open BotFather and COPY your bot token (the long 123456:ABC... text).
echo  2. Come back here and press any key.
echo.
pause >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\dev\brain\scripts\save_token.ps1"
echo.
echo  Next: close the old Brain window, then double-click "Start Brain (Telegram)".
echo.
pause
