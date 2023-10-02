# Websocketを利用して指定された会社・路線の運行情報を返す#

import asyncio
import websockets
import JREastInformation as jre

async def handler(websocket):
    try:    
        print("接続されました。")
        while True:
            print("待機中です・・・")
            data = await websocket.recv()
            print ("受信：" + data)

            statusKantou = jre.getJREastInformation()
            statusTohoku = jre.getJREastTohokuInformation()
            status = statusKantou + statusTohoku
            print ("長さ：" + str(len(status)))
            print ("路線数：" + str(len(status) / 2))
            result = ""

            count = 0
            sended = ["" for i in range(int(len(status) / 2))]
            sendedCount = 0
            if data == "ALL":
                for i in range(0, len(status), 2):
                    count  = count + 1
                    result = status[i + 1]
                    name = status[i]

                    for l in range(sendedCount):
                        if sended[l] == status[i] + status[i + 1]:
                            print("同一内容のためスキップ" + str(count) + "件目：" + name + "：" + result)
                            continue
                        else:
                            await websocket.send(str(count))
                            await websocket.send(name)
                            await websocket.send(result)
                            sended[sendedCount] = status[i] + status[i + 1]
                            sendedCount = sendedCount + 1
                            print("送信：" + str(count) + "件目：" + name + "：" + result)
            
            for i in range(0, len(status), 2):
                print ("検索中・・・（" +  str(i) + "件目）" + status[i])
                if status[i] == data:
                    count  = count + 1
                    result = status[i + 1]
                    name = status[i]

                    l = 0
                    while True:                          
                        if sended[l] == status[i] + status[i + 1]:
                            print("同一内容のためスキップ" + str(count) + "件目：" + name + "：" + result)
                            continue
                        else:
                            await websocket.send(str(count))
                            await websocket.send(name)
                            await websocket.send(result)
                            sended[sendedCount] = status[i] + status[i + 1]
                            sendedCount = sendedCount + 1
                            print("送信：" + str(count) + "件目：" + name + "：" + result)                 
                        l = l + 1
                if i == len(status) - 2 and count == 0:
                    await websocket.send("NOTFOUND")
                    print("見つかりませんでした。")
            
    except KeyboardInterrupt:
        print("サーバーを終了します・・・")
        print("終了しました。")

server = websockets.serve(handler, "100.2.6.11", 4)
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