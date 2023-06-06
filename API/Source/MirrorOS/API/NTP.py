##################################################
# NTP.py
# 時刻の取得に関する関数を定義するクラスです
# (C) 2023 IshiharaRioto
##################################################
import ntplib
from datetime import datetime
from time import ctime
from .Exception import TimeServerNotFoundException

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
    
