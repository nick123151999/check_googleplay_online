import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# ===================== 【配置区域】 =====================
# TG 机器人 Token（从 Secrets 读取）
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# 群ID配置：兼容 单个群ID / 多个群ID（英文逗号分隔）
def get_chat_ids(var_name):
    raw = os.getenv(var_name, "").strip()
    return [cid.strip() for cid in raw.split(",") if cid.strip()]

# ========== 【多群发送配置】 ==========
# 一个 Secrets = 一个群，安全不乱
# 加群只需要复制下面一行，改数字即可
CHAT_IDS = []
CHAT_IDS.extend(get_chat_ids("TG_CHAT_ID_DAHU"))       # 默认群（你原来的）
# CHAT_IDS.extend(get_chat_ids("TG_CHAT_ID_COMP2"))  # 第二个群（复制这行加群）
# CHAT_IDS.extend(get_chat_ids("TG_CHAT_ID_COMP3"))  # 第三个群
# CHAT_IDS.extend(get_chat_ids("TG_CHAT_ID_COMP4"))  # 第四个群
# ======================================

# 应用列表：(渠道号, 谷歌商店链接)
APP_LIST = [
    ("hwpg_1394", "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026"),
    ("hwpg_1395", "https://play.google.com/store/apps/details?id=com.gamesters.gridora"),
    ("hwpg_1396", "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame"),
    ("hwpg_1398", "https://play.google.com/store/apps/details?id=com.majiang.luckymajiang"),
    ("hwpg_1399", "https://play.google.com/store/apps/details?id=com.pandamajiang.panda001"),
]

# ---------------------
# 发送 TG 消息（支持多群）
# ---------------------
def send_tg(msg):
    for chat_id in CHAT_IDS:
        if not chat_id:
            continue
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": chat_id, "text": msg}
            req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
            with urllib.request.urlopen(req, timeout=10):
                pass
        except:
            pass

# ---------------------
# 检查应用是否可访问（正常/下架）
# ---------------------
def check_ok(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=15) as f:
            return f.getcode() == 200
        except Exception as e:
            err = str(e).lower()
        # 出现 404 / 410 判定为已下架
        if "404" in err or "410" in err:
            return False
        return True

# ---------------------
# 巡检主逻辑
# ---------------------
def run_check():
    # 获取当前北京时间
    now = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    normal = []  # 正常应用
    down = []    # 下架应用

    # 遍历检查每个应用
    for tag, url in APP_LIST:
        try:
            content = f"{tag}：{url}"
            if check_ok(url):
                normal.append(content)
            else:
                down.append(content)
        except:
            continue

    # 构造推送消息
    text = "\n".join([
        "【谷歌应用定时巡检播报】",
        f"巡检时间：{now} (北京时间)",
        f"正常上架：{len(normal)} 个",
        f"已下架应用：{len(down)} 个",
        "",
        "✅正常：",
        "\n".join(normal) if normal else "无",
        "",
        "❌下架：",
        "\n".join(down) if down else "无"
    ])
    
    # 发送消息
    send_tg(text)
    print("✅ 巡检完成")

# ---------------------
# 程序入口（只执行一次）
# ---------------------
if __name__ == "__main__":
    run_check()
