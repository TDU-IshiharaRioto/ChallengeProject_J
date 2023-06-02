# 関数一覧

import json
import ntplib
import requests
from time import ctime

# NTPサーバから時刻を取得するコード
# 引数は、NTPサーバのアドレス
def get_ntp_time(server):
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request(server)
        return ctime(response.tx_time)
    except:
        return "Could not connect to NTP server"
    
# 天気を取得する
def get_weather(api_key, city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    return data