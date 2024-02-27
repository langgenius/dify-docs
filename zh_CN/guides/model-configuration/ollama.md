# 接入 Ollama 部署的本地模型

![ollama](../../.gitbook/assets/ollama.png)

[Ollama](https://github.com/jmorganca/ollama) 是一个本地推理框架客户端，可一键部署如 Llama 2, Mistral, Llava 等大型语言模型。
Dify 支持接入 Ollama 部署的大型语言模型推理和 embedding 能力。

## 快速接入

### 下载并启动 Ollama

1. 下载 Ollama

   访问 [https://ollama.ai/download](https://ollama.ai/download)，下载对应系统 Ollama 客户端。

2. 运行 Ollama 并与 Llava 聊天

    ```bash
    ollama run llava
    ```

    启动成功后，ollama 在本地 11434 端口启动了一个 API 服务，可通过 `http://localhost:11434` 访问。

    其他模型可访问 [Ollama Models](https://ollama.ai/library) 了解详情。

3. 在 Dify 中接入 Ollama

   在 `设置 > 模型供应商 > Ollama` 中填入：

   ![](../../.gitbook/assets/ollama-config-zh.png)

   - 模型名称：`llava`
   
   - 基础 URL：`http://<your-ollama-endpoint-domain>:11434`
   
     此处需填写可访问到的 Ollama 服务地址。
   
     若 Dify 为 docker 部署，建议填写局域网 IP 地址，如：`http://192.168.1.100:11434` 或 docker 宿主机 IP 地址，如：`http://172.17.0.1:11434`。
   
     若为本地源码部署，可填写 `http://localhost:11434`。

   - 模型类型：`对话`

   - 模型上下文长度：`4096`
   
     模型的最大上下文长度，若不清楚可填写默认值 4096。
   
   - 最大 token 上限：`4096`
   
     模型返回内容的最大 token 数量，若模型无特别说明，则可与模型上下文长度保持一致。

   - 是否支持 Vision：`是`
   
     当模型支持图片理解（多模态）勾选此项，如 `llava`。

   点击 "保存" 校验无误后即可在应用中使用该模型。

   Embedding 模型接入方式与 LLM 类似，只需将模型类型改为 Text Embedding 即可。

4. 使用 Ollama 模型

   ![](../../.gitbook/assets/ollama-use-model.png)

   进入需要配置的 App 提示词编排页面，选择 Ollama 供应商下的 `llava` 模型，配置模型参数后即可使用。

如需获取 Ollama 更多信息，请参考：[https://github.com/jmorganca/ollama](https://github.com/jmorganca/ollama)

以下是上述内容的中文翻译：

### 在Linux上设置环境变量

如果Ollama作为systemd服务运行，应该使用`systemctl`设置环境变量：

1. 通过调用`systemctl edit ollama.service`编辑systemd服务。这将打开一个编辑器。

2. 对于每个环境变量，在`[Service]`部分下添加一行`Environment`：

    ```ini
    [Service]
    Environment="OLLAMA_HOST=0.0.0.0"
    ```

3. 保存并退出。

4. 重载`systemd`并重启Ollama：

   ```bash
   systemctl daemon-reload
   systemctl restart ollama
   ```

### 在Windows上设置环境变量

在Windows上，Ollama继承了您的用户和系统环境变量。

1. 首先通过任务栏点击Ollama退出程序

2. 从控制面板编辑系统环境变量

3. 为您的用户账户编辑或新建变量，比如`OLLAMA_HOST`、`OLLAMA_MODELS`等。

4. 点击OK/应用保存

5. 在一个新的终端窗口运行`ollama`


## 如何在我的网络上暴露Ollama？

Ollama默认绑定127.0.0.1端口11434。通过`OLLAMA_HOST`环境变量更改绑定地址。