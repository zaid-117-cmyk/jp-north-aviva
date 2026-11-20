$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--window-size=1600,900", "http://localhost:8080/" -PassThru
Start-Sleep -Seconds 4
node "D:\floor plans\jp-aviva-3d\verify_ui_contrast_and_hotspots.mjs"
Stop-Process -Id $chrome.Id -Force
