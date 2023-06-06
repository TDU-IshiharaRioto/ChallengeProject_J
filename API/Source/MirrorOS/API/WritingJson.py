##################################################
# WritingJson.py
# 入力されたJsonオブジェクトをファイルに書き込む関数を定義するクラスです
# (C) 2023 IshiharaRioto
##################################################

import json

# Jsonオブジェクトをファイルに書き込みます
# 引数は、Jsonオブジェクトとファイル名です
# 戻り値は、ありません
# 失敗するとそれに応じたExceptionをraiseします

def writeJson (data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise e