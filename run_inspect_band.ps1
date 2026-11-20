Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--remote-allow-origins=*", "--window-size=1920,1080", "http://localhost:8080/" -PassThru
Start-Sleep -Seconds 4
try {
    node "D:\floor plans\jp-aviva-3d\inspect_band.mjs"
} finally {
    Stop-Process -Id $chrome.Id -Force
}
