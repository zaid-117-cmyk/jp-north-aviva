$ErrorActionPreference = "Stop"
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "http://localhost:8080/" -PassThru
Start-Sleep -Seconds 3
try {
    node "D:\floor plans\jp-aviva-3d\debug_walls.mjs"
} finally {
    if ($chrome -and -not $chrome.HasExited) {
        Stop-Process -Id $chrome.Id -Force
    }
}
