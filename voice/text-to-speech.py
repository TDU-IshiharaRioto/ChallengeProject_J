"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\natural-bison-368509-34aa3ef219dc.json'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame.mixer
from google.cloud import texttospeech
import time
import io

def play_audio_from_bytes(audio_data):
    # pygameの初期化
    pygame.mixer.init()
    
    # バイナリデータから音声をロード
    audio_file = io.BytesIO(audio_data)
    pygame.mixer.music.load(audio_file)
    
    # 音声の再生
    pygame.mixer.music.play()
    
    # 音声の長さだけ待つ (再生が終わるまで)
    while pygame.mixer.music.get_busy():
        time.sleep(1)



# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="こんにちは!")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

play_audio_from_bytes(response.audio_content)