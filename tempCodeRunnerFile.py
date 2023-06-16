# エリアコードの取得
def get_area_code():
    # https://anko.education/webapi/jma
    # この地域コード対応表を見ながら作成

    return 130000 # 東京

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
    # { "date": "2023-6-13","hour":"14", "weather": "晴れ", "max-temp": 25,"min-temp": 18 }
    # の形に書き換える

    ret = []
    
    date = data['reportDatetime']
    print(date)
    # weather = data['timeSeries'][0]['areas'][0]['weathers'][i]
    # max_temp = data['timeSeries'][0]['areas'][0]['temps'][i]
    # min_temp = data['timeSeries'][0]['areas'][0]['tempsMin'][i]

    ret.append({
        'date': date[0:10],
        'hour': date[11:13],
        'weather': weather,
        'max-temp': max_temp,
        'min-temp': min_temp
    })

    print(ret)
    return ret

if __name__ == '__main__':
    # この形式でデータをjsonファイルに出力する
    import json
    code = get_area_code()
    data = get_weather_forecast()
    output = normalize_data(data)

    with open(file='weather.json', mode='w', encoding='utf_8') as f:
        json.dump(obj=data, fp=f, indent=4, ensure_ascii=False)
    