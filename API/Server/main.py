# Websocketを利用して指定された会社・路線の運行情報を返す

import asyncio
import websockets
import JREastInformation as jre
import TokyoMetro
import TobuRailway
import json

async def handler(websocket):
    try:    
        print("接続されました。")
        while True:
            print("待機中です・・・")
            data = await websocket.recv()
            print ("受信：" + data)

            # データ取得部分
            statusJREast = jre.getJREastInformation()
            statusTokyoMetro = TokyoMetro.getTokyoMetroInformation()
            statusTobu = TobuRailway.getTobuRailwayInformation()
            # 結合
            StatusData = statusJREast + statusTokyoMetro + statusTobu

            print ("長さ：" + str(len(StatusData)))
            print ("路線数：" + str(len(StatusData) / 2))
            resultData = []

            count = 0
            sended = ["" for i in range(int(len(StatusData) / 2))]
            sendedCount = 0

            # リクエストに,があれば分割
            data = data.split(",")

            for requestData in data:
                if requestData == "ALL":
                    print("メッセージ：全ての路線を送信します。")
                    for i in range(0, len(StatusData), 2):
                        count  = count + 1
                        result = StatusData[i + 1]
                        name = StatusData[i]
                        isSended = False

                        for l in range(sendedCount):
                            if sended[l] == StatusData[i] + StatusData[i + 1]:
                                #print("同一内容のためスキップ" + str(count) + "個目：" + name + "：" + result)
                                isSended = True
                                break

                        if isSended == False:
                            
                            sended[sendedCount] = StatusData[i] + StatusData[i + 1]
                            sendedCount = sendedCount + 1
                            # ここでデータを追加
                            resultData.append({"name": name, "status": result})
                            # print("送信：" + str(sendedCount + 1) + "件目：" + name + "：" + result)
                    # 追加
                    jsonData = json.dumps(resultData, ensure_ascii=False, indent=4)
                    print(jsonData)
                elif requestData == "LIST":
                    print ("メッセージ：路線一覧を送信します。")
                    for i in range(0, len(StatusData), 2):
                        isSended = False

                        for l in range(sendedCount):
                            if sended[l] == StatusData[i]:
                                #print("同一内容のためスキップ：" + str(i + 1) + "個目：" + StatusData[i])
                                isSended = True
                                break
                        
                        if isSended == False:
                            sended[sendedCount] = StatusData[i]
                            sendedCount = sendedCount + 1
                            # ここでデータを追加
                            resultData.append({"name": StatusData[i]})
                            #print("送信：" + str(sendedCount) + 1 + "件目：" + StatusData[i])
                    jsonData = json.dumps(resultData, ensure_ascii=False, indent=4)
                else:
                    print("メッセージ：指定された路線を送信します。" + requestData)
                    for i in range(0, len(StatusData), 2):
                        #print ("検索中・・・（" +  str(i) + "件目）" + StatusData[i])
                        if StatusData[i] == requestData:
                            count  = count + 1
                            result = StatusData[i + 1]
                            name = StatusData[i]
                            isSended = False

                            for l in range(sendedCount):
                                if sended[l] == StatusData[i] + StatusData[i + 1]:
                                    #print("同一内容のためスキップ" + str(count) + "個目：" + name + "：" + result)
                                    isSended = True
                                    break

                            if isSended == False:
                                sended[sendedCount] = StatusData[i] + StatusData[i + 1]
                                sendedCount = sendedCount + 1
                                # ここでデータを追加
                                resultData.append({"name": name, "status": result})
                                # print("送信：" + str(sendedCount) + "件目：" + name + "：" + result)
                        if i == len(StatusData) - 2 and count == 0:
                            print("見つかりませんでした。")
                    jsonData = json.dumps(resultData, ensure_ascii=False, indent=4)
                await websocket.send(jsonData)
            
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