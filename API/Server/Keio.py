from bs4 import BeautifulSoup
import requests as req


def getKeioInfomation():
    url = 'https://www.keio.co.jp/unkou/unkou_pc.html'
    resultList = []
    route = "京王線"

    response = req.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, "html.parser")
    operation_items = bs.find("p", class_="status")

    resultList = []
    resultList.extend([route, operation_items.text.replace('\u3000', '\n')]) # 路線名と運行状況を配列に追加

    return resultList

if __name__ == '__main__':
    print(getToeiInfomation())