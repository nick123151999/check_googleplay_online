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

# 只保留链接，移除gp渠道编号
APP_LIST = [
    "https://play.google.com/store/apps/details?id=com.game78.fishgoo",
    "https://play.google.com/store/apps/details?id=com.khalidy.fortunecatch",
    "https://play.google.com/store/apps/details?id=com.maxminder2.feedbackhub",
    "https://play.google.com/store/apps/details?id=com.maxminder1.helixflow",
    "https://play.google.com/store/apps/details?id=com.tigerfruite.match2",
    "https://play.google.com/store/apps/details?id=com.vikas.kaifeducation",
    "https://play.google.com/store/apps/details?id=com.rabbitsgame.slotsgogo2026",
    "https://play.google.com/store/apps/details?id=com.tigeranddragon.doocosj2026",
    "https://play.google.com/store/apps/details?id=com.foxgamec.foxgames2026",
    "https://play.google.com/store/apps/details?id=com.magicgames.rabbit",
    "https://play.google.com/store/apps/details?id=com.rabbitstory.discovery2026",
    "https://play.google.com/store/apps/details?id=com.pandagame.pandamatch3",
    "https://play.google.com/store/apps/details?id=com.majiangganme.majiang",
    "https://play.google.com/store/apps/details?id=com.pandangame.majiangtooo003",
    "https://play.google.com/store/apps/details?id=com.pandamajiang.majiang004",
    "https://play.google.com/store/apps/details?id=com.pamdhh.majianggame005",
    "https://play.google.com/store/apps/details?id=com.pamdhh.majianggame006",
    "https://play.google.com/store/apps/details?id=com.nafay.drift",
    "https://play.google.com/store/apps/details?id=com.nafay.brain",
    "https://play.google.com/store/apps/details?id=com.tuhbas.ncnfu3",
    "https://play.google.com/store/apps/details?id=com.rljxmuxcjw.fpyxkfxf4",
    "https://play.google.com/store/apps/details?id=com.pandagame.rockpaper20481",
    "https://play.google.com/store/apps/details?id=com.pandagame.rockpaper20483",
    "https://play.google.com/store/apps/details?id=com.pandagame.rockpaper20484",
    "https://play.google.com/store/apps/details?id=com.pandagame.rockpaper20485",
    "https://play.google.com/store/apps/details?id=com.pksoccer23.pksoccer1",
    "https://play.google.com/store/apps/details?id=com.funnyjackfootball.app",
    "https://play.google.com/store/apps/details?id=club.aill365sportsoccer.app",
    "https://play.google.com/store/apps/details?id=com.aigoldshafootball.application",
    "https://play.google.com/store/apps/details?id=ai.royalhorsesports.core",
    "https://play.google.com/store/apps/details?id=com.saltmarvelspvtltd.ultimatetictactoe&pli=1",
    "https://play.google.com/store/apps/details?id=io.classicslots777.main",
     "https://play.google.com/store/apps/details?id=xyz.huatihuisports.src",
     "https://play.google.com/store/apps/details?id=ai.xingkongsports.main",
    "https://play.google.com/store/apps/details?id=club.aigamelove.main",
    "https://play.google.com/store/apps/details?id=com.genwears.sitescale",
    "https://play.google.com/store/apps/details?id=club.aiyinhesports.core",
    "https://play.google.com/store/apps/details?id=xyz.neon777spinslot.main",
    "https://play.google.com/store/apps/details?id=tm.jackpot777rushslot.main",
    "https://play.google.com/store/apps/details?id=com.anso.ancientslots",
    "https://play.google.com/store/apps/details?id=com.lssus.luckyslots",
    "https://play.google.com/store/apps/details?id=com.fortunerush.raviksolmaveth",
    
    
    
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

    # 遍历列表，自动生成1、2、3序号，不再显示gp编号
    for idx, link in enumerate(APP_LIST, 1):
        try:
            content = f"{idx}. {link}"
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
