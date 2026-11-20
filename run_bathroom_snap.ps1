$ErrorActionPreference = "Stop"

Write-Host "Stopping existing chrome instances..."
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "Starting Chrome headless on port 9222..."
$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--remote-allow-origins=*", "--window-size=1920,1080", "about:blank" -PassThru

try {
    Start-Sleep -Seconds 3
    Write-Host "Running node test_bathroom_snap.mjs..."
    node "D:\floor plans\jp-aviva-3d\test_bathroom_snap.mjs"
} finally {
    Write-Host "Stopping Chrome..."
    if ($chrome -and -not $chrome.HasExited) {
        Stop-Process -Id $chrome.Id -Force
    }
}

Write-Host "Bathroom snapshot test finished successfully!"
