import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# 读取并解析群ID，兼容：单个ID / 多个ID(英文逗号分隔)
def get_chat_ids(var_name):
    raw = os.getenv(var_name, "")
    return [cid.strip() for cid in raw.split(",") if cid.strip()]

# 加载所有群ID
CHAT_IDS = []
CHAT_IDS.extend(get_chat_ids("TG_CHAT_ID_OWN"))
# CHAT_IDS.extend(get_chat_ids("TG_CHAT_ID_COMP2"))

# 格式：(渠道编号, 谷歌商店链接)
APP_LIST = [
    ("gp_001", "https://play.google.com/store/apps/details?id=com.pandamajiang.panda001"),
    ("gp_002", "https://play.google.com/store/apps/details?id=com.game78.fishgoo"),
    ("gp_003", "https://play.google.com/store/apps/details?id=com.khalidy.fortunecatch"),
    ("gp_004", "https://play.google.com/store/apps/details?id=com.idolive.fishingwars"),
    ("gp_005", "https://play.google.com/store/apps/details?id=com.tigerplinko.plinkogame"),
    ("gp_006", "https://play.google.com/store/apps/details?id=com.majiang.luckymajiang"),
    # ("gp_007", "https://play.google.com/store/apps/details?id=com.gamesters.gridora"),
    ("gp_008", "https://play.google.com/store/apps/details?id=com.todomaskj.toshhks2026"),
    ("gp_009", "https://play.google.com/store/apps/details?id=com.maxminder2.feedbackhub"),
    ("gp_010", "https://play.google.com/store/apps/details?id=com.maxminder1.helixflow"),
    ("gp_011", "https://play.google.com/store/apps/details?id=com.tigerfruite.match2"),
    ("gp_012", "https://play.google.com/store/apps/details?id=com.vikas.kaifeducation"),
    ("gp_013", "https://play.google.com/store/apps/details?id=com.rabbitsgame.slotsgogo2026"),
    ("gp_014", "https://play.google.com/store/apps/details?id=com.tigeranddragon.doocosj2026"),
    ("gp_015", "https://play.google.com/store/apps/details?id=com.NimbusDash.hks"),
    ("gp_016", "https://play.google.com/store/apps/details?id=com.luckygame.spinwheel"),
    ("gp_017", "https://play.google.com/store/apps/details?id=com.icefallrescue.app"),
    ("gp_018", "https://play.google.com/store/apps/details?id=com.plinkogame.tigerplinko"),
    ("gp_019", "https://play.google.com/store/apps/details?id=com.foxgamec.foxgames2026"),
    ("gp_020", "https://play.google.com/store/apps/details?id=com.magicgames.rabbit"),
    ("gp_021", "https://play.google.com/store/apps/details?id=com.rabbitstory.discovery2026"),
    ("gp_022", "https://play.google.com/store/apps/details?id=com.pandagame.pandamatch3"),
    ("gp_023", "https://play.google.com/store/apps/details?id=com.majiangganme.majiang"),
    ("gp_024", "https://play.google.com/store/apps/details?id=com.pandagame.majiang002"),
    ("gp_025", "https://play.google.com/store/apps/details?id=com.pandangame.majiangtooo003"),
    ("gp_026", "https://play.google.com/store/apps/details?id=com.pandamajiang.majiang004"),
    ("gp_027", "https://play.google.com/store/apps/details?id=com.pamdhh.majianggame005"),
    ("gp_028", "https://play.google.com/store/apps/details?id=com.pamdhh.majianggame006"),
    ("gp_029", "https://play.google.com/store/apps/details?id=pak.al.nasir.bugzy.tap.hunting"),
    ("gp_030", "https://play.google.com/store/apps/details?id=com.nafay.drift"),
    ("gp_031", "https://play.google.com/store/apps/details?id=com.nafay.brain"),
    ("gp_032", "https://play.google.com/store/apps/details?id=com.cube.firstdream"),
    ("gp_033", "https://play.google.com/store/apps/details?id=com.playwe.gaip"),
    ("gp_034", "https://play.google.com/store/apps/details?id=com.stack.mansion"),
    ("gp_035", "https://play.google.com/store/apps/details?id=com.cgmvtwrfz.ncortwc2"),
    ("gp_036", "https://play.google.com/store/apps/details?id=com.tuhbas.ncnfu3"),
    ("gp_037", "https://play.google.com/store/apps/details?id=com.rljxmuxcjw.fpyxkfxf4"),
]

# 发送消息
def send_tg(msg):
    for chat_id in CHAT_IDS:
        try:
            api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            post_data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg}).encode("utf-8")
            req = urllib.request.Request(api, data=post_data, method="POST")
            with urllib.request.urlopen(req, timeout=10):
                pass
        except:
            pass

def check_link(url):
    try:
        header = {"User-Agent":"Mozilla/5.0"}
        req = urllib.request.Request(url, headers=header)
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.getcode() == 200
    except Exception as e:
        err = str(e).lower()
        if "404" in err or "410" in err:
            return False
        return True

if __name__ == "__main__":
    now_time = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    online = []
    offline = []

    for idx, (channel_tag, link) in enumerate(APP_LIST, 1):
        try:
            content = f"{idx}. {channel_tag}  {link}"
            if check_link(link):
                online.append(content)
            else:
                offline.append(content)
        except:
            continue

    content = "\n".join([
        "【谷歌应用状态巡检】",
        f"巡检时间：{now_time} 北京时间",
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
