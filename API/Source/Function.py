# 関数一覧
import ntplib
import requests
import sys
from datetime import datetime
from time import ctime
sys.path.append('.')
import Exception.TimeServerNotFoundException as TimeServerNotFoundException

# ＊＊＊非推奨＊＊＊
# NTPサーバから時刻を取得します
# 内部的に使用している関数です
# エラー時には、TimeServerNotFoundExceptionを返します
# 引数は、NTPサーバのアドレスです
# 戻り値は、文字列で返します
def get_ntp_time(server):
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request(server)
        return ctime(response.tx_time)
    except ntplib.NTPException as e:
        raise TimeServerNotFoundException
    
# NTPサーバから現在時刻を取得します
# エラー時には、TimeServerNotFoundExceptionを返します
# 引数は、NTPサーバのアドレスです
# 戻り値は、datetime型で返します
def get_ntp_time_datetime(server):
    nowtime = get_ntp_time(server)
    return datetime.strptime(nowtime, "%a %b %d %H:%M:%S %Y")
    
# 天気を取得する
def get_weather(api_key, city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    return data