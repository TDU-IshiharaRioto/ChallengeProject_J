##################################################
# 天気のJsonについて、テストするプログラム
# auther 石原遼大
##################################################

import Function

api_key = "36e11e8ab78188c4e895599eaed67897"
city = "Tokyo"

WeatherData = Function.get_weather(api_key, city)
keys = WeatherData.keys()

for key in keys:
    print(key)
    print(WeatherData[key])
    print("\n")