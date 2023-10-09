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

            statusJREast = jre.getJREastInformation()
            print ("長さ：" + str(len(statusJREast)))
            print ("路線数：" + str(len(statusJREast) / 2))
            result = ""

            count = 0
            sended = ["" for i in range(int(len(statusJREast) / 2))]
            sendedCount = 0
            if data == "ALL":
                print("メッセージ：全ての路線を送信します。")
                for i in range(0, len(statusJREast), 2):
                    count  = count + 1
                    result = statusJREast[i + 1]
                    name = statusJREast[i]
                    isSended = False

                    for l in range(sendedCount):
                        if sended[l] == statusJREast[i] + statusJREast[i + 1]:
                            print("同一内容のためスキップ" + str(count) + "件目：" + name + "：" + result)
                            isSended = True
                            break

                    if isSended == False:
                        await websocket.send(str(count))
                        await websocket.send(name)
                        await websocket.send(result)
                        sended[sendedCount] = statusJREast[i] + statusJREast[i + 1]
                        sendedCount = sendedCount + 1
                        print("送信：" + str(count) + "件目：" + name + "：" + result)
            elif data == "LIST":
                print ("メッセージ：路線一覧を送信します。")
                for i in range(0, len(statusJREast), 2):
                    sended = []
                    sendedCount = 0
                    isSended = False

                    for l in range(sendedCount):
                        if sended[l] == statusJREast[i]:
                            print("同一内容のためスキップ" + str(i + 1) + "件目：" + statusJREast[i])
                            isSended = True
                            break
                    
                    if isSended == False:
                        sended[sendedCount] = statusJREast[i]
                        sendedCount = sendedCount + 1
                        await websocket.send(str(i + 1))
                        await websocket.send(statusJREast[i])
                        print("送信：" + str(i + 1) + "件目：" + statusJREast[i])
            else:
                print("メッセージ：指定された路線を送信します。" + data)
                for i in range(0, len(statusJREast), 2):
                    print ("検索中・・・（" +  str(i) + "件目）" + statusJREast[i])
                    if statusJREast[i] == data:
                        count  = count + 1
                        result = statusJREast[i + 1]
                        name = statusJREast[i]
                        isSended = False

                        for l in range(sendedCount):
                            if sended[l] == statusJREast[i] + statusJREast[i + 1]:
                                print("同一内容のためスキップ" + str(count) + "件目：" + name + "：" + result)
                                isSended = True
                                break

                        if isSended == False:
                            await websocket.send(str(count))
                            await websocket.send(name)
                            await websocket.send(result)
                            sended[sendedCount] = statusJREast[i] + statusJREast[i + 1]
                            sendedCount = sendedCount + 1
                            print("送信：" + str(count) + "件目：" + name + "：" + result)
                    if i == len(statusJREast) - 2 and count == 0:
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