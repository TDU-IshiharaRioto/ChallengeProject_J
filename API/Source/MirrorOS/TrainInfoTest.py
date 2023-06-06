##################################################
# TrainInfoTest.py
# 交通状況を調査する関数をテストするクラスです
# (C) 2023 IshiharaRioto
##################################################

import json
import API.Train as Train
import API.WritingJson as WritingJson

TOKEN = "ddab718aa73ce83af028fc8f518274afea4fafc21e837a1bf5387096e7ac0891"

data = Train.getStation(TOKEN)
WritingJson.writeJson(data, "Railway.json")
