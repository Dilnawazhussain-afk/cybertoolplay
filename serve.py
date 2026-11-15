"""
serve.py  -  CyberShield website ko apne computer par chalane ke liye.

Chalane ka tarika (VS Code terminal me):
    python serve.py

Phir browser me apne aap ye link khulega:
    http://localhost:8000
"""

import http.server     # built-in web server
import socketserver    # server ko network par chalane ke liye
import webbrowser      # browser apne aap kholne ke liye
import os

PORT = 8000

# Is file wale folder me jao, taaki index.html mil sake
os.chdir(os.path.dirname(os.path.abspath(__file__)))

handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), handler) as server:
    url = f"http://localhost:{PORT}"
    print("=" * 40)
    print(" CyberShield website chal rahi hai!")
    print(f" Link: {url}")
    print(" Band karne ke liye: Ctrl + C dabao")
    print("=" * 40)
    webbrowser.open(url)      # browser me website khol do
    try:
        server.serve_forever()   # server chalta rahega
    except KeyboardInterrupt:
        print("\nServer band ho gaya. Bye!")