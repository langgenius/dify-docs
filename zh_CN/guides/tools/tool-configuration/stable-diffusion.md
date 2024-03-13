# Stable Diffusion
StableDiffusion 是一种基于文本提示生成图像的工具，Dify 已经实现了访问 Stable Diffusion WebUI API 的接口，因此你可以直接在 Dify 中使用它。以下是在 Dify 中集成 Stable Diffusion 的步骤。

## 1. 确保你有一台带 GPU 的机器
Stable Diffusion 最好使用一台有较强 GPU 的机器来生成图像。但这并不是必须的，你也可以只使用 CPU 来生成图像，但速度可能会很慢。

## 2. 启动 Stable Diffusion WebUI
在本地机器或服务器上启动 Stable Diffusion WebUI。

### 2.1. 克隆 Stable Diffusion WebUI 仓库
从[官方仓库](https://github.com/AUTOMATIC1111/stable-diffusion-webui)克隆 Stable Diffusion WebUI 仓库
    
```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
```

### 2.2. 本地启动
克隆仓库后，你应该切换到克隆的仓库目录，并运行以下命令来启动 Stable Diffusion WebUI。

#### Windows
```bash
cd stable-diffusion-webui
./webui.bat --api --listen
```

#### Linux
```bash
cd stable-diffusion-webui
./webui.sh --api --listen
```

### 2.3. 准备模型
现在你可以根据终端中显示的地址在浏览器中访问 Stable Diffusion WebUI，但模型还不可用。你需要从 HuggingFace 或其他来源下载模型，并将其放在 Stable Diffusion WebUI 的 `models` 目录中。

例如，我们使用 [pastel-mix](https://huggingface.co/JamesFlare/pastel-mix) 作为模型，使用 `git lfs` 下载模型并将其放在 `stable-diffusion-webui` 的 `models` 目录中。

```bash
git clone https://huggingface.co/JamesFlare/pastel-mix
```

### 2.4 获取模型名称
现在你可以在模型列表中看到 `pastel-mix`，但我们仍然需要获取模型名称，访问 `http://your_id:port/sdapi/v1/sd-models`，你将看到如下的模型名称。

```json
[
    {
        "title": "pastel-mix/pastelmix-better-vae-fp32.ckpt [943a810f75]",
        "model_name": "pastel-mix_pastelmix-better-vae-fp32",
        "hash": "943a810f75",
        "sha256": "943a810f7538b32f9d81dc5adea3792c07219964c8a8734565931fcec90d762d",
        "filename": "/home/takatost/stable-diffusion-webui/models/Stable-diffusion/pastel-mix/pastelmix-better-vae-fp32.ckpt",
        "config": null
    },
]
```

`model_name` 就是我们需要的，这个例子中是 `pastel-mix_pastelmix-better-vae-fp32`。

## 3. 在 Dify 中集成 Stable Diffusion
在 `工具 > StableDiffusion > 去认证` 中填写认证和模型配置，使用你从之前步骤中获取的信息。

## 4. 完成

尝试在Dify中使用它吧！
