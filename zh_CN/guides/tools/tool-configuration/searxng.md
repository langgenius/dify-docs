# SearXNG
SearXNG 是一个免费的互联网元搜索引擎，整合了各种搜索服务的结果。用户不会被跟踪，也不会被分析。Dify 已经实现了访问 SearXNG 的接口，因此您可以直接在 Dify 中使用它。下面介绍使用 docker 将 SearXNG 集成到 Dify 的步骤，如果您想通过其他方式安装 SearXNG，请参考[这里](https://docs.searxng.org/admin/installation.html)。

## 1. 按需修改配置，也可使用默认配置。  
配置文件位于 `dify/api/core/tools/provider/builtin/searxng/docker/settings.yml`， 配置文档可参考[这里](https://docs.searxng.org/admin/settings/index.html)。

## 2. 在 dify 根目录下启动 Docker 容器
```
cd dify
docker run --rm -d -p 8081:8080 -v "${PWD}/api/core/tools/provider/builtin/searxng/docker:/etc/searxng" searxng/searxng
```

## 3. 在 Dify 中集成 SearXNG  
在 `工具 > SearXNG > 去认证` 中填写访问地址，如果您使用的 docker 部署的 Dify，这个地址一般是 `http://host.docker.internal:8081`。
