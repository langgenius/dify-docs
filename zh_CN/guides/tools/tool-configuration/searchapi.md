# SearchApi

> 工具作者 @SearchApi。

{% hint style="warning" %}
“工具”已全面升级为“插件”生态，详细的使用说明请参考[插件开发](https://docs.dify.ai/zh-hans/plugins/quick-start/install-plugins)。以下内容已归档。
{% endhint %}

SearchApi 是一个强大的实时 SERP API，可提供来自 Google 搜索、Google 招聘、YouTube、Google 新闻等搜索引擎集合的结构化数据。以下是在 Dify 中配置和使用 SearchApi 搜索工具的步骤。

## 1. 申请 Search API Key

请在 [SearchApi](https://www.searchapi.io/)申请 API Key。

## 2. 在 Dify 内填写配置

在 Dify 导航页内轻点 `工具 > SearchApi > 去授权` 填写 API Key。

![](../../../.gitbook/assets/zh-tool-searchapi.png)

## 3. 使用工具

你可以在以下应用类型中使用 SearchApi 工具。

* **Chatflow / Workflow 应用**

Chatflow 和 Workflow 应用均支持添加 `SearchApi` 系列工具节点，提供 Google Jobs API，Google News API，Google Search API，YouTube 脚本 API 四种工具。

![](../../../.gitbook/assets/zh-tool-searchapi-flow.png)

* **Agent 应用**

在 Agent 应用内选择需要添加的 `SearchApi` 工具，然后输入指令调用工具。
