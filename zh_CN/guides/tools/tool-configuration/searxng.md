# SearXNG

> 工具作者 @Junytang。

SearXNG 是一个免费的互联网元搜索引擎，整合了各种搜索服务的检索结果。用户不会被跟踪，搜索行为也不会被分析。现在你可以直接在 Dify 中使用此工具。

下文将介绍如何在[社区版](https://docs.dify.ai/v/zh-hans/getting-started/install-self-hosted/docker-compose)使用 Docker 将 SearXNG 集成到 Dify。

> 如果你想在 Dify 云服务内使用 SearXNG，请参考[ SearXNG 安装文档](https://docs.searxng.org/admin/installation.html)自建服务，然后回到 Dify，在 "工具 > SearXNG > 去认证" 页填写服务的 Base URL。

## 1. 修改 Dify 配置文件

SearXNG 的配置文件位于 `dify/api/core/tools/provider/builtin/searxng/docker/settings.yml`， 配置文档可参考[这里](https://docs.searxng.org/admin/settings/index.html)。

你可以按需修改配置，也可直接使用默认配置。

## 2. 启动服务

在 Dify 根目录下启动 Docker 容器。

```bash
cd dify
docker run --rm -d -p 8081:8080 -v "${PWD}/api/core/tools/provider/builtin/searxng/docker:/etc/searxng" searxng/searxng
```

## 3. 使用 SearXNG

在 `工具 > SearXNG > 去认证` 中填写访问地址，建立 Dify 服务与 SearXNG 服务的连接。SearXNG 的 Docker 内网地址一般是 `http://host.docker.internal:8081`。


---

# 在 Linux VM 上托管 SearXNG 作为私有实例

本节将指导你如何在 **Linux VM** 上托管 SearXNG 并确保它可以与 Dify 集成。

### 1. 准备 Linux VM 环境

确保你的 Linux VM 环境具备以下条件：

- **安装了 Docker 和 Docker Compose**。
- 你可以使用任何支持的 Linux 发行版（如 Ubuntu 24.04 或其他基于 Debian 的系统）。

#### 1.1 安装 Docker

运行以下命令来安装 Docker：

```bash
# 更新包列表
sudo apt update

# 安装必要的包
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# 添加 Docker GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加 Docker 官方仓库
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

验证 Docker 是否安装成功：

```bash
docker --version
```

#### 1.2 安装 Docker Compose

运行以下命令来安装 Docker Compose：

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/2.32.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

验证 Docker Compose 是否安装成功：

```bash
docker-compose --version
```

### 2. 设置 SearXNG Docker 容器

#### 2.1 克隆 SearXNG Docker 仓库

首先，克隆 SearXNG Docker 仓库到你的 Linux VM 中：

```bash
git clone https://github.com/searxng/searxng-docker.git
cd searxng-docker
```

#### 2.2 修改 Docker 配置文件

1. **修改 `docker-compose.yaml` 文件**，确保 SearXNG 服务绑定到端口 `8081`，并且配置 Redis 服务。修改后的 `docker-compose.yaml` 文件如下所示：

```yaml
version: '3'

services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8081:8080"  # 将容器的 8080 端口映射到宿主机的 8081 端口
    volumes:
      - ./searxng:/etc/searxng  # 配置 SearXNG 配置文件的挂载
    networks:
      - searxng_network

  redis:
    image: valkey/valkey:8-alpine
    ports:
      - "6379:6379"  # Redis 服务映射端口
    networks:
      - searxng_network

  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    networks:
      - searxng_network

networks:
  searxng_network:
    driver: bridge
```

2. **修改 `settings.yml` 配置文件**，确保 SearXNG 监听所有 IP 地址并启用 JSON 格式的输出：

```yaml
server:
  bind_address: "0.0.0.0"  # 允许外部访问
  port: 8080

search:
  formats:
    - html
    - json
    - csv
    - rss
```

#### 2.3 启动 Docker 容器

修改完配置文件后，使用以下命令启动 Docker 容器：

```bash
docker-compose up -d
```

### 3. 使 SearXNG 服务可访问

默认情况下，Docker 容器将绑定到 `localhost` 或 `127.0.0.1`。如果你希望外部设备（如 Dify）能访问 SearXNG，你需要确保你的 Linux VM 可以通过公共 IP 地址访问端口 `8081`。

你可以查看你的 VM 的公共 IP 地址：

```bash
ip addr show
```

确保你的防火墙已开放 `8081` 端口。

---

# 4. 将 SearXNG 与 Dify 集成

一旦你的 SearXNG 实例在 Linux VM 上运行，你可以将其与 Dify 进行连接。

### 4.1 配置 Dify

1. 在 Dify 平台的 **工具 > SearXNG > 去认证** 页面中，输入你的自建 SearXNG 服务的 **Base URL**，格式为：

```text
http://<your-linux-vm-ip>:8081
```

2. 保存配置后，Dify 将能够连接到你的 SearXNG 实例。

---

## 5. 测试 SearXNG 集成

你可以通过 `curl` 命令测试 SearXNG 服务是否正常工作：

```bash
curl "http://<your-linux-vm-ip>:8081/search?q=apple&format=json&categories=general"
```

如果一切正常，你应该收到包含 "apple" 搜索结果的 JSON 响应。
