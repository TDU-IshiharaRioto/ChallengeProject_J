import azure.cognitiveservices.speech as speechsdk
import time

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with cyour own subscription key and service region (e.g., "westus").
speech_key, service_region, language = "dc840a90894642feba11385afc990655", "japaneast", "ja-JP"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region, speech_recognition_language=language)

audio_config = speechsdk.AudioConfig(use_default_microphone = True)
# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("Say something...")

def recognized(evt):
    print('「{}」'.format(evt.result.text))
    # do something

def start(evt):
    print('SESSION STARTED: {}'.format(evt))

def stop(evt):
    print('SESSION STOPPED {}'.format(evt))

speech_recognizer.recognized.connect(recognized)
speech_recognizer.session_started.connect(start)
speech_recognizer.session_stopped.connect(stop)

try:
    speech_recognizer.start_continuous_recognition()
    time.sleep(60)
except KeyboardInterrupt:
    print("bye.")
    speech_recognizer.recognized.disconnect_all()
    speech_recognizer.session_started.disconnect_all()
    speech_recognizer.session_stopped.disconnect_all()
