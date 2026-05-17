import requests
import os
from datetime import datetime

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 11) Chrome/120.0.0.0 Mobile Safari/537.36"
}

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id":CHAT_ID,"text":msg}, timeout=15)
    except:
        pass

def check_ok(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 404 or "Not Found" in res.text or "此应用不存在" in res.text:
            return False
        return True
    except:
        return True

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normal = []
    down = []

    for url in APP_LIST:
        if check_ok(url):
            normal.append(url.split("id=")[-1])
        else:
            down.append(url.split("id=")[-1])

    text = f"""【谷歌应用定时巡检播报】
巡检时间：{now}
正常上架应用：{len(normal)} 个
已下架异常应用：{len(down)} 个

✅正常列表：
{chr(10).join(normal) if normal else "无"}

❌下架列表：
{chr(10).join(down) if down else "暂无下架应用"}
"""
    send_tg(text)
    print("本轮巡检完成，消息已推送")
