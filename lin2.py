import os
import requests
from datetime import datetime, timedelta
# ===================== 【配置区域】 =====================
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
def get_chat_ids(var_name):
    raw = os.getenv(var_name, "").strip()
    return [cid.strip() for cid in raw.split(",") if cid.strip()]

CHAT_IDS = []
CHAT_IDS.extend(get_chat_ids("TG_CHAT_IDS_LIN"))

# 🔥 格式：(渠道名, 链接, B面审核通过时间, 投放时间, 下架时间)
APP_LIST = [
    ("Lucky Spin Wheel Game 2026", "https://play.google.com/store/apps/details?id=com.luckygame.spinwheel", "2026-05-26", "2026-05-29", ""),
    # 继续加在这里
]

# ---------------------
# 计算存活天数
# ---------------------
def calc_days(start_date_str, end_date_str):
    try:
        if not start_date_str.strip():
            return None
        
        now = datetime.utcnow() + timedelta(hours=8)
        start = datetime.strptime(start_date_str, "%Y-%m-%d")

        if end_date_str.strip():
            end = datetime.strptime(end_date_str, "%Y-%m-%d")
        else:
            end = now

        days = (end.date() - start.date()).days
        return max(days, 0)
    except:
        return None

# ---------------------
# 发送 TG
# ---------------------
def send_tg(msg):
    for chat_id in CHAT_IDS:
        if not chat_id:
            continue
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": msg,
                "disable_web_page_preview": True
            }
            requests.post(url, json=data, timeout=10)
        except:
            pass

# ---------------------
# 检查链接状态
# ---------------------
def check_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        return r.status_code == 200
    except:
        return False

# ---------------------
# 主巡检
# ---------------------
if __name__ == "__main__":
    now_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    online = []
    offline = []

    for idx, (channel_tag, link, b_date, start_date, off_date) in enumerate(APP_LIST, 1):
        try:
            days = calc_days(start_date, off_date)
            line = f"{idx}. {channel_tag}"

            # 有投放时间才显示
            if start_date.strip() and days is not None:
                if b_date.strip():
                    line += f" | B面通过：{b_date}"
                line += f" | 投放：{start_date} | 投放：{days} 天"
                
                if off_date.strip():
                    line += f"\n下架时间：{off_date}"

            line += f"\n{link}"

            if check_link(link):
                online.append(line)
            else:
                offline.append(line)
        except:
            continue

    content = "\n".join([
        "【谷歌应用状态巡检】",
        f"巡检时间：{now_time} 北京时间",
        f"正常应用：{len(online)} 个",
        f"离线应用：{len(offline)} 个",
        "",
        "✅ 正常链接：",
        "\n\n".join(online) if online else "无",
        "",
        "❌ 下架链接：",
        "\n\n".join(offline) if offline else "无"
    ])

    send_tg(content)
