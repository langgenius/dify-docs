# 魔搭社区的模型服务

[魔搭](https://www.modelscope.cn/my/overview)是一个针对深度学习模型和技术的开源社区，魔搭提供了多种模型部署方式和Dify进行结合。

## 魔搭API服务

魔搭提供了[API服务](https://www.modelscope.cn/docs/model-service/API-Inference/intro)给不同需求的用户。该服务可以从页面配置，它是SaaS化的。

目前我们支持了Qwen系列模型的服务，并很快会扩展到其他重要模型上。查看上述列出的文档来关注我们的最新进度以及如何使用该服务。

另一个支持模型服务的方法是[SwingDeploy](https://www.modelscope.cn/my/modelService/deploy)。SwingDeploy是一个用户自行付费在阿里云上执行模型部署的方式，它的服务是独占式的。

上述两个方案都提供了标准OpenAI接口，因此很容易填入Dify的魔搭模型服务界面中，并提供便捷的模型后台支持。

## SWIFT

[SWIFT](https://github.com/modelscope/ms-swift)是魔搭社区开发的开源框架，主要能力是针对300+纯文本大模型和100+多模态大模型提供训练和推理部署能力。这些模型涵盖了用户需要的绝大多数模型，例如LLaMA/Qwen/Mistral/ChatGLM/DeepSeek众多系列模型，这些模型列表可以查看[这里](https://swift.readthedocs.io/zh-cn/latest/Instruction/%E6%94%AF%E6%8C%81%E7%9A%84%E6%A8%A1%E5%9E%8B%E5%92%8C%E6%95%B0%E6%8D%AE%E9%9B%86.html).

SWIFT针对大模型提供了众多便捷命令，例如针对训练的pt/sft/rlhf，以及针对推理的infer/deploy，在这里我们仅介绍和Dify进行结合的deploy能力来执行本地化部署。

执行下面的命令安装SWIFT：

```shell
pip install ms-swift[llm]
# if you are using mac:
# pip install "ms-swift[llm]"
```

接下来执行部署：

```shell
swift deploy --model Qwen/Qwen2.5-7B-Instruct --port 8000
```

部署能力仅通过上述一个命令就可以启动起来。

SWIFT支持多种推理加速框架，包含了pt（原生transformers），vLLM和LMDeploy。

你可以切换使用这些推理加速框架：

```shell
swift deploy --model Qwen/Qwen2.5-7B-Instruct --port 8000 --infer_backend pt/vllm/lmdeploy
```

推理文档可以参考[这里](https://swift.readthedocs.io/zh-cn/latest/Instruction/%E6%8E%A8%E7%90%86%E5%92%8C%E9%83%A8%E7%BD%B2.html#id4).

SWIFT提供了标准的OpenAI接口服务，方便集成在Kubernates或Docker等工程环境中。只需要填入模型名称`Qwen2.5-7B-Instruct`以及OpenAI url到Dify的魔搭模型服务界面中，即可在Dify中使用SWIFT的模型服务。
