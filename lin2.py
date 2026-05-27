import os
import requests
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_IDS = os.getenv("TG_CHAT_IDS_LIN", "").split(",")

APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.luckygame.spinwheel",
]

def send_tg(msg):
    for chat_id in CHAT_IDS:
        chat_id = chat_id.strip()
        if not chat_id:
            continue
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": msg,
                # "disable_web_page_preview": True
            }
            r = requests.post(url, json=data, timeout=10)
            print(f"✅ 发送到 {chat_id} 结果: {r.status_code}")
        except Exception as e:
            print(f"❌ 发送失败 {chat_id}: {str(e)}")

def check_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        return r.status_code == 200
    except:
        return False

if __name__ == "__main__":
    now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    online = []
    offline = []
    for link in APP_LIST:
        if check_link(link):
            online.append(link)
        else:
            offline.append(link)

    content = "\n".join([
        "【谷歌应用状态巡检】",
        f"巡检时间：{now} 北京时间",
        f"正常应用：{len(online)} 个",
        f"离线应用：{len(offline)} 个",
        "",
        "✅ 正常链接：",
        "\n".join(online) if online else "无",
        "",
        "❌ 离线链接：",
        "\n".join(offline) if offline else "无"
    ])
    send_tg(content)
