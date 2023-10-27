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

def client_left(client, server):
    print("Client disconnected")

def message_received(client, server, message):
    global last_recognized_names  # グローバル変数として参照する
    server.send_message_to_all(",".join(last_recognized_names))
        

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
    "Nakatsu",
]

last_recognized_names = []

recognition_repeat = 3
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    
    all_recognized_names_for_current_frame = []

    for (top, right, bottom, left) in face_locations:
        names_counter = {}

        # Recognition repeated for increased accuracy
        for _ in range(recognition_repeat):
            face_encodings = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])
            if face_encodings:
                face_encoding = face_encodings[0]
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                name = known_face_names[best_match_index] if matches[best_match_index] else "Unknown"
                names_counter[name] = names_counter.get(name, 0) + 1

        # Choosing the name that was recognized the most times
        most_recognized_name = max(names_counter, key=names_counter.get)
        all_recognized_names_for_current_frame.append(most_recognized_name)

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, most_recognized_name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Check for changes in recognized names and print only if there's a change
    if set(last_recognized_names) != set(all_recognized_names_for_current_frame):
        print(all_recognized_names_for_current_frame)
        server.send_message_to_all(",".join(all_recognized_names_for_current_frame))

    last_recognized_names = all_recognized_names_for_current_frame.copy()

    cv2.imshow('Video', frame)
    cv2.waitKey(1)


video_capture.release()
cv2.destroyAllWindows()
