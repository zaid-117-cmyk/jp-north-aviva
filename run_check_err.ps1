$ErrorActionPreference = "Stop"
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--remote-allow-origins=*", "--window-size=1920,1080", "about:blank" -PassThru

try {
    Start-Sleep -Seconds 3
    node "D:\floor plans\jp-aviva-3d\inspect_console.mjs"
} finally {
    if ($chrome -and -not $chrome.HasExited) {
        Stop-Process -Id $chrome.Id -Force
    }
}
