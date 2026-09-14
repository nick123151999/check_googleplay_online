import os
import urllib.request
import urllib.parse
from datetime import datetime

# 配置
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TARGET_CHAT_ID = "-1001661572274"

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": TARGET_CHAT_ID,
        "text": text
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10):
            print("✅广告发送成功")
    except Exception as err:
        print(f"❌发送失败：{err}")

if __name__ == "__main__":
    # 北京时间
    bj_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # =========在这里修改你的广告语=========
    ad_text = f"""🔥谷歌上架渠道接单🔥
可接谷歌上架业务，APP不限类型，稳定出包
欢迎咨询，需要的直接私聊！
推送时间：{bj_time}"""
    # =====================================
    send_telegram_message(ad_text)
