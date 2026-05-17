import requests
import os

# 读取密钥
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# 你的APP列表
APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
]

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

# 🔥 修复后的精准检测：只在真下架时报警
def check_app_status(url):
    try:
        res = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )

        # 只有 404 / 页面找不到 才算真正下架
        if res.status_code == 404:
            return False
        if "Not Found" in res.text or "此应用不存在" in res.text or "找不到应用" in res.text:
            return False

        # 其他情况一律算正常（不会误报）
        return True

    except Exception:
        # 网络错误、超时 → 不算下架
        return True

# 主程序
if __name__ == "__main__":
    down_list = []

    for app in APP_LIST:
        if not check_app_status(app):
            down_list.append(app)

    if down_list:
        msg = "⚠️ *APP 下架告警*\n\n"
        msg += f"异常数量：{len(down_list)}\n\n"
        msg += "\n".join(down_list)
        send_telegram(msg)
        print("发送告警成功")
    else:
        print("✅ 全部APP正常")
