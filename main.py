import os
from slack import WebClient
from slack.errors import SlackApiError
from datetime import datetime
import re
import time
import threading

# Slack APIで指定のチャンネルのメッセージを読み、指定時間以上経過したメッセージを削除する
def worker():
    try:
        # 対象のチャンネルのメッセージの取得
        response = client.conversations_history(channel=target_channel["id"])
        message_list = response

        # 現在のtime stampを調べる
        current_ts = int(datetime.now().strftime('%s'))

        # 指定時間以上経過したメッセージを削除する
        for message in (reversed(message_list["messages"])):
            if current_ts - int(re.sub(r'\.\d+$', '', message['ts'])) > delete_time:
                response = client.chat_delete(
                    channel=target_channel["id"], ts=message["ts"])
            else:
                break
            pass
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(e)

# 指定した感覚で指定の関数を実行する
def scheduler(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)


# 環境変数からAPIトークンを環境変数から受け取る
slack_token = os.environ['SLACK_API_TOKEN']
client = WebClient(token=slack_token)

# 定期削除を実行したいchannel名を環境変数から受け取る
target_channel_name = os.environ['DEV_NULL_CHANNEL']

# 削除し始める経過時間を環境変数から受け取る
delete_time = int(os.environ['DEV_NULL_DELETE_SECONDS'])

# メッセージをクロールする感覚を環境変数から受け取る

try:
    # channel情報のリストを受け取る
    response = client.conversations_list(
        types="public_channel", exclude_archived="true",  limit=1000)
    channel_list = response

    # 定期削除を実行したいchannelの情報を探す
    target_channel = {}
    for channel_info in channel_list["channels"]:
        if target_channel_name == channel_info["name"]:
            target_channel = channel_info
            break
        pass
    
    scheduler(60, worker, False)


except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(e)


