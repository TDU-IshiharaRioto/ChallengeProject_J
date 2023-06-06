##################################################
# Train.py
# 交通状況に関する関数を定義するクラスです
# (C) 2023 IshiharaRioto
##################################################
import json
import requests
from .Exception import TrainServerNotFoundException as TrainServerNotFoundException

API_URL = "https://api.odpt.org/api/v4/"

# 鉄道路線情報を取得します
# 引数は、APIキーです
# 戻り値は、Json形式で返します
# 例外として、requests.exceptions.RequestExceptionとjson.decoder.JSONDecodeErrorをraiseする可能性があります
def getRailway (APIKey):
    base_url = f"{API_URL}odpt:Railway?acl:consumerKey={APIKey}"
    try:
        response = requests.get(base_url)
    except requests.exceptions.RequestException as e:
        raise TrainServerNotFoundException.TrainServerNotFoundException()
    
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        raise e
    
    return data

# 駅情報を取得します
# 引数は、APIキーです
# 戻り値は、Json形式で返します
# 例外として、requests.exceptions.RequestExceptionとjson.decoder.JSONDecodeErrorをraiseする可能性があります
def getStation (APIKey):
    base_url = f"{API_URL}odpt:Station?acl:consumerKey={APIKey}"
    try:
        response = requests.get(base_url)
    except requests.exceptions.RequestException as e:
        raise TrainServerNotFoundException.TrainServerNotFoundException()
    
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        raise e
    
    return data

# 指定された鉄道路線名称から、その路線に該当する駅名の配列を返します。
# 引数は、APIキーと鉄道路線名称です
# 戻り値は、駅名の配列です
# 例外として、requests.exceptions.RequestExceptionとjson.decoder.JSONDecodeErrorをraiseする可能性があります
#def getStationNameList (APIKey, railwayName):