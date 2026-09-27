# Reads the Telegram bot token from the clipboard and saves it for the Telegram plugin.
# The token never appears on screen or in any Claude chat.
$t = Get-Clipboard -Raw
if ($t) { $t = $t.Trim().Trim('<', '>', ' ') }
if ($t -notmatch '^\d{6,}:[A-Za-z0-9_-]{30,}$') {
    Write-Host ''
    Write-Host '  That is not a bot token. Copy the token from BotFather and run this again.' -ForegroundColor Red
    exit 1
}
$dir = Join-Path $env:USERPROFILE '.claude\channels\telegram'
New-Item -ItemType Directory -Force $dir | Out-Null
[IO.File]::WriteAllText((Join-Path $dir '.env'), "TELEGRAM_BOT_TOKEN=$t`n", (New-Object Text.UTF8Encoding($false)))
Set-Clipboard -Value ' '
Write-Host ''
Write-Host '  Saved! The token is stored on this PC only. Clipboard cleared.' -ForegroundColor Green
