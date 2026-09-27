@echo off
title Brain (Telegram)
rem Clear settings inherited from other Claude sessions so this window uses its own login.
for /f "delims==" %%V in ('set CLAUDE 2^>nul') do set "%%V="
set "ANTHROPIC_BASE_URL="
rem The newer MCP runtime does not start the Telegram connection; use the older one.
set "MCP_SDK_GENERATION=v1"
set "PATH=%LOCALAPPDATA%\Microsoft\WinGet\Packages\Oven-sh.Bun_Microsoft.Winget.Source_8wekyb3d8bbwe\bun-windows-x64;%USERPROFILE%\.bun\bin;%PATH%"
cd /d C:\dev\brain
echo Starting your Brain. Keep this window open so it can answer Telegram.
echo Close this window to stop it.
echo.
rem The Telegram connection starts after the first message, so send one right away.
claude "Brain online. Reply with just: ready. Then wait for Telegram messages." --channels plugin:telegram@claude-plugins-official
pause
