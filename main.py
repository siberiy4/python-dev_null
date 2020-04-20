import os
from slack import WebClient
from slack.errors import SlackApiError
from datetime import datetime
import re

#環境変数からAPIトークンを受け取る
slack_token = os.environ['SLACK_API_TOKEN']
client = WebClient(token=slack_token)

#定期削除を実行したいchannel名を受け取る
target_channel_name = os.environ['DEV_NULL_CHANNEL']

#削除し始める経過時間
delete_time=int(os.environ['DEV_NULL_DELETE_SECONDS'])

try:
    #channel情報のリストを受け取る
    response = client.conversations_list(types="public_channel", exclude_archived="true",  limit=1000 )
    channel_list=response

    #定期削除を実行したいchannelの情報を探す
    target_channel={}
    for channel_info in channel_list["channels"]:
        if target_channel_name == channel_info["name"]:
            target_channel = channel_info
            break
        pass
    
    #対象のチャンネルのメッセージの取得
    response = client.conversations_history(channel=target_channel["id"])
    message_list=response

    #現在のtime stampを調べる
    current_ts = int(datetime.now().strftime('%s'))

    #指定時間以上経過したメッセージを削除する
    for message in (reversed(message_list["messages"])):
            if current_ts - int(re.sub(r'\.\d+$', '', message['ts'])) > delete_time:
                response = client.chat_delete(channel=target_channel["id"], ts=message["ts"])
            else:
                break
            pass

    print(response)

except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]  
    print(e)

