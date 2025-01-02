# モダ（ModelScope）コミュニティのモデルサービス

[モダ（ModelScope）](https://www.modelscope.cn/my/overview)は、深層学習モデルと技術に特化したオープンソースコミュニティです。モダは、さまざまなモデル展開方法とDifyとの連携を提供しています。

## モダAPIサービス

モダは、さまざまなニーズを持つユーザー向けに[APIサービス](https://www.modelscope.cn/docs/model-service/API-Inference/intro)を提供しています。このサービスは、ページ上で設定可能であり、SaaS形式で提供されています。

現在、Qwenシリーズモデルのサービスをサポートしており、今後は他の主要なモデルにも対応を拡大する予定です。最新の進捗やサービスの利用方法については、上記のドキュメントをご覧ください。

モデルサービスを利用するもう一つの方法は、[SwingDeploy](https://www.modelscope.cn/my/modelService/deploy)です。SwingDeployは、ユーザーが自己負担でAlibaba Cloud上にモデルを展開する専用サービスです。

これらの2つのソリューションはどちらも標準的なOpenAIインターフェースを提供しており、Difyのモダモデルサービス画面に簡単に統合できるため、便利なモデルバックエンドサポートを提供します。

## SWIFT

[SWIFT](https://github.com/modelscope/ms-swift)は、モダコミュニティが開発したオープンソースフレームワークであり、300以上のテキスト生成モデルおよび100以上のマルチモーダルモデルに対して、トレーニングや推論・展開の能力を提供します。これらのモデルは、LLaMA/Qwen/Mistral/ChatGLM/DeepSeekなど、多くのシリーズモデルを含み、利用者のニーズに応じた大部分のモデルを網羅しています。モデルのリストについては[こちら](https://swift.readthedocs.io/zh-cn/latest/Instruction/%E6%94%AF%E6%8C%81%E7%9A%84%E6%A8%A1%E5%9E%8B%E5%92%8C%E6%95%B0%E6%8D%AE%E9%9B%86.html)をご覧ください。

SWIFTでは、大規模モデル向けに便利なコマンドを数多く提供しています。例えば、トレーニング用の`pt/sft/rlhf`や、推論用の`infer/deploy`などです。ここでは、Difyと連携するための`deploy`機能を利用したローカル展開について説明します。

以下のコマンドを実行してSWIFTをインストールします：

```shell
pip install ms-swift[llm]
# macを使用している場合：
# pip install "ms-swift[llm]"
```

続いて、展開を実行します：

```shell
swift deploy --model Qwen/Qwen2.5-7B-Instruct --port 8000
```

展開機能は、上記の1つのコマンドで簡単に起動できます。

SWIFTは、複数の推論加速フレームワークをサポートしており、`pt`（ネイティブtransformers）、`vLLM`、`LMDeploy`が含まれます。

これらの推論加速フレームワークを切り替えることも可能です：

```shell
swift deploy --model Qwen/Qwen2.5-7B-Instruct --port 8000 --infer_backend pt/vllm/lmdeploy
```

推論に関する詳細なドキュメントは[こちら](https://swift.readthedocs.io/zh-cn/latest/Instruction/%E6%8E%A8%E7%90%86%E5%92%8C%E9%83%A8%E7%BD%B2.html#id4)をご覧ください。

SWIFTは、標準的なOpenAIインターフェースを提供しており、KubernetesやDockerなどのエンジニアリング環境への統合が容易です。Difyのモダモデルサービス画面にモデル名`Qwen2.5-7B-Instruct`とOpenAI URLを入力するだけで、Dify内でSWIFTのモデルサービスを利用できます。
