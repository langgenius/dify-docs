# 创建应用

你可以通过 3 种方式在 Dify 的工作室内创建应用：

* 基于应用模板创建（新手推荐）
* 创建一个空白应用
* 通过 DSL 文件（本地/在线）创建应用

### 从模板创建应用

初次使用 Dify 时，你可能对于应用创建比较陌生。为了帮助新手用户快速了解在 Dify 上能够构建哪些类型的应用，Dify 团队内的提示词工程师已经创建好了多场景、高质量的应用模板。

你可以从导航选择 「工作室 」，在应用列表内选择 「从模版创建」。

<figure><img src="../../.gitbook/assets/image (168).png" alt=""><figcaption><p>从模板创建应用</p></figcaption></figure>

任意选择某个模板，并将其添加至工作区。

<figure><img src="../../.gitbook/assets/image (169).png" alt=""><figcaption><p>Dify 应用模板</p></figcaption></figure>

### 创建一个新应用

如果你需要在 Dify 上创建一个空白应用，你可以从导航选择 「工作室」 ，在应用列表内选择 「从空白创建 」。

<figure><img src="../../.gitbook/assets/image (167).png" alt=""><figcaption></figcaption></figure>

初次创建应用时，你可能需要先理解 Dify 上 4 种不同应用类型的[基本概念](./#application_type)，分别是聊天助手、文本生成应用、Agent 和工作流。

创建应用时，你需要给应用起一个名字、选择合适的图标，或者上传喜爱的图片用作图标、使用简介清晰的文字来描述此应用的用途，以方便后续应用在团队内的使用。

<figure><img src="../../.gitbook/assets/image (170).png" alt=""><figcaption><p>创建一个空白应用</p></figcaption></figure>

### 通过 DSL 文件创建应用

{% hint style="info" %}
Dify DSL 是由 Dify.AI 所定义的 AI 应用工程文件标准，文件格式为 YML。该标准涵盖应用在 Dify 内的基本描述、模型参数、编排配置等信息。
{% endhint %}

#### 本地导入

如果你从社区或其它人那里获得了一个应用模版（DSL 文件），可以从工作室选择 「 导入DSL 文件 」。DSL 文件导入后将直接加载原应用的所有配置信息。

<figure><img src="../../../img/import-dsl-file.png" alt=""><figcaption><p>导入 DSL 文件创建应用</p></figcaption></figure>

#### URL 导入

你也可以通过 URL 导入 DSL 文件，参考的链接格式：

```URL
https://example.com/your_dsl.yml
```

<figure><img src="../../../img/import-dsl-from-url.jpeg" alt=""><figcaption><p>通过 URL 导入 DSL 文件</p></figcaption></figure>
