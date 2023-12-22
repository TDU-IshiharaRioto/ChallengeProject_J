import asyncio
import websockets

# エリアコードの取得
def get_area_code(pref):
    import requests
    url = 'https://www.jma.go.jp/bosai/common/const/area.json'
    response = requests.get(url)

    if(response.status_code != 200):
        print('error')
        return
    
    row_data = response.json()

    # データの整形
    # centersが地方、officesが都道府県、class10,15,20がより詳細な場所を指す
    # 欲しいエリアコードはofficesの値
    data = {}
    for key2, value2 in row_data['offices'].items():
        if 'officeName' in value2:
            if '気象台' or '気象庁' in value2['officeName']:
                data[value2['name']] = key2
    
    # ソケットで取得した名前からエリアコードを取得
    return data.get(pref)

# 週刊天気予報をのjsonファイルを取得
def get_weather_forecast(area):
    import requests
    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/' + str(area) + '.json'
    response = requests.get(url)
    
    if(response.status_code != 200):
        print('error')
        return
    
    data = response.json()

    return data

code2weather = {} # 天気コードと天気の対応表

# データの正規化(本日の天気のみ)
def normalize_data_today(data):
    import datetime
    ret = []
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 現在時刻
    time = data[0]['reportDatetime'] # 予報時刻

    area = data[0]['publishingOffice']
    date = time[0:10]
    w_code = data[0]['timeSeries'][0]['areas'][0]['weatherCodes'][0]
    weather = code2weather[int(w_code)]
    max_temp = data[1]['tempAverage']['areas'][0]['max']
    min_temp = data[1]['tempAverage']['areas'][0]['min']

    ret.append({
        'area' : area,
        'now': now,
        'date': date,
        'weather': weather,
        'maxtemp': max_temp,
        'mintemp': min_temp
    })
    return ret

# データの正規化(週間の天気)
def normalize_data_week(data):
    import datetime
    ret = []
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #現在時刻
    time = data[1]['reportDatetime'] #予報時刻

    date_row = data[1]['timeSeries'][0]['timeDefines']
    dates = []
    for i in date_row:
        dates.append(i[0:10])

    weather_row = data[1]['timeSeries'][0]['areas'][0]['weatherCodes']
    weathers = []
    for i in weather_row:
        weather_code = i
        weathers.append(code2weather[int(weather_code)])

    max_temp_row = data[1]['timeSeries'][1]['areas'][0]['tempsMax']
    max_temps = []
    for i in max_temp_row:
        max_temps.append(i)

    min_temp_row = data[1]['timeSeries'][1]['areas'][0]['tempsMin']
    min_temps = []
    for i in min_temp_row:
        min_temps.append(i)

    for i in range(len(dates)):
        ret.append({
            'now': now,
            'date': dates[i],
            'weather': weathers[i],
            'maxtemp': max_temps[i],
            'mintemp': min_temps[i]
        })

    return ret


async def Socket(websocket):
    pref = await websocket.recv() # 県の名前を受け取る
    area_code = get_area_code(pref) 
    data = get_weather_forecast(area_code)
    print(data)
    output = normalize_data_today(data)
    # output = normalize_data_week(data)
    await websocket.send(str(output).replace('\'','\"'))

async def main():
    async with websockets.serve(Socket, "localhost", 9998):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    import json
    # 天気コードと天気の対応表を作成
    with open(file='./weatherCode.json', mode='r', encoding='utf_8') as f:
        hoge = json.loads(f.read())
        for i in hoge:
            code2weather[int(i)] = hoge[i][3]

    # サーバーを起動
    asyncio.run(main())

    '''
    jsonファイルを作成するためのコード
    code = get_area_code()
    data = get_weather_forecast(code)

    output = normalize_data_today(data)
    output = normalize_data_week(data)
    
    with open(file='./application/weather.json', mode='w', encoding='utf_8') as f:
        json.dump(obj=output, fp=f, indent=4, ensure_ascii=False)
    '''