import requests
import datetime
import json
import mytoken

# 現在はトークンで認証しているが、いずれOAuth認証にする
__ACCESS_TOKEN = mytoken.timetree_token

def get_calendars():
    headers = {
        'Accept': 'application/vnd.timetree.v1+json',
        'Authorization': 'Bearer ' + __ACCESS_TOKEN
    }

    url = 'https://timetreeapis.com/calendars'
    response = requests.get(url, headers=headers)
    row_data = response.json()
    # print(json.dumps(data, indent=4, ensure_ascii=False))
    ret = []
    for i in range(len(row_data['data'])):
        ret.append({
            'id': row_data['data'][i]['id'],
            'name': row_data['data'][i]['attributes']['name'],
            'color': row_data['data'][i]['attributes']['color'],
            'image': row_data['data'][i]['attributes']['image_url']
        })

    print(json.dumps(ret, indent=4, ensure_ascii=False))
    return ret

def get_tasks():
    headers = {
        'Accept': 'application/vnd.timetree.v1+json',
        'Authorization': 'Bearer ' + __ACCESS_TOKEN
    }

    calendars = get_calendars()
    ret = []
    for calendar in calendars:
        url = 'https://timetreeapis.com/calendars/' + calendar['id'] + '/upcoming_events?timezone=Asia/Tokyo&days=7'
        response = requests.get(url, headers=headers)
        data = response.json()
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        
        hoge = []
        for i in range(len(data['data'])):
            hoge.append({
                'title': data['data'][i]['attributes']['title'],
                'start_at': data['data'][i]['attributes']['start_at'][:16],
                'end_at': data['data'][i]['attributes']['end_at'][:16]
            })
        
        ret.append({
            'name': calendar['name'],
            'id': calendar['id'],
            'color': calendar['color'],
            'image': calendar['image'],
            'data': hoge
        })

    # print(json.dumps(ret, indent=4, ensure_ascii=False))
    return ret

if __name__ == '__main__':
    output = get_tasks()
    with open (file='./application/task.json', mode='w', encoding='utf_8') as f:
        json.dump(obj=output, fp=f, indent=4, ensure_ascii=False)