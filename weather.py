def get_weather_forecast(area = 130000):
    import requests
    # あとで引数で地域を指定できるようにする
    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json'
    response = requests.get(url)
    
    if(response.status_code != 200):
        print('error')
        return
    
    data = response.json()
    # print(data)

    return data


if __name__ == '__main__':
    # { "date": "2023-6-13","hour":"14", "weather": "晴れ", "max-temp": 25,"min-temp": 18 }
    # この形式でデータをjsonファイルに出力する
    import json
    data = get_weather_forecast()
    with open(file='weather.json', mode='w', encoding='utf_8') as f:
        json.dump(obj=data, fp=f, indent=4, ensure_ascii=False)
    