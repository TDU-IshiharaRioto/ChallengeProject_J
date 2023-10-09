#運行情報の取得（関東圏JR）

from bs4 import BeautifulSoup
import requests as req

def getJREastInformation():
    url = "https://www.tokyometro.jp/"

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