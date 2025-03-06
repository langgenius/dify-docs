# テキスト生成型アプリケーション

テキスト生成型アプリケーションは、ユーザーが提供するプロンプトに基づいて高品質のテキストを自動生成するアプリケーションです。記事の要約や翻訳など、さまざまなタイプのテキストを生成することができます。

テキスト生成型アプリケーションは以下の機能をサポートしています：

1. 一回実行。
2. バッチ実行。
3. 実行結果の保存。
4. より類似した結果の生成。

以下にそれぞれの機能を紹介します。

### 一度実行

クエリ内容を入力し、実行ボタンをクリックすると、右側に結果が生成されます。以下の図のように：

<figure><img src="https://assets-docs.dify.ai/img/jp/launch-your-webapp-quickly/200353b18e7fddb7b7eedaf1d349021c.webp" alt=""><figcaption></figcaption></figure>

生成された結果部分では、「コピー」ボタンをクリックすると内容をクリップボードにコピーできます。「保存」ボタンをクリックすると内容を保存できます。「保存済み」タブで保存した内容を見ることができます。また、生成された内容には「いいね」や「バッド」をつけることもできます。

### バッチ実行

時には、アプリケーションを何度も実行する必要があります。例えば、テーマに基づいて記事を生成するWebアプリケーションがあるとします。今、100種類のテーマに基づいて記事を生成する必要があるとします。この場合、このタスクを100回も行うのは非常に面倒です。また、1つのタスクが完了するのを待たなければ次のタスクを開始できません。

上記のシナリオでは、バッチ実行機能を使うと操作が便利になり（テーマを `csv` ファイルに入力し、一度だけ実行する）、生成時間も節約できます（複数のタスクが同時に実行される）。使用方法は以下の通りです：

#### 第1歩 バッチ実行ページに入る

「バッチ実行」タブをクリックすると、バッチ実行ページに入ります。

<figure><img src="https://assets-docs.dify.ai/img/jp/launch-your-webapp-quickly/dc8166acc55edeeac96e8974ff662683.webp" alt=""><figcaption></figcaption></figure>

#### 第2歩 テンプレートをダウンロードして内容を入力する

「テンプレートダウンロード」ボタンをクリックし、テンプレートをダウンロードします。テンプレートを編集し、内容を入力して `.csv` 形式のファイルとして保存します。

<figure><img src="https://assets-docs.dify.ai/img/jp/launch-your-webapp-quickly/2dbbfc6fcef4e882d9bdec1de0047005.webp" alt=""><figcaption></figcaption></figure>

#### 第3歩 ファイルをアップロードして実行

<figure><img src="https://assets-docs.dify.ai/img/jp/launch-your-webapp-quickly/eda3652b5b9f2f7fda047f44cc551a23.webp" alt=""><figcaption></figcaption></figure>

生成された内容をエクスポートする必要がある場合は、右上の「ダウンロードボタン」をクリックして `csv` ファイルとしてエクスポートできます。

**注意:** アップロードする `csv` ファイルのエンコードは `ユニコード` でなければなりません。そうでないと、実行結果が失敗する可能性があります。解決策：ExcelやWPSなどで `csv` ファイルをエクスポートする際に、エンコードを `ユニコード` に選択します。

### 保存結果

生成結果の下にある「保存」ボタンをクリックすると、実行結果を保存できます。「保存済み」タブで、すべての保存された内容を見ることができます。

<figure><img src="https://assets-docs.dify.ai/img/jp/launch-your-webapp-quickly/c6ba431cb12c09288ff05c6b9d67d233.webp" alt=""><figcaption></figcaption></figure>

### より多くの類似結果の生成

アプリケーションのオーケストレーションで「より類似した」機能を有効にしている場合、Webアプリケーションで「より類似した」ボタンをクリックすると、現在の結果と似た内容を生成できます。以下の図の通りです：

<figure><img src="https://assets-docs.dify.ai/img/jp/launch-your-webapp-quickly/bbae9c215d972d72c7cff9fe389c4f7b.webp" alt=""><figcaption></figcaption></figure>