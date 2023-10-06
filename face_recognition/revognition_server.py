import face_recognition
import cv2
import numpy as np
from websocket_server import WebsocketServer
import threading
import signal
import sys

# SIGINTハンドラ関数
def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    server.shutdown()
    video_capture.release()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# WebSocketサーバーのコールバック関数
def new_client(client, server):
    global last_recognized_names  # グローバル変数として参照する
    print("New client connected")
    last_recognized_names = []  # リセット
    print("New client connected")
    server.send_message_to_all("Unknown")

def client_left(client, server):
    print("Client disconnected")

def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client said: %s" % (client['id'], message))

# WebSocketサーバーの初期設定
PORT=5001
server = WebsocketServer(host="127.0.0.1", port=PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

# 別のスレッドでWebSocketサーバーを起動
thread = threading.Thread(target=server.run_forever)
thread.start()

# 顔認識の部分
video_capture = cv2.VideoCapture(0)
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
makoto_image = face_recognition.load_image_file("makoto.jpg")
makoto_face_encoding = face_recognition.face_encodings(makoto_image)[0]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    makoto_face_encoding,
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Makoto"
]

last_recognized_names = []

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    current_recognized_names = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.4)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            current_recognized_names.append(name)
        
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    for name in current_recognized_names:
        if name not in last_recognized_names:
            print(f"Recognized: {name}")
            server.send_message_to_all(name)
            last_recognized_names = current_recognized_names.copy()

    
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
