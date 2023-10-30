import requests as req
import json
from bs4 import BeautifulSoup

def getTobuRailwayInformation():
    url = []
    url.append('https://www.tobu.co.jp/service_status/')
    LineList = getTobuLineList()
    contentNormal = '平常どおり運転しています。	'
    

    resultList = []

    for i in range(len(url)):
        responce = req.get(url[i])
        print (responce.text)
        bs = BeautifulSoup(responce.text, "html.parser")
        statusList = bs.find_all ("tbody")

        for l in range(len(statusList)):
            print ('**********')
            byte_string = statusList[l].getText().replace('\n', '').encode()
            decoded_string = byte_string.decode('utf-8')
            print(decoded_string)
            print ('***********')
        
        for i in range(len(statusList)):
            print(statusList[i].getText().replace('\n', ''))
            # resultList.append(LineList[i])
            # resultList.append(statusList[i].getText().replace('\n', ''))

    return resultList

def getTobuLineList():
    url = []
    resultList = []
    url.append('https://www.tobu.co.jp/service_status/')

    for i in range(len(url)):
        responce = req.get(url[i])
        responce.encoding = responce.apparent_encoding

        bs = BeautifulSoup(responce.text, "html.parser")

        lineList = bs.find_all ("td")

        for line in lineList:
            data = line.getText().replace('\n', '')
            if data != "" and data != " ":
                resultList.append(data.replace('\u3000', ''))

    return resultList

if __name__ == "__main__":
    print(getTobuRailwayInformation())