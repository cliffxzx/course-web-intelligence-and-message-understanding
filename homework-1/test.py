import re
import requests
import pandas as pd
import time
from tqdm import trange


# 影片頁面點選“瀏覽器位址列小鎖-Cookie-bilibili.com-Cookie-SESSDATA”進行獲取
SESSDATA = ""
# 影片頁面“按F12-Console-輸入document.cookie”進行獲取
cookie = ""
cookie += f";SESSDATA={SESSDATA}"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "cookie": cookie,
}


def get_info(vid):
    url = f"https://api.bilibili.com/x/web-interface/view/detail?bvid={vid}"
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    data = response.json()
    info = {}
    info["標題"] = data["data"]["View"]["title"]
    info["總彈幕數"] = data["data"]["View"]["stat"]["danmaku"]
    info["影片數量"] = data["data"]["View"]["videos"]
    info["cid"] = [dic["cid"] for dic in data["data"]["View"]["pages"]]
    if info["影片數量"] > 1:
        info["子標題"] = [dic["part"] for dic in data["data"]["View"]["pages"]]
    for k, v in info.items():
        print(k + ":", v)
    return info


def get_danmu(info, start='2022-3-26', end='2022-3-27'):
    date_list = [i for i in pd.date_range(start, end).strftime("%Y-%m-%d")]
    all_dms = []
    for i, cid in enumerate(info["cid"]):
        dms = []
        for j in trange(len(date_list)):
            url = f"https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={cid}&date={date_list[j]}"
            response = requests.get(url, headers=headers)
            response.encoding = "utf-8"
            data = re.findall(r"[:](.*?)[@]", response.text)
            dms += [dm[1:] for dm in data]
        if info["影片數量"] > 1:
            print("cid:", cid, "彈幕數:", len(dms), "子標題:", info["子標題"][i])
        all_dms += dms
    print(f"共獲取彈幕{len(all_dms)}條！")
    return all_dms


if __name__ == "__main__":
    ids = [
    "BV1Bb4y167sQ",
    "BV1Bb4y167sQ",
    "BV1jP4y1p7gU",
    "BV1jP4y1p7gU",
    "BV1Fa411m7M2",
    "BV1Fa411m7M2",
    "BV1TL4y1p72q",
    "BV1TL4y1p72q",
    "BV1YT4y1X72Z",
    "BV1YT4y1X72Z",
    "BV1H44y1p7Dy",
    "BV1H44y1p7Dy",
    "BV1FF411p7ZA",
    "BV1FF411p7ZA",
    "BV11u411X7b9",
    "BV11u411X7b9",
    "BV1e44y1N72u",
    "BV1e44y1N72u",
    "BV1vZ4y1Z7eJ",
    "BV1vZ4y1Z7eJ",
    "BV12L411T7bQ",
    "BV12L411T7bQ",
    "BV1Q3411s7nc",
    "BV1Q3411s7nc",
    "BV1S34y127cu",
    "BV1S34y127cu",
    "BV1oL4y1B7SV",
    "BV1oL4y1B7SV",
    "BV1EZ4y1C7H1",
    "BV1EZ4y1C7H1",
    "BV1Yq4y1v7m2",
    "BV1KY411H7Dc",
    "BV1HL4y177t7",
    "BV1sL4y177YJ",
    "BV1r44y1N7MP",
    "BV1e44y1N72u",
    "BV1Hi4y1k7dH",
    "BV1gr4y167ee",
    "BV16i4y1k7Zm",
    "BV1Z94y1Z76T",
    "BV1y34y1B7vm",
    "BV1y34y1B7vm",
    "BV1Zw41197gR",
    "BV1Zw41197gR",
    "BV1PF411p7jY",
    "BV1PF411p7jY",
    "BV1Uu41127mP",
    "BV1Uu41127mP",
    "BV1dK4y1d7ux",
    "BV1dK4y1d7ux",
    "BV1UY411b7Ey",
    "BV1UY411b7Ey",
    "BV13Q4y1o7Hz",
    "BV13Q4y1o7Hz",
    "BV1U5411w74d",
    "BV1U5411w74d",
    "BV1P44y1L7dj",
    "BV1P44y1L7dj",
    "BV1hb4y1Q7vE",
    "BV1hb4y1Q7vE",
    "BV1ML4y1M7cL",
    "BV1ML4y1M7cL",
    "BV1PX4y1g7cm",
    "BV1PX4y1g7cm",
    "BV1hU4y1a7jN",
    "BV1hU4y1a7jN",
    "BV1Gf4y1x71h",
    "BV1Gf4y1x71h",
    "BV1dh411S7S6",
    "BV1dh411S7S6",
    "BV17Z4y1A7TX",
    "BV17Z4y1A7TX",
    "BV1N64y187cy",
    "BV1N64y187cy",
    "BV1fr4y1v74C",
    "BV1fr4y1v74C",
    "BV1cF411i7Th",
    "BV1cF411i7Th",
    "BV1Br4y1Y7Er",
    "BV1Br4y1Y7Er",
    "BV1Xx411c7cH"
]
    for vid in ids:
        info = get_info(vid)
        danmu = get_danmu(info)
        with open("danmu.txt", "w", encoding="utf-8") as fout:
            for dm in danmu:
                fout.write(dm + "\n")