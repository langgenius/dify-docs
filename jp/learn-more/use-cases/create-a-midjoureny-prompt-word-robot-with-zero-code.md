# コードなしでMidjourney プロンプトボットを作成する方法

_著者：歸藏の AI ツールボックス_

先日、私の週刊誌で紹介した自然言語プログラミングツール「Dify」を試してみました。これは @goocarlos が開発したもので、コードを書けない人でもプロンプトを作成するだけで Webアプリケーションを生成できるツールです。さらには API も自動生成され、希望するプラットフォームにデプロイすることができます。

以下のアプリケーションは、私が20分かけて作成したもので、非常に良い結果を得られました。Dify がなければ、これを完成させるのにもっと時間がかかったでしょう。具体的な機能としては、入力された短いテーマに基づいて Midjourney のプロンプトを生成するもので、よく使われる Midjourney コマンドも迅速に入力できるよう支援します。以下に、このアプリケーションの作成プロセスを紹介し、このプラットフォームに慣れていただけるようにします。

Dify には、ChatGPT のような対話型アプリケーションと、ボタンをクリックするだけでテキストを生成するテキスト生成型アプリケーションの2種類があります。今回は Midjourney 提示ワードロボットを作成するので、テキスト生成アプリケーションを選択します。

Dify はこちらでアクセスできます：https://dify.ai/

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/39e84c5e325bfbc4fea88f6b941a86cb.webp" alt=""><figcaption></figcaption></figure>

名前を入力して作成が完了すると、ダッシュボードページが表示され、データモニタリングやアプリケーション設定が行えます。まずは左側のプロンプトオーケストレーションをクリックします。ここが主な作業ページです。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/87afe74c0a9aa0f4f9fb88dbe510d055.webp" alt=""><figcaption></figcaption></figure>

このページの左側にはプロンプト設定とその他の機能があり、右側では作成した内容をリアルタイムでプレビューおよび使用できます。プレフィックスプロンプトは、ユーザーが毎回入力する内容に応じてトリガーされるプロンプトです。これは、GPT が毎回プレフィックスプロンプトの内容に基づいてユーザー入力を処理するということです。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/87b6579ecdf7866f006e3e2fea900e48.webp" alt=""><figcaption></figcaption></figure>

私のプレフィックスプロンプトの構造を見てみましょう。主に2つの部分から成り立っています。最初は、GPT に以下の英語の構造に従って写真の説明を出力するよう指示する部分です。英語の構造はプロンプトのテンプレートで、主に「テーマのカラフルな写真、複雑なパターン、鮮明なコントラスト、環境の説明、カメラモデル、入力内容に関連するレンズ焦点距離の説明、入力内容に関連する構図の説明、4人の写真家の名前」となります。これがプロンプトの主な内容です。理論的には、右側のプレビュー領域に保存して、生成したいテーマを入力すると、対応するプロンプトが生成されるはずです。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/6573752b0cb7eb8f53787b14c7b4f479.webp" alt=""><figcaption></figcaption></figure>

さて、後ろにある \{{proportion\}} と \{{version\}} は何でしょうか。右側を見ると、ユーザーが画像比率とモデルバージョンを選択する必要があります。これらの変数はユーザーの選択情報を伝達するためのものです。設定方法を見てみましょう。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/4f92181fb3f74924db3abbd09006ece6.webp" alt=""><figcaption></figcaption></figure>

私たちの機能は、ユーザーが選択した情報をプロンプトの最後に自動的に挿入し、ユーザーがコマンドを再入力する手間を省くことです。ここで変数機能を使用します。

変数の役割は、ユーザーがフォームに入力または選択した内容を動的にプロンプトに組み込むことです。例えば、ここでは画像比率を表す変数とモデルバージョンを表す変数を作成しました。追加ボタンをクリックして変数を作成します。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/a5d6c075658912892a0a3431e9646846.webp" alt=""><figcaption></figcaption></figure>

作成後、まず変数キーとフィールド名を入力する必要があります。変数キーは英語で入力します。オプションを有効にすると、このフィールドは選択必須ではなくなります。その後、操作バーの設定をクリックして変数内容を設定します。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/5aa9cf5f54a0e11bfdcb93c4453ca66f.webp" alt=""><figcaption></figcaption></figure>

変数には2種類あり、テキスト変数とドロップダウンオプションがあります。テキスト変数はユーザーが手動で入力するもので、ドロップダウンオプションは選択するものです。ここではユーザーにコマンドを手打ちさせたくないので、ドロップダウンオプションを選択します。必要なオプションを追加します。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/10533925c96d886ee52a5075d2e4f22f.webp" alt=""><figcaption></figcaption></figure>

次に変数を使用します。変数キーを二重の {} で囲んでプレフィックスプロンプトに入力します。ここでは、GPT にユーザーが選んだ内容をそのまま出力させたいので、「如実に変数内容を出力」というプロンプトを追加しました。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/6553e7e74d53832a1ca7f6761051da92.webp" alt=""><figcaption></figcaption></figure>

しかし、GPT が変数内容を変更してしまう可能性があります。その対策として、右側のモデル選択で多様性を低く設定します。これにより創造的な出力が減り、変数内容が変更されにくくなります。他のパラメータの意味は小さな感嘆符をクリックして確認できます。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/731639399f7df8b94ad6aa343329680a.webp" alt=""><figcaption></figcaption></figure>

これでアプリケーションが完成し、テスト出力に問題がなければ、右上の公開ボタンをクリックしてアプリケーションを公開します。公開アクセス URL からアプリケーションにアクセスできます。設定でアプリケーション名や概要、アイコンなどの内容を設定することもできます。

<figure><img src="https://assets-docs.dify.ai/img/jp/use-cases/24de168da16ef9452957b90905bf270e.webp" alt=""><figcaption></figcaption></figure>

これが Dify を使ってシンプルな AI アプリケーションを作成する手順です。また、生成された API を使って他のプラットフォームにアプリケーションをデプロイしたり、UI を変更したりすることもできます。Dify は独自のデータをアップロードすることもサポートしており、例えば製品に関する質問に答えるカスタマーサポートロボットを作成することもできます。以上でチュートリアルは終了です。@goocarlos に感謝します。
