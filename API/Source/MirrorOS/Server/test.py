import asyncio
import websockets
import JREastInformation as jre

foundLine = '常磐線快速電車'

resultList = []
jre = jre.getJREastInformation()
print(jre)

for i in range(len(jre)):
    if jre[i] == foundLine:
        print(jre[i] + "は、" + jre[i+1] + "です。")
    
    if i == len(jre) - 1:
        print("見つかりませんでした。")