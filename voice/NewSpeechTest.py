#coding utf-8
import speech_recognition as sr
from datetime import datetime
import wave
import pyaudio

# チャンク数を指定
CHUNK = 1024
filename = "C:\\Users\\nihuhuhu\\Documents\\voice\\konnichiwa_02.wav"

# 音声ファイルを開く
wf = wave.open(filename, 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# インデックスをファイルの先頭に戻す
def reset_audio():
    wf.rewind()

# 最初に1回リセットしておく
reset_audio()

r = sr.Recognizer()
mic = sr.Microphone()

while True:
    print("しゃべってください")

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    print ("録音しています")

    try:
        recognized_text = r.recognize_google(audio, language='ja-JP')
        print(recognized_text)

        if recognized_text == "こんにちは":
            reset_audio()  # 音声ファイルをリセット
            while len(data := wf.readframes(CHUNK)):
                stream.write(data)
            continue
    

    except sr.UnknownValueError:
        print("録音できませんでした")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
