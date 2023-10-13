import azure.cognitiveservices.speech as speechsdk
import time
import openai
import os


openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_version = "2023-07-01-preview"
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")

recognized_text = ""

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with cyour own subscription key and service region (e.g., "westus").
speech_key, service_region, language = "dc840a90894642feba11385afc990655", "japaneast", "ja-JP"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region, speech_recognition_language=language)

audio_input_config = speechsdk.AudioConfig(device_name="{0.0.1.00000000}.{f4230723-0f8c-4396-aa65-59ebe2d673ad}")
# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input_config)

#--------------------------------------------------
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='ja-JP-NanamiNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)

print("Say something...")

def recognized(evt):
    global recognized_text
    if evt.result.text == "":
        return
    if recognized_text != "":
        return
    print('「{}」'.format(evt.result.text))
    recognized_text = evt.result.text

def start(evt):
    print('SESSION STARTED: {}'.format(evt))

def stop(evt):
    print('SESSION STOPPED {}'.format(evt))

speech_recognizer.recognized.connect(recognized)
speech_recognizer.session_started.connect(start)
speech_recognizer.session_stopped.connect(stop)


speech_recognizer.start_continuous_recognition()


while True:
    time.sleep(0.5)
    if(recognized_text != ""):
        try:
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=[{"role": "user", "content": recognized_text}],
            )
        except Exception as e:
            print(e)
        recognized_text = ""
        print(response['choices'][0]['message']['content'])
        speech_synthesis_result = speech_synthesizer.speak_text(response['choices'][0]['message']['content'])
        recognized_text = ""
