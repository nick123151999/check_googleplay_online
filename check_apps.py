import os
import urllib.request
from datetime import datetime

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
]

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = f"chat_id={CHAT_ID}&text={msg}".encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10):
            pass
    except:
        pass

def check_ok(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        req = urllib.request.Request(url, headers=headers, method="GET")
        
        # 只获取状态码，不下载内容
        with urllib.request.urlopen(req, timeout=15) as f:
            code = f.getcode()
            # 200 = 正常在线
            return code == 200
    except Exception as e:
        # 404 / 410 = 应用已下架
        if "404" in str(e) or "410" in str(e):
            return False
        # 其他错误 = 网络问题 → 不算下架
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
{"\n".join(normal) if normal else "无"}

❌下架列表：
{"\n".join(down) if down else "暂无下架应用"}
"""
    send_tg(text)
    print("完成 ✅")
