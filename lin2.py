import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID_LIN")

print("=== 调试信息 ===")
print("BOT_TOKEN 存在:", bool(BOT_TOKEN))
print("CHAT_ID    存在:", bool(CHAT_ID))
print("CHAT_ID 值:", repr(CHAT_ID))

APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.luckygame.spinwheel",
]

def send_tg(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ 缺少环境变量，无法发送")
        return
    try:
        api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": CHAT_ID,
            "text": msg
        }).encode("utf-8")
        req = urllib.request.Request(api, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as res:
            print("✅ TG 返回码:", res.getcode())
    except Exception as e:
        print("❌ TG 发送异常:", str(e))

def check_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.getcode() == 200
    except Exception as e:
        print("⚠️ 链接异常:", url, str(e))
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
    print("准备发送内容：\n", content)
    send_tg(content)
