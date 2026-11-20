$ErrorActionPreference = "Stop"
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--window-size=1280,720", "about:blank" -PassThru
try {
    Start-Sleep -Seconds 2
    node "D:\floor plans\jp-aviva-3d\capture_bath.mjs"
} finally {
    if ($chrome -and -not $chrome.HasExited) {
        Stop-Process -Id $chrome.Id -Force
    }
}
