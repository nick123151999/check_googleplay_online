import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

APP_LIST = [
    "com.todomaskj.toshhks2026",
    "com.gamesters.gridora",
    "com.tigerplinko.plinkogame",
]

STATE_FILE = "state.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="ignore").lower()


def check_app(app):
    try:
        url = f"https://play.google.com/store/apps/details?id={app}&hl=en"
        html = fetch(url)

        if "item not found" in html:
            return False
        if "we're sorry" in html:
            return False

        return True

    except:
        return True


def send(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("missing env")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": msg
    }).encode()

    urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=10)


def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}


def save_state(s):
    json.dump(s, open(STATE_FILE, "w"))


if __name__ == "__main__":

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    old = load_state()
    new = {}

    up = []
    down = []

    for app in APP_LIST:
        status = check_app(app)
        new[app] = status

        if app in old and old[app] != status:
            if status:
                up.append(app)
            else:
                down.append(app)

    save_state(new)

    if up or down:
        msg = f"📊 Play监控更新\n时间: {now}\n\n"

        if up:
            msg += "🟢 上架:\n" + "\n".join(up) + "\n\n"

        if down:
            msg += "🔴 下架:\n" + "\n".join(down)

        send(msg)

    print("done")
