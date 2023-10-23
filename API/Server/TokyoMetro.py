import requests
import json

def getTokyoMetroInformation():
    url = 'https://www.tokyometro.jp/library/common/operation/status.json'

    response = requests.get(url)
    data_str = response.text[len('operate_status_cb_func('):-1]
    jsonData = json.loads(data_str)
    lines = jsonData['jp']['lines']
    result = []
    for line in lines:
        result.append(line['line_name'])
        if line['status_info'] == '平常運転':
            result.append(line['status_info'])
        else:
            result.append(line['status_info'] + ' ' + line['contents'])
    return result

if __name__ == '__main__':
    print(getTokyoMetroInformation())