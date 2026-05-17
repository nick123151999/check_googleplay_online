import requests
import os

# 读取密钥
BOT_TOKEN = os.getenv("8754776183:AAFKZrLrH4_tnB-lBghOePH5LErnIPWPTCo")
CHAT_ID = os.getenv("361699392")

# ============在这里粘贴你所有APP链接============
APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026",
    "https://play.google.com/store/apps/details?id=com.gamesters.gridora",
    "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame",
    # "https://play.google.com/store/apps/details?id=填写包名链接4",
    # "https://play.google.com/store/apps/details?id=填写包名链接5"
    # 继续往下粘贴满20个
]
# ============================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 11) Chrome/120.0.0.0 Mobile Safari/537.36"
}

def send_telegram(message):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(api_url, json=data, timeout=10)
    except Exception as e:
        print("发送TG消息失败", e)

def check_app_status(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        # 判定下架
        if res.status_code != 200 or "Not Found" in res.text:
            return False
        return True
    except:
        return False

if __name__ == "__main__":
    abnormal = []
    for app_url in APP_LIST:
        if not check_app_status(app_url):
            abnormal.append(app_url)

    if abnormal:
        tip = f"【APP下架告警】\n异常数量：{len(abnormal)} 个\n\n"
        tip += "\n".join(abnormal)
        send_telegram(tip)
