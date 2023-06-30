import asyncio
import websockets
import json

# 天気予報を取得
def get_weather_forecast(area = 140000):
    import requests
    # あとで引数で地域を指定できるようにする
    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/' + str(area) + '.json'
    response = requests.get(url)
    
    if(response.status_code != 200):
        print('error')
        return
    
    data = response.json()
    # print(data)

    return data

# データの正規化
def normalize_data(data):
    # { "date": "2023-6-13", "weather": "晴れ", "max-temp": 25,"min-temp": 18 }
    # の形に書き換える

    ret = []
    
    time = data[0]['reportDatetime']
    # print(time)
    date = time[0:10]
    weather = data[0]['timeSeries'][0]['areas'][0]['weathers'][0]
    max_temp = data[1]['tempAverage']['areas'][0]['min']
    min_temp = data[1]['tempAverage']['areas'][0]['max']

    # print(date + ' ' + weather + ' ' + str(max_temp) + ' ' + str(min_temp))

    ret.append({
        'date': date,
        'weather': weather,
        'max-temp': max_temp,
        'min-temp': min_temp
    })
    return ret
 
async def Socket(websocket):
    await websocket.recv() # 県の名前を受け取る
    data = get_weather_forecast()
    print(data)
    output = normalize_data(data)
    await websocket.send(str(output))
    
async def main():
    async with websockets.serve(Socket, "localhost", 9998):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())