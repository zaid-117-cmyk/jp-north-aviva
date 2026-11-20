Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$proc = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--window-size=1600,900", "http://localhost:8080/" -PassThru
Start-Sleep -Seconds 4
node "D:\floor plans\jp-aviva-3d\capture_transitions_audit.mjs"
Stop-Process -Id $proc.Id -Force
