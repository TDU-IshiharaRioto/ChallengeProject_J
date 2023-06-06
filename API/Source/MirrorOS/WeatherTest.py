##################################################
# 天気のJsonについて、テストするプログラム
# auther 石原遼大
##################################################

import Weather

api_key = "36e11e8ab78188c4e895599eaed67897"
city = "Tokyo"

WeatherData = Weather.get_weather(api_key, city)
keys = WeatherData.keys()

for key in keys:
    print(key)
    print(WeatherData[key])
    print("\n")