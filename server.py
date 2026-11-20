import http.server
import socketserver
import json
import base64
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/save_snapshot':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            filename = payload.get('filename', 'snapshot.png')
            img_b64 = payload.get('image', '')

            if ',' in img_b64:
                img_b64 = img_b64.split(',', 1)[1]

            filepath = os.path.join(DIRECTORY, filename)
            data_bytes = base64.b64decode(img_b64)
            with open(filepath, 'wb') as f:
                f.write(data_bytes)

            brain_filepath = os.path.join(r"C:\Users\ADMIN\.gemini\antigravity\brain\ba763b61-d8cc-448d-88e4-7b9f23b03879", filename)
            try:
                with open(brain_filepath, 'wb') as f:
                    f.write(data_bytes)
            except Exception:
                pass

            print(f"Saved snapshot: {filepath} ({len(img_b64)} b64 chars)")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'saved': filepath}).encode('utf-8'))
            self.close_connection = True
            return

        if self.path == '/save_gltf':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            filename = payload.get('filename', 'jp_north_aviva_blender_export.glb')
            data_b64 = payload.get('data', '')

            if ',' in data_b64:
                data_b64 = data_b64.split(',', 1)[1]

            filepath = os.path.join(DIRECTORY, filename)
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(data_b64))

            print(f"Exported scene for Blender: {filepath} ({len(data_b64)} b64 chars)")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'saved': filepath}).encode('utf-8'))
            self.close_connection = True
            return
        super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == '__main__':
    httpd = ThreadedHTTPServer(("", PORT), CustomHandler)
    print(f"Serving at http://localhost:{PORT} from {DIRECTORY}")
    httpd.serve_forever()
