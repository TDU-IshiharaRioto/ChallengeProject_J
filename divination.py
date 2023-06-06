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
        "大吉",
        "中吉",
        "小吉",
        "吉",
        "凶",
        "大凶"
    ]

    random_index = random.randint(0, len(fortunes)-1)
    fortune = fortunes[random_index]

    return fortune

def lucky_item():
    items = [
        "ラッキーアイテム1",
        "ラッキーアイテム2",
        "ラッキーアイテム3",
        "ラッキーアイテム4",
        "ラッキーアイテム5",
        "ラッキーアイテム6",
        "ラッキーアイテム7",
        "ラッキーアイテム8",
        "ラッキーアイテム9",
        "ラッキーアイテム10"
    ]

    random_index = random.randint(0, len(items)-1)
    item = items[random_index]

    return item

def lucky_color():
    colors = [
        "赤",
        "青",
        "黄",
        "緑",
        "紫",
        "白",
        "黒"
    ]

    random_index = random.randint(0, len(colors)-1)
    color = colors[random_index]

    return color

def main():
    print(fortune_telling())
    print(constellation(1, 20))
    print(lucky_item())
    print(lucky_color())


main()