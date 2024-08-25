# LangFuseの統合

### 1 Langfuseとは

LangfuseはLLMアプリケーションの開発者がデバッグ、分析、反復等を使用してアプリケーションのパフォーマンスを向上させるためのツールです。

{% hint style="info" %}
Langfuseの公式サイト：[https://langfuse.com/](https://langfuse.com/)
{% endhint %}

***

### 2 Langfuseの使い方

1. Langfuseの[公式サイト](https://langfuse.com/)から登録し、ログインする。
2. Langfuseからプロジェクトを作成します
ログイン後、ホームページの **New** をクリックし、新たな**プロジェクト**を作成します。このプロジェクトは、Dify内の**アプリ**と連動したデータモニタリングに使用されます。

<figure><img src="../../../.gitbook/assets/image (249).png" alt=""><figcaption><p>新たなプロジェクトを作成します。</p></figcaption></figure>

プロジェクトの名前を付けます。

<figure><img src="../../../.gitbook/assets/image (251).png" alt=""><figcaption><p>プロジェクトの名前を付けます。</p></figcaption></figure>

3. プロジェクト認証情報の作成
左のサイドバーでプロジェクト **設定** を見つける。

<figure><img src="../../../.gitbook/assets/image (253).png" alt=""><figcaption><p>左のサイドバーをクリックします</p></figcaption></figure>

**Create API Key**をクリックし，新たな認証情報を作ります。

<figure><img src="../../../.gitbook/assets/image (252).png" alt=""><figcaption><p>プロジェクトのAPI Keyを作ります。</p></figcaption></figure>

**Secret Key** と **Public Key，Host** をコピーし、保存します。

<figure><img src="../../../.gitbook/assets/image (254).png" alt=""><figcaption><p>APIキーの設定を取得する</p></figcaption></figure>

4\. Dify アプリの中に Langfuse を設定します
監視用のアプリのサイトメニューの**監視**ボタンをクリックし，**設定**をクリックします。

<figure><img src="../../../.gitbook/assets/image (255).png" alt=""><figcaption><p>Langfuseを設定します</p></figcaption></figure>

それから，Langfuse から作った **Secret Key, Public Key** と **Host** を**設定**の中に貼り付け、保存します。

<figure><img src="../../../.gitbook/assets/image (256).png" alt=""><figcaption><p>Langfuseを設定します</p></figcaption></figure>

保存に成功すると、現在のページで監視状態を見ることができます。

<figure><img src="../../../.gitbook/assets/image (257).png" alt=""><figcaption><p>監視状態を見る</p></figcaption></figure>

***

### 3 Langfuse ページで監視データをチェックします

設定した後， Difyのアプリや生産データは Langfuse の中にチェクをできます。

<figure><img src="../../../.gitbook/assets/image (259).png" alt=""><figcaption><p>Dify 内でのアプリの調整</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (258).png" alt=""><figcaption><p>Langfuse でアプリデータを見る</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image.png" alt=""><figcaption><p>Langfuse でアプリデータを見る</p></figcaption></figure>
