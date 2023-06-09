import random


def constellation(month, day):
    between = lambda m,M,x : m <= x and x <= M
    
    # 2月や4月など、月によって日数が異なる場合に注意
    # 定義域チェックは完璧ではない
    if(not(between(1,12,month) and between(1,31,day))):
        return "Domain Error"

    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "水瓶座"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "魚座"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "牡羊座"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "牡牛座"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "双子座"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "蟹座"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "獅子座"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "乙女座"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
        return "天秤座"
    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return "蠍座"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
        return "射手座"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "山羊座"
    
    return "Not Found"

def fortune_telling():
    fortunes = [
        "今日はあなたにとって成功と幸運の日です。周囲の人々とのコミュニケーションが円滑になり、新しいチャンスが訪れるでしょう。自信を持って行動し、大きな目標に向かって前進してください。",
        "今日は財運が向上する日です。お金に関連する機会や出費が増えるかもしれませんが、しっかりと管理すれば成功への一歩となるでしょう。自分の価値を認め、賢明な選択をしてください。",
        "今日はリラックスして過ごすことが大切な日です。ストレスやプレッシャーを感じるかもしれませんが、ヨガや瞑想などのリラックス方法を取り入れることで心を落ち着かせることができるでしょう。自分自身を大切にしましょう。",
        "今日は創造力が高まる日です。新しいアイデアやプロジェクトに取り組むと良い結果を得られるでしょう。周囲の人々とのコラボレーションも成功する可能性があります。自分の才能を信じて行動しましょう。",
        "今日は内面の成長と洞察力が深まる日です。自己啓発やスピリチュアルな活動に時間を割くと良いでしょう。また、他の人の意見や知識にも耳を傾けることで新たな気づきが得られるかもしれません。自分自身との対話を大切にしましょう。",
        "今日は愛情や幸福があなたに満ちる日です。家族やパートナーとの絆が深まり、楽しい時間を過ごすことができるでしょう。感謝の気持ちを忘れずに相手に対して思いやりを示しましょう。",
        "今日は行動力が求められる日です。新しいチャレンジやプロジェクトに積極的に取り組みましょう。自分の能力を信じて、勇気を持って前進してください。困難に立ち向かうことで成長が生まれます。",
        "今日は内なる自己と向き合う日です。静かな環境で思考や瞑想に集中し、自分自身の目標や価値観を再確認すると良いでしょう。自分自身に素直になり、内なる声を聴くことで新たな気づきが得られるかもしれません。",
        "今日は繁栄と成功のチャンスが巡ってくる日です。新しいビジネスや投資などの機会が訪れるかもしれません。チャンスを逃さず、冷静な判断をして行動しましょう。運気が高まっているので、大胆な目標に向かって進んでください。",
        "今日はバランスと安定が求められる日です。スケジュールや計画を整理し、優先順位を明確にすることで効率的に行動することができるでしょう。物事を客観的に考え、冷静な判断を下してください。",
        "今日は新しい出会いや人間関係の拡大のチャンスがあります。積極的にコミュニケーションを取り、人とのつながりを大切にしましょう。新たなアイデアや視点を得ることができるでしょう。",
        "今日は集中力が高まる日です。目標に向かって一点集中し、タスクを片付けると良い結果を得られるでしょう。外部からの干渉を避け、自分自身に集中することが大切です。",
        "今日は冒険心とチャレンジ精神が湧いてくる日です。新しい経験や挑戦を積極的に受け入れましょう。恐れや心配を捨てて、大胆に行動することで成長が生まれます。",
        "今日は感謝と思いやりの気持ちが重要な日です。周囲の人々への感謝を忘れずに、助け合いや思いやりの行動を心がけましょう。善意が周りに広がり、良い結果をもたらすでしょう。",
        "今日は自己表現と創造力が高まる日です。アートや音楽、執筆など、自分の才能を開花させる活動に積極的に取り組んでください。自己の個性を大切にし、自由な表現を楽しんでください。",
        "今日は運気が安定している日です。穏やかな日常を過ごし、自分自身との調和を保つことが大切です。日常のルーティンに従いつつ、心地よい余暇を楽しんでください。",
        "今日は学びと知識の獲得が重要な日です。新しいスキルや知識を身につける機会が訪れるでしょう。自己啓発や学習に時間を割くことで、将来の成長に繋げることができます。",
        "今日は感情のバランスを保つことが重要な日です。ストレスや不安が襲ってくるかもしれませんが、冷静さを保ち、感情に振り回されないようにしましょう。心の安定を保つことが大切です。",
        "今日は人間関係の調和が重要な日です。他人との協力やコミュニケーションが円滑に進み、良い関係を築くことができるでしょう。思いやりと優しさを忘れずに接することが大切です。",
        "今日は自己信頼と自己表現が重要な日です。自分の考えや意見を自信を持って表現しましょう。他人の評価に囚われず、自分自身を信じることが大切です。",
        "今日は冷静な判断力と決断力が必要な日です。重要な選択や決断が迫られるかもしれませんが、情報を収集し、冷静な思考を持って判断してください。自分自身の直感にも耳を傾けましょう。"
    ]

    random_index = random.randint(0, len(fortunes)-1)
    fortune = fortunes[random_index]

    return fortune

def lucky_item():
    items = [
        "キーチェーン",
        "ペン",
        "ブレスレット",
        "ネックレス",
        "財布",
        "パワーストーン",
        "アクセサリー",
        "手帳",
        "スマートフォンケース",
        "お守り",
        "ハンカチ",
        "ハンドクリーム",
        "ボールペン",
        "ノート",
        "ヘアゴム",
        "鉛筆"
    ]


    random_index = random.randint(0, len(items)-1)
    item = items[random_index]

    return item

def lucky_color():
    colors = [
        "シアン",
        "ベージュ",
        "マゼンタ",
        "アクア",
        "ターコイズ",
        "ライム",
        "オリーブ",
        "カラフル",
        "バイオレット",
        "サーモン",
        "グラデーション",
        "ブラック",
        "ホワイト",
        "レッド",
        "ブルー",
        "イエロー",
        "グリーン",
        "ピンク",
        "オレンジ",
        "パープル"
    ]


    random_index = random.randint(0, len(colors)-1)
    color = colors[random_index]

    return color

def main():
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    print("birth : " + str(month) + "/" + str(day))
    
    print(fortune_telling())
    print(constellation(month, day))
    print(lucky_item())
    print(lucky_color())



if __name__ == "__main__":
    main()

