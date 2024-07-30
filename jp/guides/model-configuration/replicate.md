# Replicateのオープンソースモデルを統合

DifyはReplicate上の[言語モデル](https://replicate.com/collections/language-models)と[埋め込みモデル](https://replicate.com/collections/embedding-models)に接続することができます。言語モデルはDifyの推論モデルに対応し、埋め込みモデルはDifyの埋め込みモデルに対応します。

具体的な手順は以下の通りです：

1. Replicateのアカウントが必要です（[登録ページ](https://replicate.com/signin?next=/docs)）。
2. APIキーを取得します（[取得ページ](https://replicate.com/account/api-tokens)）。
3. モデルを選択します。[言語モデル](https://replicate.com/collections/language-models)と[埋め込みモデル](https://replicate.com/collections/embedding-models)からモデルを選びます。
4. Difyの`設定 > モデルプロバイダ > Replicate`にてモデルを追加します。

<figure><img src="../../../img/jp-replicate-model.png" alt=""><figcaption></figcaption></figure>

APIキーは第2ステップで設定したAPIキーです。モデル名とモデルバージョンはモデルの詳細ページで見つけることができます：

<figure><img src="../../.gitbook/assets/image (5) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>