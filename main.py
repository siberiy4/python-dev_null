import os
from slack import WebClient
from slack.errors import SlackApiError

#環境変数からAPIトークンを受け取る
slack_token = os.environ['SLACK_API_TOKEN']
client = WebClient(token=slack_token)

#定期削除を実行したいchannel名を受け取る
target_channel_name = os.environ['DEV_NULL_CHANNEL']

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

    print(response)

except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]  
    print(e)

