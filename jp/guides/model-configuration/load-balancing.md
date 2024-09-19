# 負荷分散

モデルのレート制限（Rate limits）とは、モデルプロバイダーがユーザーまたは顧客に対し、指定された時間内にAPIサービスへアクセスする回数に対して設ける制限のことです。これにより、APIの乱用や誤用を防ぎ、すべてのユーザーが公平にAPIにアクセスできるようにし、インフラ全体の負荷を管理することができます。

企業レベルで大規模にモデルAPIを呼び出す際、高い同時リクエストがレート制限を超えてしまい、ユーザーのアクセスに影響を及ぼすことがあります。負荷分散は、複数のAPIエンドポイント間でAPIリクエストを分配することで、すべてのユーザーが最速の応答と最高のモデル呼び出しスループットを得られるようにし、ビジネスの安定した運用を保障します。

**モデルプロバイダー -- モデルリスト -- 負荷分散の設定** でこの機能を有効にし、同じモデルに複数の資格情報（APIキー）を追加することができます。

<figure><img src="../../../img/jp-load_balancing_1.png" alt="" width="563"><figcaption><p>モデルを負荷分散する</p></figcaption></figure>

{% hint style="info" %}
モデル負荷分散は有料機能です。[SaaS有料サービスのサブスクリプション](../../getting-started/cloud.md#ding-yue-ji-hua)または企業版の購入を通じてこの機能を有効にすることができます。
{% endhint %}

デフォルト設定では、APIキーは初回設定時にモデルプロバイダーに追加された資格情報です。**設定の追加** をクリックして、同じモデルの異なるAPIキーを追加することで、負荷分散機能を正常に使用できます。

<figure><img src="../../img/jp-load_balancing_2.png" alt="" width="563"><figcaption><p>負荷分散の設定</p></figcaption></figure>

**少なくとも1つの追加モデル資格情報**を追加することで、保存し負荷分散を有効にできます。

既に設定されている資格情報を**一時的に無効化**または**削除**することも可能です。

<figure><img src="../../.gitbook/assets/image (7).png" alt="" width="563"><figcaption></figcaption></figure>

設定完了後、モデルリスト内にすべての有効な負荷分散モデルが表示されます。

<figure><img src="../../img/jp-load_balancing_3.png" alt="" width="563"><figcaption><p>負荷分散の有効化</p></figcaption></figure>

{% hint style="info" %}
デフォルトでは、負荷分散はラウンドロビン戦略を使用します。レート制限を超えた場合、1分間のクールダウンタイムが適用されます。
{% endhint %}

**モデルの追加**からも負荷分散を設定することができ、設定手順は上記と同じです。

<figure><img src="../../.gitbook/assets/image (4).png" alt="" width="563"><figcaption><p>モデルの追加から負荷分散を設定</p></figcaption></figure>