$ErrorActionPreference = "Stop"

Write-Host "Stopping any previous Chrome instances..."
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "Starting Chrome in Headless New mode on port 9222..."
$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--window-size=1280,720", "about:blank" -PassThru

try {
    Start-Sleep -Seconds 3
    Write-Host "Running verify_hotspots_and_glare.mjs..."
    node "D:\floor plans\jp-aviva-3d\verify_hotspots_and_glare.mjs"
} finally {
    Write-Host "Stopping Chrome..."
    if ($chrome -and -not $chrome.HasExited) {
        Stop-Process -Id $chrome.Id -Force
    }
}

Write-Host "Verification completed successfully!"
