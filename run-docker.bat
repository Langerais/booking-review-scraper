@echo off
setlocal

echo [*] Launching Booking Review Assistant (Docker)...

for %%I in ("settings.json") do set FULL_PATH=%%~fI

docker run -it -v "%FULL_PATH%:/app/settings.json" booking-review-summarizer
