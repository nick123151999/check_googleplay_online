import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# ===================== 【配置区域】 =====================
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

def get_chat_ids(var_name):
    raw = os.getenv(var_name, "").strip()
    return [cid.strip() for cid in raw.split(",") if cid.strip()]

CHAT_IDS = []
CHAT_IDS.extend(get_chat_ids("TG_CHAT_ID_DAHU"))

# 格式：(渠道号, 链接, B面审核通过时间，投放时间, 下架时间)
APP_LIST = [
    ("hwpg_1394", "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026", "2026-05-14", "2026-05-16", "2026-6-4"),
    ("hwpg_1395", "https://play.google.com/store/apps/details?id=com.gamesters.gridora", "", "", ""),
    ("hwpg_1396", "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame", "2026-05-17", "2026-05-19", ""),
    ("hwpg_1398", "https://play.google.com/store/apps/details?id=com.majiang.luckymajiang", "2026-05-20", "2026-05-21", ""),
    ("hwpg_1399", "https://play.google.com/store/apps/details?id=com.pandamajiang.panda001", "2026-05-25", "2026-05-26", ""),
]

# ---------------------
# 计算天数（只有投放时间不为空才计算）
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
            data = {"chat_id": chat_id, "text": msg, "disable_web_page_preview": True}
            req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
            with urllib.request.urlopen(req, timeout=10):
                pass
        except:
            pass

# ---------------------
# 检查应用状态
# ---------------------
def check_ok(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=15):
            return True
    except Exception as e:
        err = str(e).lower()
        if "404" in err or "410" in err:
            return False
        return True

# ---------------------
# 主巡检逻辑
# ---------------------
def run_check():
    now_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    normal = []
    down = []

    for tag, url, b_date, start_date, off_date in APP_LIST:
        try:
            days = calc_days(start_date, off_date)
            line = f"{tag}"
            if start_date.strip() and days is not None:
                if b_date.strip():
                    line += f" | B面过审：{b_date}"
                line += f" | 投放：{start_date} | 投放：{days} 天"
                if off_date.strip():
                    line += f"\n下架时间：{off_date}"
            line += f"\n{url}"
            if check_ok(url):
                normal.append(line)
            else:
                down.append(line)
        except:
            continue

    # 彻底删除多余空行，全部紧挨着
    text = "【谷歌应用定时巡检播报】\n" \
           f"巡检时间：{now_time} (北京时间)\n" \
           f"正常上架：{len(normal)} 个\n" \
           f"已下架应用：{len(down)} 个\n" \
           "✅正常：\n" + "\n".join(normal if normal else ["无"]) + "\n" \
           "❌下架：\n" + "\n".join(down if down else ["无"])
    
    send_tg(text)
    print("✅ 巡检完成")

if __name__ == "__main__":
    run_check()
