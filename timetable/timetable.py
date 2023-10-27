import cv2
import numpy as np
import time
from websocket_server import WebsocketServer
import threading
import signal
import sys

# SIGINTハンドラ関数
def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    server.shutdown()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# WebSocketサーバーのコールバック関数
def new_client(client, server):
    print("New client connected")

def client_left(client, server):
    print("Client disconnected")

def message_received(client, server, message):
    str = '金曜二限挑戦型' # 形式はjsonなどテキストデータが送れる
    server.send_message_to_all(str)


def main():
    while True:
        None


# WebSocketサーバーの初期設定
server = WebsocketServer(host="127.0.0.1", port=5004)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

# 別のスレッドでWebSocketサーバーを起動
thread = threading.Thread(target=server.run_forever)
thread.start()

main()
