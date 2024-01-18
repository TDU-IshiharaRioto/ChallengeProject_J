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
		"description": "電車の運行情報を教えてください。路線名は以下から検索してください[山手線, 上野東京ライン, 湘南新宿ライン, 相鉄線直通列車, 東海道線, 京浜東北線, 横須賀線, 南武線, 横浜線]",
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
    {
		"name":"dateTimeFunction",
		"description": "日付もしくは時間を聞かれた際に答える",
		"parameters":{
			"type": "object",
                "properties": {
			},
			"requaired":[]
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
    payload = json.loads(sned_message)
    if payload['type'] == 'CONNECT':
        clients[payload['name']] = client

    if payload['type'] == 'RESPONSE':
        contents_data = str(payload['data'])
        
        if(client == clients['MMM-trainInfo']):
            messages_history.append({"role": "user", "content": "以下のデータを使って一つ前の質問に答えてください" + contents_data})
            
        if(client == clients['weather']):
            messages_history.append({"role": "user", "content": "以下のフォーマットとデータを使って一つ前の質問に答えてください。#フォーマット[現在の天気は~,気温は~です] #データ" + contents_data})

        if(client == clients['MMM-timeTable']):
            if(json.loads(contents_data) == []):
                speak_and_dispaly("時間割はありません。")
                return
            messages_history.append({"role": "user", "content": "以下のデータを読み上げてください。授業がない場合はスキップしてください。" + contents_data})

        if(client == clients['clock']):
            messages_history.append({"role": "user", "content": "以下のデータを使って一つ前の質問に日本語で答えてください" + contents_data})

        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=messages_history,
        )
        speak_and_dispaly(str(response['choices'][0]['message']['content']))
        global session_active
        session_active = False

def get_openai_response(text):
    global messages_history

    try:
        # ユーザーメッセージを履歴に追加
        messages_history.append({"role": "user", "content": text})

        # OpenAIのレスポンスを取得
        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=messages_history,
            functions=functions,
            function_call="auto"
        )
        response_data = response['choices'][0]['message']

        # 機能呼び出しの処理
        if 'function_call' in response_data:
            function_call = response_data['function_call']
            function_name = function_call['name']
            arguments = json.loads(function_call['arguments'])

            if function_name == 'trainFunction':
                lineName = arguments['lineName']
                server.send_message(clients['MMM-trainInfo'], f'{{"type":"CALL","lineName":"{lineName}"}}')
            elif function_name == 'weatherFunction':
                server.send_message(clients['weather'], '{"type":"CALL"}')
            elif function_name == 'timeTableFunction':
                dayNumber = arguments.get('dayNumber', time.localtime().tm_wday + 1)
                server.send_message(clients['MMM-timeTable'], f'{{"type":"CALL","dayNumber":{dayNumber}}}')
            elif function_name == 'dateTimeFunction':
                server.send_message(clients['clock'], '{"type":"CALL"}')
            return ""

        # 通常のレスポンスの処理
        else:
            messages_history.append({"role": "assistant", "content": response_data['content']})
            return response_data['content']


    except Exception as e:
        print("Exception:", e)
        return "すみません、よくわかりませんでした."

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
    messages_history = [{"role": "system", "content": "あなたは与えられた情報を使って質問に答えることができます。質問に答える際は質問に対する回答をなるべく簡潔に答えてください。"}]
    speak_and_dispaly("はい、なんでしょう？")

def speak_and_dispaly(text):
    print(text)
    speech_recognizer.stop_continuous_recognition()

    #clientsにMMM-chatがあるか確認
    if('MMM-chat' in clients):
        server.send_message(clients['MMM-chat'],'{"type":"TEXT","text":"' + text.replace('\n','') + '"}')
    speech_synthesizer.speak_text(text)
    speech_recognizer.start_continuous_recognition()


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
