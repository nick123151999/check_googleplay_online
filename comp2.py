import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID_COMP2")

# 填写公司2谷歌商店完整链接
APP_LIST = [
     "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
    "https://play.google.com/store/apps/details?id=com.idolive.fishingwars",
]

def send_tg(msg):
    try:
        api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        post_data = urllib.parse.urlencode({"chat_id":CHAT_ID,"text":msg}).encode("utf-8")
        req = urllib.request.Request(api, data=post_data, method="POST")
        with urllib.request.urlopen(req, timeout=10):
            pass
    except:
        pass

def check_link(url):
    try:
        header = {"User-Agent":"Mozilla/5.0"}
        req = urllib.request.Request(url, headers=header)
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.getcode() == 200
    except Exception as e:
        err = str(e).lower()
        if "404" in err or "410" in err:
            return False
        return True

if __name__ == "__main__":
    now_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    online = []
    offline = []
    for link in APP_LIST:
        if check_link(link):
            online.append(link)
        else:
            offline.append(link)

    content = "\n".join([
        "【googleplay应用状态巡检】",
        f"巡检时间：{now_time} 北京时间",
        f"正常应用：{len(online)} 个",
        f"下架应用：{len(offline)} 个",
        "",
        "✅ 正常链接：",
        "\n".join(online) if online else "无",
        "",
        "❌ 下架链接：",
        "\n".join(offline) if offline else "无"
    ])
    send_tg(content)
