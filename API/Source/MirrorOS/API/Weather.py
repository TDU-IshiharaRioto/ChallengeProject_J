##################################################
# Weather.py
# 天気の取得に関する関数を定義するクラスです
# (C) 2023 IshiharaRioto
##################################################

import json
import requests
import sys
sys.path.append('.')
import Exception.WeatherServerNotFoundException as WeatherServerNotFoundException

# 天気を取得します
# 引数は、APIキーと都市名です
# 戻り値は、Json形式で返します
# 例外として、requests.exceptions.RequestExceptionとjson.decoder.JSONDecodeErrorをraiseする可能性があります
def get_weather(api_key, city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(base_url)
    except requests.exceptions.RequestException as e:
        raise e
    
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        raise e
    
    return data