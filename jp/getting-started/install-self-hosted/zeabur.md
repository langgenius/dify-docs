# Zeabur に Dify をデプロイする

[Zeabur](https://zeabur.com) は、ワンクリックデプロイで Dify をデプロイできるサービスデプロイプラットフォームです。本ガイドは、Zeabur に Dify をデプロイする方法を説明します。

## 前提条件

開始する前に、以下の事項が必要です：

- Zeabur のアカウント。アカウントをお持ちでない場合は、[Zeabur](https://zeabur.com/) で無料のアカウントを登録できます。
- Zeabur のアカウントを開発者プラン（月額 5 ドル）にアップグレードする必要があります。詳細は [Zeabur 定价](https://zeabur.com/pricing) をご覧ください。

## Dify を Zeabur にデプロイする

Zeabur チームはワンクリックデプロイテンプレートを用意しています。以下のボタンをクリックするだけで開始できます：

[![Deploy to Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/1D4DOW)

ボタンをクリックすると、Zeabur 上のテンプレートページに移動し、デプロイの詳細情報と説明を確認できます。

<figure><img src="https://assets-docs.dify.ai/img/jp/install-self-hosted/4f2451c684f691815930b830d57e2446.webp" alt="Zeabur テンプレート概要"><figcaption></figcaption></figure>

デプロイボタンをクリックした後、生成されたドメイン名を入力し、そのドメイン名を Dify インスタンスにバインドし、他のサービスに環境変数として注入します。
次に、お好みのリージョンを選択し、デプロイボタンをクリックすると、数分以内に Dify インスタンスがデプロイされます。

<figure><img src="https://assets-docs.dify.ai/img/jp/install-self-hosted/b23726cca84bb2617f39809b4d123c54.webp" alt="リージョンを選択"><figcaption></figcaption></figure>

デプロイが完了すると、Zeabur コンソール上にプロジェクトページが表示されます。以下の図のように、デプロイ中に入力したドメイン名が自動的に NGINX サービスにバインドされ、そのドメイン名を使用して Dify インスタンスにアクセスできます。

<figure><img src="https://assets-docs.dify.ai/img/jp/install-self-hosted/b3c19c1bfe1ef9d955b8e57fb64d1119.webp" alt="Zeabur プロジェクト概要"><figcaption></figcaption></figure>

また、NGINX サービスページのネットワーキングタブでドメイン名を変更することもできます。詳細については [Zeabur ドキュメント](https://zeabur.com/docs/deploy/domain-binding) を参照してください。