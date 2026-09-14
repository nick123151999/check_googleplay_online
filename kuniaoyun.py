from pyrogram import Client
from datetime import datetime
import os

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH"))
session_str = os.getenv("TG_SESSION_STR")
target_chat_id = "-1001661572274"

app = Client(
    ":memory:",
    api_id=api_id,
    api_hash=api_hash,
    session_string=session_str
)

async def send_ad_message():
    try:
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ad_text = f"""🔥谷歌上架渠道接单🔥
可接谷歌上架业务，APP不限类型，稳定出包
欢迎咨询，需要的直接私聊！
推送时间：{now_time}"""
        async with app:
            await app.send_message(target_chat_id, ad_text)
        print("✅消息发送成功")
    except Exception as e:
        print(f"❌发送失败，错误详情：{e}")

app.run(send_ad_message())
