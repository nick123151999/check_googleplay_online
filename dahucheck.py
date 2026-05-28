import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# 密钥配置
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# 手动填写渠道标识+链接，自行修改前缀编号
APP_LIST = [
    ("hwpg_1394", "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026"),
    ("hwpg_1395", "https://play.google.com/store/apps/details?id=com.gamesters.gridora"),
    ("hwpg_1396", "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame"),
    ("hwpg_1398", "https://play.google.com/store/apps/details?id=com.majiang.luckymajiang"),
    ("hwpg_1399", "https://play.google.com/store/apps/details?id=com.pandamajiang.panda001"),
]

# 发送TG消息
def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg}
        req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
        with urllib.request.urlopen(req, timeout=10):
            pass
    except:
        pass

# 检查APP状态
def check_ok(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=15) as f:
            return f.getcode() == 200
    except Exception as e:
        err = str(e).lower()
        if "404" in err or "410" in err:
            return False
        return True

# 巡检逻辑
def run_check():
    now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    normal = []
    down = []

    for tag, url in APP_LIST:
        try:
            content = f"{tag}：{url}"
            if check_ok(url):
                normal.append(content)
            else:
                down.append(content)
        except:
            continue

    text = "\n".join([
        "【谷歌应用定时巡检播报】",
        f"巡检时间：{now} (北京时间)",
        f"正常上架：{len(normal)} 个",
        f"已下架应用：{len(down)} 个",
        "",
        "✅正常：",
        "\n".join(normal) if normal else "无",
        "",
        "❌下架：",
        "\n".join(down) if down else "无"
    ])
    send_tg(text)
    print("✅ 巡检完成")

if __name__ == "__main__":
    run_check()  # 只执行一次，不再循环
