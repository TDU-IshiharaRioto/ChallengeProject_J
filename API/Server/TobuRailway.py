import requests as req
import xml.etree.ElementTree as ET

def getTobuRailwayInformation():
    url = "https://www.tobu.co.jp/file/trainop/trainop.xml"
    contentNormal = '平常どおり運転しています。'

    statusList = []
    lineList = []
    
    responce = req.get(url)
    responce.encoding = responce.apparent_encoding
    xmlData = responce.text
    root = ET.fromstring(xmlData)

    lineTag = 'line'
    statusTag = 'description'
    for line in root.iter(lineTag):
        text = ET.tostring(line, encoding='utf-8').decode('utf-8')
        text = text.replace('<line>', '').replace('</line>', '').replace('\n', '').replace(' ', '').replace('\u3000', ' ')
        lineList.append(text)

    i = 0
    for status in root.iter(statusTag):
        text = ET.tostring(status, encoding='utf-8').decode('utf-8')
        text = text.replace('<description>', '').replace('</description>', '').replace('\n', '').replace(' ', '').replace('\u3000', ' ')
        statusList.append(lineList[i])
        if text == contentNormal:
            statusList.append('平常運転')
        else:
            statusList.append(text)
        i = i + 1
    
    return statusList


        

if __name__ == "__main__":
    print (getTobuRailwayInformation())