import os
import requests
from datetime import datetime, timedelta

# ===================== 【配置区域】 =====================
# TG 机器人 Token（从 Secrets 读取）
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# 群ID解析：兼容单个ID / 多个ID（英文逗号分隔）
def get_chat_ids(var_name):
    raw = os.getenv(var_name, "").strip()
    return [cid.strip() for cid in raw.split(",") if cid.strip()]

# ========== 【多群发送配置】 ==========
# 加群方法：复制一行 → 改数字 → Secrets 新建对应变量即可
CHAT_IDS = []
CHAT_IDS.extend(get_chat_ids("TG_CHAT_IDS_LIN"))       # lin 默认群
# CHAT_IDS.extend(get_chat_ids("TG_CHAT_IDS_LIN2"))    # 第二个群（复制加群）
# CHAT_IDS.extend(get_chat_ids("TG_CHAT_IDS_LIN3"))    # 第三个群
# ======================================

# 应用列表：(渠道号, 谷歌链接)
APP_LIST = [
    ("gp_001", "https://play.google.com/store/apps/details?id=com.luckygame.spinwheel"),
]
# ======================================================

# ---------------------
# 发送 TG 消息（支持多群）
# ---------------------
def send_tg(msg):
    for chat_id in CHAT_IDS:
        if not chat_id:
            continue
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": msg
            }
            r = requests.post(url, json=data, timeout=10)
        except Exception as e:
            pass

# ---------------------
# 检查应用是否正常/下架
# ---------------------
def check_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        return r.status_code == 200
    except:
        return False

# ---------------------
# 巡检主逻辑
# ---------------------
if __name__ == "__main__":
    now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    online = []
    offline = []

    # 自动编号 + 渠道号
    for idx, (channel_tag, link) in enumerate(APP_LIST, 1):
        try:
            line = f"{idx}. {channel_tag}  {link}"
            if check_link(link):
                online.append(line)
            else:
                offline.append(line)
        except:
            continue

    # 构造消息
    content = "\n".join([
        "【谷歌应用状态巡检】",
        f"巡检时间：{now} 北京时间",
        f"正常应用：{len(online)} 个",
        f"离线应用：{len(offline)} 个",
        "",
        "✅ 正常链接：",
        "\n".join(online) if online else "无",
        "",
        "❌ 离线链接：",
        "\n".join(offline) if offline else "无"
    ])

    send_tg(content)
