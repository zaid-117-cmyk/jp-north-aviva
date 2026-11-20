$chrome = Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--headless=new", "--remote-debugging-port=9222", "--window-size=1600,900", "about:blank" -PassThru
Start-Sleep -Seconds 3
node "d:\floor plans\jp-aviva-3d\capture_all_photorealism.mjs"
Stop-Process -Id $chrome.Id -Force
