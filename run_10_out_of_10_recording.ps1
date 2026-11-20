$ErrorActionPreference = "Stop"

Write-Host "Starting Chrome in Headless New mode on port 9222..."
$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--window-size=1280,720", "about:blank" -PassThru

try {
    Start-Sleep -Seconds 3
    Write-Host "Running render_10_out_of_10_video.mjs..."
    node "D:\floor plans\jp-aviva-3d\render_10_out_of_10_video.mjs"
} finally {
    Write-Host "Stopping Chrome..."
    if ($chrome -and -not $chrome.HasExited) {
        Stop-Process -Id $chrome.Id -Force
    }
}

Write-Host "10/10 Video recording pipeline completed successfully!"
