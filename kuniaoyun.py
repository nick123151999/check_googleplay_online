import os
import urllib.request
import urllib.parse
from datetime import datetime

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
# 新群组ID
TARGET_CHAT_ID = "-1001661572274"

def send_tg(msg):
    try:
        api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        post_data = urllib.parse.urlencode({"chat_id": TARGET_CHAT_ID, "text": msg}).encode("utf-8")
        req = urllib.request.Request(api, data=post_data, method="POST")
        with urllib.request.urlopen(req, timeout=10):
            print("广告消息发送成功")
    except Exception as e:
        print(f"发送失败: {e}")

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ad_content = f"""🔥谷歌上架渠道接单🔥
可接谷歌上架业务，APP不限类型，稳定出包
欢迎咨询，需要的直接私聊！
发送时间：{now}"""
    send_tg(ad_content)
