# コンテンツモデレーション

AIアプリケーションと対話する際、コンテンツの安全性、ユーザーエクスペリエンス、法律と規制など多方面で厳しい要件が求められます。このような場合、エンドユーザーにより良いインタラクティブ環境を提供するために「センシティブワード審査」機能が必要です。プロンプト編成ページで「機能を追加」をクリックし、下部のツールボックス「コンテンツのモデレーション」を見つけます：

<figure><img src="../../../.gitbook/assets/jp-moderation-tool-1.png" alt=""><figcaption><p>コンテンツ監査</p></figcaption></figure>

### 機能一：OpenAI モデレーション API の呼び出し

OpenAI やほとんどの大規模言語モデル (LLM) 会社が提供するモデルには、暴力、性、違法行為などの議論を含むコンテンツを出力しないようにするためのコンテンツ審査機能が備わっています。OpenAI はこのコンテンツ審査機能を公開しており、詳細は [platform.openai.com](https://platform.openai.com/docs/guides/moderation/overview) を参照してください。今では Dify でも直接 OpenAI モデレーション API を呼び出すことができます。入力内容や出力内容を監査するには、対応する「プリセット応答」を入力するだけです。

<figure><img src="../../../.gitbook/assets/jp-moderation-tool-2.png" alt=""><figcaption><p>OpenAI モデレーション API</p></figcaption></figure>

### 機能二：カスタムキーワード

開発者は監査が必要なセンシティブワードをカスタムキーワードとして設定できます。例えば「kill」をキーワードとして設定し、ユーザーが入力した際に監査動作を行い、プリセット応答内容として「The content is violating usage policies.」と設定します。予測される結果として、ユーザーが「kill」を含むテキストを入力すると、センシティブワード審査ツールが作動し、プリセット応答内容が返されます。

<figure><img src="../../../.gitbook/assets/jp-moderation-tool-3.png" alt=""><figcaption><p>キーワード</p></figcaption></figure>

### 機能三：センシティブワード審査 モデレーション拡張

企業内部では異なるセンシティブワード審査のメカニズムが存在することが多いです。企業が企業内ナレッジベースチャットボットなどのAIアプリケーションを開発する際、社員が入力したクエリ内容をセンシティブワード審査する必要があります。このため、開発者は自社のセンシティブワード審査メカニズムに基づいて API 拡張を作成することができます。詳細は [moderation.md](../../extension/api-based-extension/moderation.md "mention") を参照してください。これにより、Dify 上で呼び出し、高度なカスタマイズとプライバシー保護を実現することができます。

<figure><img src="../../../.gitbook/assets/jp-moderation-tool-4.png" alt=""><figcaption><p>モデレーション設定</p></figcaption></figure>

例えば、私たちのローカルサービスで、`ドナルド・ジョン・トランプ`というセンシティブワード審査ルールをカスタマイズします。ユーザーが`query`変数に「トランプ」と入力すると、対話時に "貴社のご使用ポリシーに反するコンテンツとなっております。" という応答が返されます。テスト結果は以下の通りです：

<figure><img src="../../../.gitbook/assets/jp-moderation-tool-5.png" alt=""><figcaption><p>モデレーションテスト</p></figcaption></figure>
