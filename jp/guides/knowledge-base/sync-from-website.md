# ウェブページからデータをインポート

Dify のナレッジベースでは、Firecrawl を利用してウェブページをスクレイピングし、解析したデータをMarkdownの形式でナレッジベースに取り込むことができます。

{% hint style="info" %}
[Firecrawl ](https://www.firecrawl.dev/)は、オープンソースのウェブページ解析ツールです。ウェブページをクリーンで大規模言語モデル（LLM）が扱いやすいMarkdown形式のテキストに変換します。また、使いやすいAPIサービスも提供しています。
{% endhint %}

### 設定方法

まず、DataSourceページでFirecrawlの認証情報を設定する必要があります。

<figure><img src="../../../en/.gitbook/assets/guides/knowledge-base/sync-from-website/image (6).png" alt=""><figcaption></figcaption></figure>

[Firecrawl 公式サイト](https://www.firecrawl.dev/) にログインして登録を完了し、APIキーを取得してから入力し、保存します。

<figure><img src="../../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

ナレッジベース作成のページで**Sync from website**を選択し、**スクレイピングの対象どしてのウェブページのURLを入力します**。

<figure><img src="../../../en/.gitbook/assets/guides/knowledge-base/sync-from-website/image (7).png" alt=""><figcaption><p>网页抓取配置</p></figcaption></figure>

設定項目には、サブページのスクレイピング、スクレイピングするページの上限、ページのスクレイピング深度、ページの除外、指定ページのみのスクレイピング、コンテンツの抽出などが含まれます。設定が完了したら **Run** をクリックし、解析結果のページをプレビューします。

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption><p>执行抓取</p></figcaption></figure>

解析されたテキストをナレッジベースのドキュメントにインポートし、結果を確認します。**Add URL** をクリックすると、新しいウェブページをさらにインポートできます。

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>解析されたウェブページのテキストをナレッジベースにインポート</p></figcaption></figure>
