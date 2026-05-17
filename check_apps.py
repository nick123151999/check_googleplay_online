import os
import urllib.request
from datetime import datetime

# 配置
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# 你要监控的全部APP
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
        data = f"chat_id={CHAT_ID}&text={msg}".encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10):
            pass
    except:
        pass

# ✅ 核心：真正准确的判断逻辑（只认404为下架）
def check_ok(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=15) as f:
            return f.getcode() == 200
    except Exception as e:
        err = str(e)
        # 只有明确 404 / 410 才是下架
        if "404" in err or "410" in err:
            return False
        # 其他错误=网络问题 → 不算下架
        return True

# 主程序
if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normal = []
    down = []

    for url in APP_LIST:
        pkg = url.split("id=")[-1]
        if check_ok(url):
            normal.append(pkg)
        else:
            down.append(pkg)

    # 推送消息
    text = f"""【谷歌应用定时巡检播报】
巡检时间：{now}
正常上架：{len(normal)} 个
已下架应用：{len(down)} 个

✅正常：
{"\n".join(normal) if normal else "无"}

❌下架：
{"\n".join(down) if down else "无"}
"""
    send_tg(text)
    print("完成推送")
