# 接入 Hugging Face 上的开源模型

Dify 支持 Text-Generation 和 Embeddings，以下是与之对应的 Hugging Face 模型类型：

* Text-Generation：[text-generation](https://huggingface.co/models?pipeline\_tag=text-generation\&sort=trending)，[text2text-generation](https://huggingface.co/models?pipeline\_tag=text2text-generation\&sort=trending)
* Embeddings：[feature-extraction](https://huggingface.co/models?pipeline\_tag=feature-extraction\&sort=trending)

具体步骤如下：

1. 你需要有 Hugging Face 账号([注册地址](https://huggingface.co/join))。
2. 设置 Hugging Face 的 API key([获取地址](https://huggingface.co/settings/tokens))。
3. 进入 [Hugging Face 模型列表页](https://huggingface.co/models)，选择对应的模型类型。

<figure><img src="../../.gitbook/assets/image (14) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Dify 支持用两种方式接入 Hugging Face 上的模型：

1. Hosted Inference API。这种方式是用的 Hugging Face 官方部署的模型。不需要付费。但缺点是，只有少量模型支持这种方式。
2. Inference Endpoint。这种方式是用 Hugging Face 接入的 AWS 等资源来部署模型，需要付费。

### 接入 Hosted Inference API 的模型

#### 1 选择模型

模型详情页右侧有包含 Hosted inference API 的 区域才支持 Hosted inference API 。如下图所：

<figure><img src="../../.gitbook/assets/image (7) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

在模型详情页，可以获得模型的名称。

<figure><img src="../../.gitbook/assets/image (8) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

#### 2 在 Dify 中使用接入模型

在 `设置 > 模型供应商 > Hugging Face > 模型类型` 的 Endpoint Type 选择 Hosted Inference API。如下图所示：

<figure><img src="../../.gitbook/assets/image (103).png" alt=""><figcaption></figcaption></figure>

API Token 为文章开头设置的 API Key。模型名字为上一步获得的模型名字。

### 方式 2: Inference Endpoint

#### 1 选择要部署模型

模型详情页右侧的 `Deploy` 按钮下有 Inference Endpoints 选项的模型才支持 Inference Endpoint。如下图所示：

<figure><img src="../../.gitbook/assets/image (10) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

#### 2 部署模型

点击模型的部署按钮，选择 Inference Endpoint 选项。如果之前没绑过银行卡的，会需要绑卡。按流程走即可。绑过卡后，会出现下面的界面：按需求修改配置，点击左下角的 Create Endpoint 来创建 Inference Endpoint。

<figure><img src="../../.gitbook/assets/image (11) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

模型部署好后，就可以看到 Endpoint URL。

<figure><img src="../../.gitbook/assets/image (13) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

#### 3 在 Dify 中使用接入模型

在 `设置 > 模型供应商 > Hugging Face > 模型类型` 的 Endpoint Type 选择 Inference Endpoints。如下图所示：

<figure><img src="../../.gitbook/assets/image (105).png" alt=""><figcaption></figcaption></figure>

API Token 为文章开头设置的 API Key。`Text-Generation 模型名字随便起，Embeddings 模型名字需要跟 Hugging Face 的保持一致。`Endpoint URL 为 上一步部署模型成功后获得的 Endpoint URL。

<figure><img src="../../.gitbook/assets/image (97).png" alt=""><figcaption></figcaption></figure>

> 注意：Embeddings 的「用户名 / 组织名称」，需要根据你在 Hugging Face 的 [Inference Endpoints](https://huggingface.co/docs/inference-endpoints/guides/access) 部署方式，来填写「[用户名](https://huggingface.co/settings/account)」或者「[组织名称](https://ui.endpoints.huggingface.co/)」。
