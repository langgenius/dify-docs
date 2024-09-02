# SearchApi

> ツールの作者：@SearchApi。
SearchApiは、Google検索、Google Jobs、YouTube、Googleニュースなどの検索エンジンから構造化データを提供する強力なリアルタイムのSERP APIです。以下示されましたの手順フォローし、SearchApiツールを設定する。

## 1. SearchのAPIキーを申請する

[SearchApi](https://www.searchapi.io/)のウェブサイトでAPIキーを申請してください。

## 2. Dify内での設定

Difyのナビゲーションページから `ツール > SearchApi > 認証する`の順にクリックし、API キーを入力してください。

![](../../../../img/tool-searchapi.png)

## 3. ツールの使用方法

以下のアプリケーションタイプでSearchApiツールを使用できます。

- **チャットフロー / ワークフロー アプリ**

チャットフローとワークフローアプリでは、`SearchApi`のツールノードを追加することで、Google Jobs API、Google News API、Google Search API、YouTube Data APIの4つの異なるツールを使用可能にします。

![](../../../../img/tool-searchapi-flow.png)

- **エージェントアプリ**

エージェントアプリ内では、使用したい`SearchApi`ツールを選択し、続いてそのツールを呼び出すためのコマンドを入力してください。