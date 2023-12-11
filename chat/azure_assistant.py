import azure.cognitiveservices.speech as speechsdk
import time
import openai
import os
from websocket_server import WebsocketServer
import threading
import signal
import sys
import json

functions = [
	{
		"name":"trainFunction",
		"description": "電車の運行情報を教えてください",
		"parameters":{
			"type": "object",
                "properties": {
					"lineName": {
                        "type": "string",
                        "description": "聞かれている路線"
					}
			},
			"requaired":["lineName"]
		}

	},
    {
		"name":"weatherFunction",
		"description": "天気を教えてください",
		"parameters":{
			"type": "object",
                "properties": {
			},
			"requaired":[]
		}
	},
    {
		"name":"timeTableFunction",
		"description": "時間割を教えてください",
		"parameters":{
			"type": "object",
                "properties": {
                    "dayNumber": {
                        "type": "string",
                        "description": "聞かれている曜日を表す整数 (0:指定なし, 1:月曜日, 2:火曜日, 3:水曜日, 4:木曜日, 5:金曜日, 6:土曜日)"
					}
			},
			"requaired":["dayNumber"]
		}
	},
    
    
	
]

# Global Variables
server = None
session_active = False
messages_history = []
last_input_time = time.time()
recognized_text = ""
clients = {}

# SIGINTハンドラ関数
def signal_handler(sig, frame):
    global server
    print("Shutting down gracefully...")
    server.shutdown()
    sys.exit(0)

# WebSocketサーバーのコールバック関数
def new_client(client, server):
    print("New client connected")

def client_left(client, server):
    print("Client disconnected")

def message_received(client, server, sned_message):
    print("Client said: " + sned_message)
    data = json.loads(sned_message)
    if data['type'] == 'CONNECT':
        clients[data['name']] = client

    if data['type'] == 'RESPONSE':
        

        if(client == clients['MMM-trainInfo']):
            messages_history.append({"role": "user", "content": "以下のデータを使って一つ前の質問に答えてください" + str(data['data'])})
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=messages_history,
            )
            s = str(response['choices'][0]['message']['content'])
            speak_and_dispaly(s)
        if(client == clients['weather']):
            messages_history.append({"role": "user", "content": "以下のフォーマットとデータを使って一つ前の質問に答えてください。#フォーマット[現在の天気は~,気温は~です] #データ" + str(data['data'])})
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=messages_history,
            )
            speak_and_dispaly(response['choices'][0]['message']['content'])
        if(client == clients['MMM-timeTable']):
            print(json.loads(data['data']))
            if(json.loads(data['data']) == []):
                speak_and_dispaly("時間割はありません。")
                return
            messages_history.append({"role": "user", "content": "以下のデータを読み上げてください。授業がない場合はスキップしてください。" + str(data['data'])})
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=messages_history,
            )
            speak_and_dispaly(response['choices'][0]['message']['content'])
        global session_active
        session_active = False

    
    

def setup_websocket_server():
    global server
    server = WebsocketServer(host="127.0.0.1", port=5005)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    thread = threading.Thread(target=server.run_forever)
    thread.start()

def recognized(evt):
    global recognized_text
    if evt.result.text == "":
        return
    print('「{}」'.format(evt.result.text))
    recognized_text = evt.result.text

def check_activation_phrase(text):
    activation_phrases = ["鏡よ", "鏡を","スマートミラー"]
    return any(phrase in text for phrase in activation_phrases)

def handle_activation():
    global session_active, messages_history
    session_active = True
    messages_history = [{"role": "system", "content": "あなたはスマートミラーの中に搭載されたAIアシスタントです。"},{"role": "user", "content": "鏡よ、鏡"}]
    speak_and_dispaly("はい、なんでしょう？")

def speak_and_dispaly(text):
    print(text)
    speech_recognizer.stop_continuous_recognition()

    #clientsにMMM-chatがあるか確認
    if('MMM-chat' in clients):
        server.send_message(clients['MMM-chat'],'{"type":"TEXT","text":"' + text.replace('\n','') + '"}')
    speech_synthesizer.speak_text(text)
    speech_recognizer.start_continuous_recognition()

def get_openai_response(text):
    global messages_history,session_active
    try:
        messages_history.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=messages_history,
            functions=functions,
            function_call="auto"
        )
        response_data = json.loads(str(response['choices'][0]['message']))
        print(response_data)
        if('function_call' in response_data):
            if(response_data['function_call']['name'] == 'trainFunction'):
                print('運行情報')
                arguments = json.loads(response_data['function_call']['arguments'])
                lineName = arguments['lineName']
                server.send_message(clients['MMM-trainInfo'],'{"type":"CALL","lineName":' + str(lineName) + '}')
            if(response_data['function_call']['name'] == 'weatherFunction'):
                server.send_message(clients['weather'],'{"type":"CALL"}')
            if(response_data['function_call']['name'] == 'timeTableFunction'):
                arguments = json.loads(response_data['function_call']['arguments'])
                dayNumber = arguments['dayNumber']
                if(dayNumber == '0'):
                    dayNumber = time.localtime().tm_wday + 1
                    server.send_message(clients['MMM-timeTable'],'{"type":"CALL","dayNumber":' + str(dayNumber) +'}')
                else:
                    server.send_message(clients['MMM-timeTable'],'{"type":"CALL","dayNumber":' + str(arguments['dayNumber']) +'}')
            
            return ""
        elif('content' in response_data):
            
            messages_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
            return response['choices'][0]['message']['content']
            
        else:
            return ""
    except Exception as e:
        print("exceptions")
        print(e)
        return "すみません、よくわかりませんでした。"

def main_loop():
    global recognized_text, last_input_time, session_active, messages_history

    while True:
        time.sleep(1)
        if recognized_text == "":
            continue
            
        if session_active:
        #if True:
            messages_history = []
            speech_recognizer.stop_continuous_recognition()
            response_text = get_openai_response(recognized_text)
            if response_text:
                session_active = False
                print(response_text)
                speak_and_dispaly(response_text)

        elif check_activation_phrase(recognized_text):
            handle_activation()
        recognized_text = ""

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    setup_websocket_server()

    # Azure and OpenAI setup
    openai.api_key = os.getenv("AZURE_OPENAI_KEY")
    openai.api_version = "2023-07-01-preview"
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")

    speech_key = os.getenv('AZURE_SPEECH_KEY')
    service_region, language = "japaneast", "ja-JP"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language=language)
    audio_input_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input_config)

    audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = 'ja-JP-NanamiNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)

    print("話しかけてください...")

    speech_recognizer.recognized.connect(recognized)
    speech_recognizer.start_continuous_recognition()

    main_loop()
