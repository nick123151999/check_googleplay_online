import requests
import os

# ========== 正确读取 GitHub 密钥（不要改这里！）==========
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# ============ 你的APP列表 ============
APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
]
# ======================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 11) Chrome/120.0.0.0 Mobile Safari/537.36"
}

# 发送 TG 消息
def send_telegram(message):
    try:
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(api_url, json=payload, timeout=15)
    except Exception as e:
        print("发送失败:", e)

# 检测 APP 是否在架
def check_app_status(url):
    try:
        res = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )
        # 真正下架才返回 False
        if res.status_code in (404, 410, 403):
            return False
        if "Not Found" in res.text or "找不到" in res.text:
            return False
        return True
    except:
        return True  # 网络问题不算下架

# 主程序
if __name__ == "__main__":
    down_list = []

    for app in APP_LIST:
        if not check_app_status(app):
            down_list.append(app)

    # 有下架才发消息
    if down_list:
        msg = "⚠️ *APP 下架告警*\n\n"
        msg += f"异常数量：{len(down_list)}\n\n"
        msg += "\n".join(down_list)
        send_telegram(msg)
        print("发送告警成功")
    else:
        print("✅ 全部APP正常")
