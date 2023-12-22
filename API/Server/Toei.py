from bs4 import BeautifulSoup
import requests as req


def getToeiInfomation():
    url = 'https://www.kotsu.metro.tokyo.jp/subway/schedule/'
    resultList = []

    response = req.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, "html.parser")
    operation_items = bs.find_all("dl", class_="operation__item")

    resultList = []
    for item in operation_items:
        route = item.find("dt").text.strip() # 路線名を取得
        operation_info = item.find("dd", class_="operation__info").text.strip() # 運行状況を取得
        if operation_info == '現在、１５分以上の遅延はありません。':
            operation_info = '平常運転'
        resultList.extend([route, operation_info]) # 路線名と運行状況を配列に追加

    return resultList

if __name__ == '__main__':
    print(getToeiInfomation())