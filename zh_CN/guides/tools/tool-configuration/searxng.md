# SearXNG
SearXNG 是一个免费的互联网元搜索引擎，整合了各种搜索服务的结果。用户不会被跟踪，也不会被分析。Dify 已经实现了访问 SearXNG 的接口，因此您可以直接在 Dify 中使用它。以下是将 SearXNG 集成到 Dify 的步骤：

## 1. 使用 Docker 安装 SearXNG 容器
```
docker run --rm \
             -d -p 8080:8080 \
             -v "${PWD}/searxng:/etc/searxng" \
             -e "BASE_URL=http://0.0.0.0:8080/" \
             -e "INSTANCE_NAME=searxng" \
             searxng/searxng
```
如果你想通过其他方式安装 SearXNG，请参考[这里](https://docs.searxng.org/admin/installation.html).

## 2. 修改 settings.yml
当您安装 SearXNG 时，默认的输出格式是 HTML 格式。您需要激活 JSON 格式。请将以下行添加到 settings.yml 文件中。如前面的示例所示，settings.yml 文件位于 ${PWD}/searxng/settings.yml
```
  # remove format to deny access, use lower case.
  # formats: [html, csv, json, rss]
  formats:
    - html
    - json    # <-- 添加这一行
```

## 3. 在 Dify 中集成 SearXNG
在 `工具 > SearXNG > 去认证` 中填写访问地址，例如：http://x.x.x.x:8080，


## 4. Finish
开启使用吧！

