import cv2
import numpy as np
import os 

# 自分で作成した学習モデルを読み込む
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('.\\trainer.yml')

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0
# ユーザーIDを名前に置き換えるためのリストを作る
# 例 id=1(リストの要素1) ⇒ pi、id=2 ⇒ raspberry
names = ['None', 'nakatsu'] 

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# 顔として認識する最小サイズを定義する
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

# 前回のフレームで認識したIDを保持する変数
prev_id = None

while True:
    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        # 顔認識の信頼度を取得 100～0 0の時が100%一致
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        if (confidence < 60):
            # 顔認識しているidから名前に変換
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        # 新たな人物が認識された場合、名前をprintする
        if prev_id != id and id != "unknown":
            print(f"新たに {id} を認識しました!")
            
        # 名前を表示
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        # 信頼度(%)を表示
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

print("プログラムを終了します。")
cam.release()
cv2.destroyAllWindows()