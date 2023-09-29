# Websocketを利用して指定された会社・路線の運行情報を返す#

import asyncio
import websockets
import JREastInformation as jre

async def handler(websocket):
    try:    
        print("接続されました。")
        while True:
            data = await websocket.recv()
            print ("受信：" + data)

            statusKantou = jre.getJREastInformation()
            statusTohoku = jre.getJREastTohokuInformation()
            status = statusKantou + statusTohoku
            print ("東北部分の長さ：" + str(len(status)))
            result = ""

            count = 0
            for i in range(0, len(status), 2):
                print ("検索中・・・（" +  str(i) + "件目）" + status[i])
                if status[i] == data:
                    count  = count + 1
                    result = status[i + 1]
                    name = status[i]
                    await websocket.send(str(count))
                    await websocket.send(name)
                    await websocket.send(result)
                    print("送信：" + str(count) + "件目：" + result)
                    
                if i == len(status) - 2 and count == 0:
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