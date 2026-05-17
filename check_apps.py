import os
import urllib.request
import urllib.parse
import time
from datetime import datetime, timedelta

# 密钥配置（从GitHub Secrets读取）
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# 监控列表
APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
    "https://play.google.com/store/apps/details?id=com.sz99.jiuqian.wallet",
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

# 检查APP是否在线
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

# 执行一次巡检
def run_check():
    now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    normal = []
    down = []

    for url in APP_LIST:
        try:
            if check_ok(url):
                normal.append(url)
            else:
                down.append(url)
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

# ==========================================
# 自动循环：每 1小时 执行一次（3600秒）
# ==========================================
if __name__ == "__main__":
    while True:
        run_check()
        print("⏱ 等待 1 小时后再次检查...")
        time.sleep(3600)  # 这里就是1小时
