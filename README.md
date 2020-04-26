# python-dev_null

一定時間たてばSlackのメッセージを削除する。

このアプリケーションはSlackのOAuth Access Tokenが必要であり、[このリンク](https://api.slack.com/apps?new_app=1)の先で作ることができる。
発行するアカウントが管理者でなければ他人のメッセージを消すことができないため、OAuth Access Tokenを管理者が発行する必要がある。

必要なUser Token Scopesは
```
channels:history
channels:read
chat:write
```

の三つである。


.envにはTokenのほかに
一定時間でメッセージを消したいチャンネル名(#を抜いておく)
メッセージのクロールを走らせる間隔
メッセージの生存時間
を設定する必要がある

