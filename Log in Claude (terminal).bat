@echo off
title Log in Claude (terminal)
for /f "delims==" %%V in ('set CLAUDE 2^>nul') do set "%%V="
set "ANTHROPIC_BASE_URL="
echo.
echo  A browser page will open. Approve with your Claude account (the same one as the Claude app).
echo  If asked how to log in, pick your Claude subscription (Claude.ai account), not an API key.
echo.
claude auth login
echo.
claude auth status
echo.
echo  Done. Close this window, then double-click "Start Brain (Telegram)".
pause
