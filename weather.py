# エリアコードの取得
def get_area_code():
    # https://anko.education/webapi/jma
    # この地域コード対応表を見ながら作成

    return 130000 # 東京

# 天気予報を取得
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

# データの正規化
def normalize_data(data):
    import datetime
    ret = []
    
    time = data[0]['reportDatetime']
    # print(time)
    date = time[0:10]
    weather = data[0]['timeSeries'][0]['areas'][0]['weathers'][0]
    max_temp = data[1]['tempAverage']['areas'][0]['min']
    min_temp = data[1]['tempAverage']['areas'][0]['max']

    # print(date + ' ' + weather + ' ' + str(max_temp) + ' ' + str(min_temp))

    ret.append({
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date': date,
        'weather': weather,
        'maxtemp': max_temp,
        'mintemp': min_temp
    })
    return ret

if __name__ == '__main__':
    # この形式でデータをjsonファイルに出力する
    import json
    code = get_area_code()
    data = get_weather_forecast()
    # print(data)
    output = normalize_data(data)

    with open(file='weather.json', mode='w', encoding='utf_8') as f:
        json.dump(obj=output, fp=f, indent=4, ensure_ascii=False)
    