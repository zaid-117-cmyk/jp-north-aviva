# test_transition_snapshots.py
import json
import time
import base64
import urllib.request
import subprocess
import websocket

# Kill any existing chrome
subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue"])
time.sleep(1)

# Start Chrome headless on 9222
chrome_proc = subprocess.Popen([
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    "--window-size=1280,720",
    "http://localhost:8080/"
])
time.sleep(3)

try:
    # Get debugger websocket url
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    targets = json.loads(req.read().decode())
    page_target = next(t for t in targets if t.get("type") == "page" and "8080" in t.get("url", ""))
    ws_url = page_target["webSocketDebuggerUrl"]

    ws = websocket.create_connection(ws_url)
    msg_id = 1

    def send(method, params=None):
        global msg_id
        payload = {"id": msg_id, "method": method, "params": params or {}}
        msg_id += 1
        ws.send(json.dumps(payload))
        while True:
            res = json.loads(ws.recv())
            if res.get("id") == payload["id"]:
                if "error" in res:
                    raise Exception(res["error"])
                return res.get("result", {})

    send("Runtime.enable")
    send("Page.enable")
    time.sleep(2)

    # Prepare HUD
    send("Runtime.evaluate", {
        "expression": """
            window.isCapturing = true;
            if (window.closeRoomCard) window.closeRoomCard();
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'none';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'none';
            const btn = document.getElementById('room-plus-btn');
            if (btn) btn.style.display = 'none';
            renderer.setSize(1280, 720);
            composer.setSize(1280, 720);
            camera.aspect = 1280 / 720;
            camera.updateProjectionMatrix();
        """
    })

    test_points = [
        (0.34, "stop2_living_hold"),
        (0.40, "trans_living_to_kitchen_passage"),
        (0.44, "trans_kitchen_portal_entry"),
        (0.49, "stop3_kitchen_hold"),
        (0.56, "trans_kitchen_to_bath"),
        (0.625, "stop4_bath_hold"),
        (0.70, "trans_bath_to_bed_doorway"),
        (0.775, "stop5_bed_hold"),
        (0.81, "trans_bed_to_balc_hub"),
        (0.83, "trans_bed_to_balc_open_portal"),
        (0.85, "trans_bed_to_balc_living_corridor"),
        (0.88, "trans_bed_to_balc_slider_approach"),
        (0.905, "stop6_balc_hold"),
        (0.98, "stop7_sunset_hold")
    ]

    for p, name in test_points:
        send("Runtime.evaluate", {"expression": f"window.applyProgressToScene({p:.4f});"})
        time.sleep(0.1)
        shot = send("Page.captureScreenshot", {"format": "jpeg", "quality": 92})
        img_data = base64.b64decode(shot["data"])
        out_path = f"C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c/verify_{name}.jpg"
        with open(out_path, "wb") as f:
            f.write(img_data)
        print(f"Captured p={p:.3f} -> verify_{name}.jpg")

    ws.close()
    print("All verification snapshots captured successfully!")

finally:
    chrome_proc.terminate()
