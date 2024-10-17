---
description: プレミアムPremium
---

# Dify Premium

Dify Premiumは[AWS AMI](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/ec2-instances-and-amis.html)製品であります。これにより、ブランドのカスタマイズが可能で、AWS EC2にワンクリックで展開できます。[AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-t22mebxzwjhu6)から購読し、次のようなシナリオに最適です：

* 中小企業が1つ以上のアプリケーションをサーバーに構築し、データのプライバシーに関心がある場合。
* [Dify Cloud](https://docs.dify.ai/v/ja-jp/getting-started/cloud)のサブスクリプションプランに関心があり、しかし、ユースケースが[プラン](https://dify.ai/pricing)で提供されるリソースを超える場合。
* Dify Enterpriseを組織内で導入する前に、POC検証を行いたい場合。

### セットアップ

Difyを初めて使用する際には、管理者初期化パスワード（EC2インスタンスIDとして設定）を入力し、セットアッププロセスを開始してください。

AMIを展開した後は、EC2コンソールで見つかるインスタンスのパブリックIPを使用してDifyにアクセスします（デフォルトではHTTPポート80を使用します）。

### アップグレード

EC2インスタンスで、次のコマンドを実行してください：

```
git clone https://github.com/langgenius/dify.git /tmp/dify
mv -f /tmp/dify/docker/* /dify/
rm -rf /tmp/dify
docker-compose down
docker-compose pull
docker-compose -f docker-compose.yaml -f docker-compose.override.yaml up -d
```

### カスタマイズ

セルフホスト展開の場合と同様に、EC2インスタンス内の.envファイルの環境変数を必要に応じて変更することができます。その後、以下のコマンドを使用してDifyを再起動してください：

```
docker-compose down
ocker-compose -f docker-compose.yaml -f docker-compose.override.yaml up -d
```
