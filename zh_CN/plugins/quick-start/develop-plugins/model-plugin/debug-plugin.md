# 调试插件

插件开发完成后，接下来需测试插件是否可以正常运行。Dify 提供远程调试方式，前往“插件管理”页获取调试 Key 和远程服务器地址。

<figure><img src="https://assets-docs.dify.ai/2024/11/1cf15bc59ea10eb67513c8bdca557111.png" alt=""><figcaption></figcaption></figure>

回到插件项目，拷贝 `.env.example` 文件并重命名为 `.env`，将获取的远程服务器地址和调试 Key 等信息填入其中。

`.env` 文件

```bash
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=remote-url
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=****-****-****-****-****
```

运行 `python -m main` 命令启动插件。在插件页即可看到该插件已被安装至 Workspace 内。其他团队成员也可以访问该插件。

<figure><img src="https://assets-docs.dify.ai/2024/12/ec26e5afc57bbfeb807719638f603807.png" alt=""><figcaption></figcaption></figure>
