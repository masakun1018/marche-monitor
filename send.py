import requests
from bs4 import BeautifulSoup
import os
import time

# ===== 設定 =====
TARGETS = {
    "miri": {
        "url": "https://marche-yell.com/miri_rakia/",
        "message": "MIRI在庫変わりました"
    },
    "rin": {
        "url": "https://marche-yell.com/kaine_rin/",
        "message": "凜在庫変わりました"
    }
}

WEBHOOK_URL = "https://hooks.slack.com/services/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"
# =================

def get_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if "販売中商品はありません" in soup.text:
        return 0
    else:
        return soup.text.count("購入可能")

while True:
    try:
        for name, data in TARGETS.items():

            url = data["url"]
            notify_message = data["message"]
            save_file = f"{name}_count.txt"

            count = get_count(url)

            if os.path.exists(save_file):
                with open(save_file, "r") as f:
                    old_count = int(f.read())
            else:
                old_count = None

            print(f"[{name}] 前回:", old_count)
            print(f"[{name}] 今回:", count)

            if old_count is not None and count != old_count:

                requests.post(
                    WEBHOOK_URL,
                    json={"text": f"{notify_message}\n前回:{old_count} → 今回:{count}\n{url}"}
                )

                print("Slack通知しました！")

            with open(save_file, "w") as f:
                f.write(str(count))

        time.sleep(180)  # ←180秒ごと（変更OK）

    except Exception as e:
        print("エラー:", e)
        time.sleep(180)