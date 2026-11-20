import json
import os
import subprocess
import time
import urllib.request
import websocket
import base64

artifact_dir = r"C:\Users\ADMIN\.gemini\antigravity\brain\a89496f6-6f7c-4a3f-b45b-cae80fa0337c"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = r"C:\Users\ADMIN\AppData\Local\Temp\chrome_test_kitchen"

print("Starting headless Chrome...")
proc = subprocess.Popen([
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    f"--user-data-dir={user_data}",
    "--window-size=1920,1080",
    "--disable-gpu-vsync",
    "http://localhost:8080"
])

time.sleep(3)

try:
    tabs = json.loads(urllib.request.urlopen("http://localhost:9222/json").read().decode("utf-8"))
    tab = [t for t in tabs if "localhost:8080" in t.get("url", "") or t.get("type") == "page"][0]
    ws_url = tab["webSocketDebuggerUrl"]
    ws = websocket.create_connection(ws_url)

    msg_id = 1
    def send(method, params=None):
        global msg_id
        mid = msg_id
        msg_id += 1
        msg = {"id": mid, "method": method}
        if params:
            msg["params"] = params
        ws.send(json.dumps(msg))
        while True:
            res = json.loads(ws.recv())
            if res.get("id") == mid:
                return res

    print("Waiting for Three.js initialization...")
    for _ in range(20):
        res = send("Runtime.evaluate", {"expression": "typeof window.applyProgressToScene === 'function'"})
        if res.get("result", {}).get("result", {}).get("value") is True:
            break
        time.sleep(1)

    shots = [
        ("kitchen_overhaul_046", 0.46),
        ("kitchen_overhaul_049", 0.49),
    ]

    for name, p in shots:
        print(f"Applying progress {p:.2f} for {name}...")
        send("Runtime.evaluate", {"expression": f"window.applyProgressToScene({p:.4f});"})
        time.sleep(0.6)
        shot = send("Page.captureScreenshot", {"format": "jpeg", "quality": 92})
        data = shot.get("result", {}).get("data")
        if data:
            out_path = os.path.join(artifact_dir, f"{name}.jpg")
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(data))
            print(f"Saved: {out_path} ({os.path.getsize(out_path)} bytes)")

    ws.close()
finally:
    proc.terminate()
    proc.wait()
    print("Chrome terminated.")
