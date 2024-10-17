# LangSmithの統合

### 1 LangSmithとは

LangSmithはLLMアプリケーションの開発、コラボレーション、テスト、デプロイ、監視などのツールを提供するプラットフォームです。

{% hint style="info" %}
LangSmithの公式サイト：[https://www.langchain.com/langsmith](https://www.langchain.com/langsmith)
{% endhint %}

***

### 2 LangSmithの使い方

1. LangSmithの[公式サイト](https://www.langchain.com/langsmith)から登録し、ログインする。
2. LangSmithからプロジェクトを作成します
ログイン後、ホームページの **New Project** をクリックし、新たな**プロジェクト**を作成します。このプロジェクトは、Dify内の**アプリ**と連動したデータモニタリングに使用されます。

<figure><img src="../../../.gitbook/assets/image (3).png" alt=""><figcaption><p>新たなプロジェクトを作成します。</p></figcaption></figure>

作成する後、プロジェクトの中にチェクできます。

<figure><img src="../../../.gitbook/assets/image (7).png" alt=""><figcaption><p>LangSmithの中にプロジェクトをチェクします。</p></figcaption></figure>

3. プロジェクト認証情報の作成
左のサイドバーでプロジェクト **設定** を見つける。

<figure><img src="../../../.gitbook/assets/image (8).png" alt=""><figcaption><p>プロジェクトを設定し</p></figcaption></figure>

**Create API Key**をクリックし，新たな認証情報を作ります。

<figure><img src="../../../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>プロジェクトのAPI Keyを作ります。</p></figcaption></figure>

**Personal Access Token** を選び，のちほとのAPI身分証明の時使えます。

<figure><img src="../../../.gitbook/assets/image (5).png" alt=""><figcaption><p>Personal Access Tokenを選択します</p></figcaption></figure>

新たなAPI keyをコピーし、保存します。

<figure><img src="../../../.gitbook/assets/image (9).png" alt=""><figcaption><p>新たなAPI keyをコピーします</p></figcaption></figure>

4. Dify アプリの中に LangSmith を設定します
監視用のアプリのサイトメニューの**監視**ボタンをクリックし，**設定**をクリックします。

<figure><img src="../../../.gitbook/assets/image (11).png" alt=""><figcaption><p>LangSmithを設定します</p></figcaption></figure>



それから，LangSmith から作った **API Key** と**プロジェクト名**を**設定**の中に貼り付け、保存します。

<figure><img src="../../../.gitbook/assets/image (12).png" alt=""><figcaption><p> LangSmithを設定します。</p></figcaption></figure>

{% hint style="info" %}
設定したプロジェクト名は LangSmith のいるプロジェクト名と必ず一致します。一致しない場合、データの同期時に LangSmith は自動的に新しいプロジェクトを作成します。
{% endhint %}

保存に成功すると、現在のページで監視状態を見ることができます。

<figure><img src="../../../.gitbook/assets/image (15).png" alt=""><figcaption><p>監視状態を見る</p></figcaption></figure>

### 3 LangSmith ページで監視データをチェックします

設定した後， Difyのアプリや生産データは LangSmith の中にチェクをできます。

<figure><img src="../../../.gitbook/assets/image (17).png" alt=""><figcaption><p>Dify内でのアプリの調整</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (2).png" alt=""><figcaption><p>LangSmithでアプリデータを見る</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (18).png" alt=""><figcaption><p>LangSmithでアプリデータを見る</p></figcaption></figure>
