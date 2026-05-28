import os
import requests
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# ===================== 多群发送（兼容1个/多个群ID） =====================
def get_chat_ids(var_name):
    raw = os.getenv(var_name, "").strip()
    return [cid.strip() for cid in raw.split(",") if cid.strip()]

CHAT_IDS = []
CHAT_IDS += get_chat_ids("TG_CHAT_IDS_LIN")
# ======================================================================

# 格式：(渠道号, 链接) → 自动带编号
APP_LIST = [
    ("gp_001", "https://play.google.com/store/apps/details?id=com.luckygame.spinwheel"),
    # 以后加应用就这样加：
    # ("gp_002", "https://play.google.com/xxx"),
]

def send_tg(msg):
    for chat_id in CHAT_IDS:
        if not chat_id:
            continue
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": msg,
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

    # 自动编号 + 渠道号
    for idx, (channel_tag, link) in enumerate(APP_LIST, 1):
        try:
            line = f"{idx}. {channel_tag}  {link}"
            if check_link(link):
                online.append(line)
            else:
                offline.append(line)
        except:
            continue

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
