import requests
import json

def getTokyuInformation():
    url = 'https://www.tokyu.co.jp/unten/unten2.json'

    response = requests.get(url)
    response.encoding = response.apparent_encoding
    data_str = response.text
    jsonData = json.loads(data_str)

    print (jsonData)

    lines = ['東横線', '目黒線', '東急新横浜線', '田園都市線', '大井町線', '池上線', '東急多摩川線', '世田谷線', 'こどもの国線']
    jsonIndex = ['ty', 'mg', 'sh', 'dt', 'om', 'ik', 'tm', 'sg', 'kd']
    result = []

    i = 0
    for line in lines:
        result.append(line)
        if jsonData['unten_' + jsonIndex[i]] == line + ('は、平常通り運転しています。'):
            result.append('平常運転')
        else:
            result.append(jsonData['unten_' + jsonIndex[i]] + '\n' + jsonData['furikae_' + jsonIndex[i]])
        i += 1
    return result

if __name__ == '__main__':
    print(getTokyuInformation())