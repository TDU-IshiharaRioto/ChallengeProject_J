import mytoken

# 現在はトークンで認証しているが、いずれOAuth認証にする
__ACCESS_TOKEN = mytoken.timetree_token
__headers = {
    'Accept': 'application/vnd.timetree.v1+json',
    'Authorization': 'Bearer ' + __ACCESS_TOKEN
}

def get_calendars():
    import requests
    import json
    url = 'https://timetreeapis.com/calendars'
    response = requests.get(url, headers=__headers)
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

    # print(json.dumps(ret, indent=4, ensure_ascii=False))
    return ret

def get_tasks():
    import requests
    import json
    import datetime
    from dateutil.tz import gettz
    calendars = get_calendars()
    ret = []
    for calendar in calendars:
        url = 'https://timetreeapis.com/calendars/' + calendar['id'] + '/upcoming_events?timezone=Asia/Tokyo&days=7'
        response = requests.get(url, headers=__headers)
        data = response.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        
        hoge = []
        for i in range(len(data['data'])):
            # TODO: start_atの時間がZ時間なので、日本時間に変換する
            hoge.append({
                'title': data['data'][i]['attributes']['title'],
                # 'start_at': datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ'),
                # 'end_at': datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')
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
    import json
    output = get_tasks()
    with open (file='./application/task.json', mode='w', encoding='utf_8') as f:
        json.dump(obj=output, fp=f, indent=4, ensure_ascii=False)