import os
import requests
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
# 多个群 ID 用英文逗号分隔
CHAT_IDS_RAW = os.getenv("TG_CHAT_IDS_LIN", "TG_CHAT_IDS_LIN2")
CHAT_IDS = [cid.strip() for cid in CHAT_IDS_RAW.split(",") if cid.strip()]

APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.luckygame.spinwheel",
]

def send_tg_all(msg):
    if not BOT_TOKEN or not CHAT_IDS:
        print("❌ 缺少 Token 或群 ID")
        return
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for cid in CHAT_IDS:
        payload = {
            "chat_id": cid,
            "text": msg,
            "disable_web_page_preview": True
        }
        try:
            r = requests.post(api_url, json=payload, timeout=15)
            print(f"→ 发往 {cid}：HTTP {r.status_code}")
            r.raise_for_status()
        except Exception as e:
            print(f"❌ 发往 {cid} 失败：{e}")

def check_link(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        return r.status_code == 200
    except Exception as e:
        print("⚠️ 链接检查失败：", url, e)
        return False

if __name__ == "__main__":
    now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    online = [link for link in APP_LIST if check_link(link)]
    offline = [link for link in APP_LIST if not check_link(link)]

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
    print("准备发送：\n", content)
    send_tg_all(content)
