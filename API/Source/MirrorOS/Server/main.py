# Websocketを利用して指定された会社・路線の運行情報を返す#

import asyncio
import websockets
import time
import JREastInformation as jre
import json

async def handler(websocket):
    try:    
        print("接続されました。")
        while True:
            data = await websocket.recv()
            print ("受信：" + data)

            status = jre.getJREastInformation()
            result = ""

            for i in range(0, len(status), 2):
                if status[i] == data:
                    result = status[i] + "は、" + status[i + 1] + "です。"
                    await websocket.send(result)
                    return
            await websocket.send("NOTFOUND")
            print("見つかりませんでした。")
    except KeyboardInterrupt:
        print("サーバーを終了します・・・")
        print("終了しました。")

server = websockets.serve(handler, "133.14.196.157", 100)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(server)
    print("サーバーを開始します・・・")
    loop.run_forever()
except KeyboardInterrupt:
    print("サーバーを終了します・・・")
finally:
    loop.close()
    print("終了しました。")