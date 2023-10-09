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