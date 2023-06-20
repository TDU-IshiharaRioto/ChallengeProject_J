# エリアコードの取得
def get_area_code():
    # https://anko.education/webapi/jma
    # この地域コード対応表を見ながら作成

    return 130000 # 東京

# 週刊天気予報をのjsonファイルを取得
def get_weather_forecast(area = 130000):
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

code2weather = {} # 天気コードと天気の対応表

# データの正規化(本日の天気のみ)
def normalize_data_today(data):
    import datetime
    ret = []
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 現在時刻
    time = data[0]['reportDatetime'] # 予報時刻
    # print(time)

    date = time[0:10]
    w_code = data[0]['timeSeries'][0]['areas'][0]['weatherCodes'][0]
    weather = code2weather[int(w_code)]
    max_temp = data[1]['tempAverage']['areas'][0]['max']
    min_temp = data[1]['tempAverage']['areas'][0]['min']
    # print(date + ' ' + weather + ' ' + str(max_temp) + ' ' + str(min_temp))

    ret.append({
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
    # print(dates)

    weather_row = data[1]['timeSeries'][0]['areas'][0]['weatherCodes']
    weathers = []
    for i in weather_row:
        weather_code = i
        weathers.append(code2weather[int(weather_code)])
    # print(weathers)

    max_temp_row = data[1]['timeSeries'][1]['areas'][0]['tempsMax']
    max_temps = []
    for i in max_temp_row:
        max_temps.append(i)
    # print(max_temps)

    min_temp_row = data[1]['timeSeries'][1]['areas'][0]['tempsMin']
    min_temps = []
    for i in min_temp_row:
        min_temps.append(i)
    # print(min_temps)

    for i in range(len(dates)):
        ret.append({
            'now': now,
            'date': dates[i],
            'weather': weathers[i],
            'maxtemp': max_temps[i],
            'mintemp': min_temps[i]
        })
    # print(ret)

    return ret

if __name__ == '__main__':
    import json

    # 天気コードと天気の対応表を作成
    with open(file='./application/weatherCode.json', mode='r', encoding='utf_8') as f:
        hoge = json.loads(f.read())
        for i in hoge:
            code2weather[int(i)] = hoge[i][3]
    # print(code2weather)

    code = get_area_code()
    data = get_weather_forecast()
    # print(data)
    output = normalize_data_today(data)
    
    with open(file='./application/weather.json', mode='w', encoding='utf_8') as f:
        json.dump(obj=output, fp=f, indent=4, ensure_ascii=False)
    