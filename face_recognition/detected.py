import cv2
import numpy as np
import time

def initialize_recognizer(trainer_path, cascade_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainer_path)
    face_cascade = cv2.CascadeClassifier(cascade_path)
    return recognizer, face_cascade

def detect_faces(gray, face_cascade, minW, minH):
    return face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

def main():
    recognizer, face_cascade = initialize_recognizer('.\\trainer.yml', 'haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['None', 'nakatsu',"obama"]

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    prev_id = None
    last_detected_time = None
    detected_printed, not_detected_printed = False, True

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray, face_cascade, minW, minH)

        if len(faces) > 0:
            if not detected_printed:
                print("検出")
                detected_printed, not_detected_printed = True, False
            last_detected_time = time.time()
        elif last_detected_time and time.time() - last_detected_time > 10 and not not_detected_printed:
            print("非検出")
            detected_printed, not_detected_printed = False, True
            prev_id = None

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            
            id_name = names[id] if confidence < 60 else "unknown"
            confidence_text = "  {0}%".format(round(100 - confidence))
            
            if prev_id == None and id_name != "unknown":
                print(f"{id_name} を認識")
                prev_id = id_name
                
            cv2.putText(img, str(id_name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, confidence_text, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)
        if cv2.waitKey(10) & 0xff == 27:
            break

    print("プログラムを終了します。")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
