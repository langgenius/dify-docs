---
title: " Ollama＋Dify による gpt-oss のローカルデプロイ"
---

## はじめに

gpt-ossシリーズは、2025年8月にOpenAIからリリースされたオープンソースモデルです。
- gpt-oss:20b（約16GBのメモリを持つシステム向け）
- gpt-oss:120b（60GB以上のメモリに対応）

ローカルでOllamaを使用して実行できます。クラウド呼び出しは不要で、データは常にローカルに保存され、プライバシー保護と低遅延に貢献します。

DifyはAIエージェントやワークフローを構築するためのオープンソースプラットフォームです。このガイドでは、Ollamaを使ってgpt-ossを実行し、Difyに接続してプライベートかつ高性能な設定を行う方法を示します。

## 環境のセットアップ

### ステップ1：Ollamaでgpt-ossを実行する

**1. Ollamaをインストール**

[Ollamaの公式サイト](https://ollama.com/)を通してmacOS、Windows、またはLinux用にダウンロードしてインストールしてください。

**2. gpt-ossモデルをインストール**

```Bash
# 開発マシン用におすすめ
ollama pull gpt-oss:20b

# 大規模GPUまたはマルチGPUホスト用におすすめ
ollama pull gpt-oss:120b
```

これらのモデルはすでに混合精度フォーマット（MXFP4）で量子化されており、ローカルデプロイに適しています。

**3. Ollamaの起動**

デフォルトのエンドポイントはhttp://localhost:11434です。

### ステップ2：Difyをローカルにインストール

Difyの[公式ドキュメント](https://docs.dify.ai/ja-jp/getting-started/install-self-hosted/readme)に完全な手順があります。もしくはこちらのシンプルなチュートリアルをご覧ください。

**前提条件**
[Docker](https://www.docker.com/products/docker-desktop/)をインストールし、Dockerエンジンが正常に動作していることを確認してください。

![1](https://raw.githubusercontent.com/NanSike/image-host/main/images/1.png)

**インストール手順**

```Bash
git clone https://github.com/langgenius/Dify.git
cd Dify/docker
cp .env.example .env
docker compose up -d
```

![2](https://raw.githubusercontent.com/NanSike/image-host/main/images/2.png)

ローカルDifyインスタンスを開き、初期設定を完了させてください。

![3](https://raw.githubusercontent.com/NanSike/image-host/main/images/3.png)

## モデルの追加とチャットのテスト

1. **設定 > モデルプロバイダー > Ollama** に移動し、**「Ollamaモデルタイプを追加」**をクリックしてください。

![4](https://raw.githubusercontent.com/NanSike/image-host/main/images/4.png)

2. 基本URLを`http://localhost:11434`に設定し、モデル名に`gpt-oss`を選択し、必要なフィールドを埋めてください。

![5](https://raw.githubusercontent.com/NanSike/image-host/main/images/5.png)

3. 空のテンプレートを作成します。

![6](https://raw.githubusercontent.com/NanSike/image-host/main/images/6.png)

4. 構築したいアプリのタイプを選択してください。

![7](https://raw.githubusercontent.com/NanSike/image-host/main/images/7.png)

## 検証と使用

- Difyの**モデルテスト**ページでプロンプトを送信し、応答が期待通りであることを確認してください。
- ワークフローに**LLMノード**を追加し、`gpt-oss:20b`を選択してノードをエンドツーエンドで接続してください。

![8](https://raw.githubusercontent.com/NanSike/image-host/main/images/8.png)

![9](https://raw.githubusercontent.com/NanSike/image-host/main/images/9.png)

## よくある質問

1. モデルのダウンロードが遅い
   ダウンロードを高速化するために、Dockerプロキシを設定するか、イメージミラーを使用してください。

2. GPUメモリ不足
   `gpt-oss:20b`を使用してください。CPUオフローディングを有効にすることもできますが、その場合は応答が遅くなります。

3. ポートアクセスの問題
   接続を確認するために、ファイアウォールのルール、ポートのバインディング、およびDockerネットワーク設定を確認してください。