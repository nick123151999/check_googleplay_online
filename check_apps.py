import os
import urllib.request
from datetime import datetime

# 配置信息（从GitHub密钥读取，无需修改）
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# 需要监控的APP列表（已包含你要检测的所有应用）
APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
    "https://play.google.com/store/apps/details?id=com.sz99.jiuqian.wallet",
]

# 发送消息到TG
def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = f"chat_id={CHAT_ID}&text={msg}".encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10):
            pass
    except:
        pass

# 精准判断APP是否在线（只认404为下架，网络问题不算）
def check_ok(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=15) as f:
            return f.getcode() == 200
    except Exception as e:
        err_info = str(e)
        # 只有返回404/410，才判定为已下架
        if "404" in err_info or "410" in err_info:
            return False
        # 网络超时/被墙等错误 → 一律视为正常，避免误报
        return True

# 主执行程序
if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normal_apps = []
    down_apps = []

    for app_url in APP_LIST:
        package_name = app_url.split("id=")[-1]
        if check_ok(app_url):
            normal_apps.append(package_name)
        else:
            down_apps.append(package_name)

    # 组装播报消息
    report = f"""【谷歌应用定时巡检播报】
巡检时间：{now}
正常上架：{len(normal_apps)} 个
已下架应用：{len(down_apps)} 个

✅ 正常在线：
{"\n".join(normal_apps) if normal_apps else "无"}

❌ 已下架：
{"\n".join(down_apps) if down_apps else "无"}
"""
    # 发送并打印
    send_tg(report)
    print("巡检完成，消息已推送")
