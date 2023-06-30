import requests
import json
import token

ACCESS_TOKEN = token.timetree_token
CALENDAR_ID = 'カレンダーのID'

# ヘッダーの設定
headers = {
    'Accept': 'application/vnd.timetree.v1+json',
    'Authorization': 'Bearer ' + ACCESS_TOKEN
}

URL = 'https://timetreeapis.com/calendars/' + CALENDAR_ID + '/upcoming_events?timezone=Asia/Tokyo'

r = requests.get(URL, headers=headers)
data = r.json()


# 予定の表示
for event in data['data']:
    print(event['attributes']['title'])