def get_weather_today():
    import requests
    import html

    url = "https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json"
    response = requests.get(url)
    data = response.json()
    
    publishing_office = data["publishingOffice"]
    report_datetime = data["reportDatetime"]
    target_area = data["targetArea"]
    headline_text = data["headlineText"]
    text = data["text"]
    
    print("データ配信元:", publishing_office)
    print("報告日時:", report_datetime)
    print("対象の地域:", target_area)
    print("ヘッドライン:", headline_text)
    print("詳細な概要情報:", html.unescape(text))

def get_weather_forecast():
    import requests
    import html

    url = "https://www.jma.go.jp/bosai/forecast/data/forecas/130000.json"
    response = requests.get(url)
    data = response.json()
    
    publishing_office = data["publishingOffice"]
    report_datetime = data["reportDatetime"]
    target_area = data["areas"]
    weathers = data["weathers"]
    
    print("発表者:", publishing_office)
    print("報告日時:", report_datetime)
    print("対象の地域:", target_area)
    print("今日の天気:", weathers)
    # print("明日の天気:", html.unescape(text))
    # print("明後日の天気:", html.unescape(text)

# get_weather_today()
get_weather_forecast()