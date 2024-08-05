# よくある質問

### 1. パスワードリセットメールが長時間届かない場合はどうしたらいいですか？

`.env`ファイルに`Mail`パラメータを設定する必要があることをご確認ください。メール設定に関する詳細は、「[環境変数の説明：メール関連の設定](https://docs.dify.ai/v/ja-jp/getting-started/install-self-hosted/environments#mru)」セクションをご参照ください。

設定の変更後は、以下のコマンドを実行して、サービスをリスタートさせてください。

```javascript
docker compose down
docker compose up -d
```

それでもまだメールが届かない場合は、メールサービスが正常に動作しているか、またメールがスパムフィルターに捕まっていないかをご確認ください。
