#parte do instalavel#
import os
import sys
import socket
import threading
import time
import uvicorn
import webview

if not getattr(sys, 'frozen', False):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

HOST = "127.0.0.1"
PORTA = 8000


def iniciar_servidor():
    uvicorn.run(app, host=HOST, port=PORTA, log_config=None)


def esperar_servidor():
    for _ in range(50):
        try:
            with socket.create_connection((HOST, PORTA), timeout=0.2):
                return
        except OSError:
            time.sleep(0.1)


if __name__ == "__main__":
    threading.Thread(target=iniciar_servidor, daemon=True).start()
    esperar_servidor()

    webview.settings["ALLOW_DOWNLOADS"] = True
    webview.create_window("RDB Digital", f"http://{HOST}:{PORTA}/app", width=1280, height=800)
    webview.start()
