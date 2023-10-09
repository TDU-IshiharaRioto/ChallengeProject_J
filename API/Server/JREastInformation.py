#運行情報の取得（関東圏JR）

from bs4 import BeautifulSoup
import requests as req


def getJREastInformation():
    url = []
    resultList = []
    url.append("https://traininfo.jreast.co.jp/train_info/kanto.aspx")
    url.append("https://traininfo.jreast.co.jp/train_info/tohoku.aspx")
    url.append("https://traininfo.jreast.co.jp/train_info/shinetsu.aspx")
    url.append("https://traininfo.jreast.co.jp/train_info/chyokyori.aspx")
    url.append("https://traininfo.jreast.co.jp/train_info/shinkansen.aspx")

    for i in range(len(url)):
        responce = req.get(url[i])
        responce.encoding = responce.apparent_encoding

        bs = BeautifulSoup(responce.text, "html.parser")

        lineList = bs.find_all ("span", class_="name")
        statusList = bs.find_all ("div", class_="rosen_infoBox")

        for i in range(len(lineList)):
            resultList.append(lineList[i].getText())
            resultList.append(statusList[i].getText().replace("\n", ""))
            # print(lineList[i].getText() + " " + statusList[i].getText().replace("\n", ""))

    return resultList

def getJREastTohokuInformation():
    url = "https://traininfo.jreast.co.jp/train_info/tohoku.aspx"

    responce = req.get(url)
    responce.encoding = responce.apparent_encoding

    bs = BeautifulSoup(responce.text, "html.parser")

    lineList = bs.find_all ("span", class_="name")
    statusList = bs.find_all ("div", class_="rosen_infoBox")

    resultList = []

    for i in range(len(lineList)):
        resultList.append(lineList[i].getText())
        resultList.append(statusList[i].getText().replace("\n", ""))
        # print(lineList[i].getText() + " " + statusList[i].getText().replace("\n", ""))
    return resultList

def getShinkansenInformation():
    TokaiUrl = "https://traininfo.jr-central.co.jp/shinkansen/pc/ja/index.html"
    HokkaidouUrl = "https://www3.jrhokkaido.co.jp/webunkou/senku.html?id=24"
    WestSanyoUrl = "https://trafficinfo.westjr.co.jp/sanyo.html"
    WestHokurikuUrl = "https://trafficinfo.westjr.co.jp/h_shinkansen.html"