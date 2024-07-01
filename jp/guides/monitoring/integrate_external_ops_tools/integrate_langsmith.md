# Langfuseの統合

### 1 LangSmithとは何か

LangSmith は、産業レベルのLLMアプリケーションを構築するためのプラットフォームで、開発、コラボレーション、テスト、展開、監視のためのLLMアプリケーションを作成するために使用されます。

{% hint style="info" %}
LangSmith 公式サイト紹介：[https://www.langchain.com/langsmith](https://www.langchain.com/langsmith)
{% endhint %}

***

### 2 LangSmithの設定方法

1. [公式サイト](https://www.langchain.com/langsmith)で登録し、LangSmithにログインします。
2. LangSmith内でプロジェクトを作成します。ログイン後、ホームページで **New Project** をクリックして、自分のプロジェクトを作成します。**プロジェクト**は、Dify内の**アプリケーション**と関連付けて、データ監視を行うために使われます。

<figure><img src="../../../.gitbook/assets/image (3).png" alt=""><figcaption><p>LangSmith内でプロジェクトを作成</p></figcaption></figure>

作成が完了すると、Projects内で作成されたすべてのプロジェクトが確認できます。

<figure><img src="../../../.gitbook/assets/image (7).png" alt=""><figcaption><p>LangSmith内で作成されたプロジェクトを確認</p></figcaption></figure>

3. プロジェクトクレデンシャルを作成します。左側のサイドバーで **Settings** を探します。

<figure><img src="../../../.gitbook/assets/image (8).png" alt=""><figcaption><p>プロジェクト設定</p></figcaption></figure>

**Create API Key** をクリックして、プロジェクトクレデンシャルを作成します。

<figure><img src="../../../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>プロジェクトAPI Keyの作成</p></figcaption></figure>

後でAPIの認証に使用される **Personal Access Token** を選択します。

<figure><img src="../../../.gitbook/assets/image (5).png" alt=""><figcaption><p>API Keyの作成</p></figcaption></figure>

作成されたAPIキーをコピーして保存します。

<figure><img src="../../../.gitbook/assets/image (9).png" alt=""><figcaption><p>API Keyのコピー</p></figcaption></figure>

4. Difyアプリケーション内でLangSmithを設定します。監視するアプリケーションを開きます。サイドバーのメニューから**モニタリング**を開きます。ページ内で**設定**を選びます。

<figure><img src="../../../.gitbook/assets/image (11).png" alt=""><figcaption><p>LangSmithの設定</p></figcaption></figure>

設定をクリックすると、LangSmith内で作成した**API Key**と**プロジェクト名**を設定内に貼り付け、保存します。

<figure><img src="../../../.gitbook/assets/image (12).png" alt=""><figcaption><p>LangSmithの設定</p></figcaption></figure>

{% hint style="info" %}
プロジェクト名の設定は、LangSmith内で設定したプロジェクトと一致する必要があります。プロジェクト名が一致しない場合、データ同期時にLangSmithは自動的に新しいプロジェクトを作成します。
{% endhint %}

正常に保存すると、現在のページで監視状態を確認できます。

<figure><img src="../../../.gitbook/assets/image (15).png" alt=""><figcaption><p>設定状態の確認</p></figcaption></figure>

### 3 LangSmith内で監視データを確認する

設定が完了すると、Dify内のアプリケーションのデバッグや生成データは、LangSmithで監視データを見ることができます。

<figure><img src="../../../.gitbook/assets/image (17).png" alt=""><figcaption><p>Dify内でアプリケーションのデバッグ</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (2).png" alt=""><figcaption><p>LangSmith内でアプリケーションデータを確認</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (18).png" alt=""><figcaption><p>LangSmith内でアプリケーションデータを確認</p></figcaption></figure>