#coding utf-8

import speech_recognition as sr
from datetime import datetime
"""
#文字起こしファイルのファイル名を日付のtxtファイルとする
filename = datetime.now().strftime('%Y%m%d_%H-%M-%S')
txt =filename +".txt"

with open(txt, 'w') as f: #txtファイルの新規作成 
    f.write(filename + "\n") #最初の一行目にはfilenameを記載する
"""
r = sr.Recognizer()
mic = sr.Microphone()

while True:
    print("しゃべってください")

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    print ("録音しています")

    try:
        print(r.recognize_google(audio, language='ja-JP'))

        if r.recognize_google(audio, language='ja-JP') == "こんにちは" :#こんにちはを検出したらこんにちはを返す
            print("こんにちは画面をうつします")
            break
        """
        with open(txt,'a') as f: #ファイルの末尾に追記していく
            f.write("\n" + r.recognize_google(audio, language='ja-JP'))
        """
    #認識できなかった時に止まらないようにする
    except sr.UnknownValueError:
        print("録音できませんでした")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
