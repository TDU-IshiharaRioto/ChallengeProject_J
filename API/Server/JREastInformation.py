#運行情報の取得（関東圏JR）

from bs4 import BeautifulSoup
import requests as req


def getJREastInformation():
    url = "https://traininfo.jreast.co.jp/train_info/kanto.aspx"

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
    EastUrl = "https://traininfo.jreast.co.jp/train_info/shinkansen.aspx"
    TokaiUrl = "https://traininfo.jr-central.co.jp/shinkansen/pc/ja/index.html"
    HokkaidouUrl = "https://www3.jrhokkaido.co.jp/webunkou/senku.html?id=24"
    WestSanyoUrl = "https://trafficinfo.westjr.co.jp/sanyo.html"
    WestHokurikuUrl = "https://trafficinfo.westjr.co.jp/h_shinkansen.html"

    EastResponce = req.get(EastUrl)
    EastResponce.encoding = EastResponce.apparent_encoding
    EastBs = BeautifulSoup(EastResponce.text, "html.parser")
    EastLineList = EastBs.find_all ("span", class_="name")
    EastStatusList = EastBs.find_all ("div", class_="rosen_infoBox")

    resultList = []
    for i in range(len(EastLineList)):
        resultList.append(EastLineList[i].getText())
        resultList.append(EastStatusList[i].getText().replace("\n", ""))
    return resultList