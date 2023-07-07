import requests
import json
import mytoken

# 現在はトークンで認証しているが、いずれOAuth認証にする
ACCESS_TOKEN = mytoken.timetree_token
CALENDAR_ID = mytoken.timetree_calendar_id

def get_caleder():
    return

# ヘッダーの設定
if __name__ == '__main__':
    headers = {
    'Accept': 'application/vnd.timetree.v1+json',
    'Authorization': 'Bearer ' + ACCESS_TOKEN
    }

    url = 'https://timetreeapis.com/calendars/' + CALENDAR_ID + '/upcoming_events?timezone=Asia/Tokyo&days=7'
    response = requests.get(url, headers=headers)
    print(response)
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))

    for i in range(len(data['data'])):
        print(data['data'][i]['attributes']['title'])
        print(data['data'][i]['attributes']['start_at'][:16])
        print(data['data'][i]['attributes']['end_at'][:16])
