# Docker Compose Deployment

## Prerequisites

| Operating System           | Software                                                       | Explanation                                                                                                                                                                                                                                                                                                                               |
| -------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| macOS 10.14 or later       | Docker Desktop                                                 | Set the Docker virtual machine (VM) to use a minimum of 2 virtual CPUs (vCPUs) and 8 GB of initial memory. Otherwise, the installation may fail. For more information, please refer to the [Docker Desktop installation guide for Mac](https://docs.docker.com/desktop/mac/install/).                                                     |
| Linux platforms            | <p>Docker 19.03 or later<br>Docker Compose 1.25.1 or later</p> | Docker と Docker Compose のインストール方法の詳細については、[Docker installation guide](https://docs.docker.com/engine/install/) と [the Docker Compose installation guide](https://docs.docker.com/compose/install/)を参照してください。                                    |
| Windows with WSL 2 enabled | Docker Desktop                                                 | Linux コンテナーにバインドされているソース コードとその他のデータは、Windows ファイル システムではなく Linux ファイル システムに保存することをお勧めします。 詳細については、[Docker Desktop installation guide for using the WSL 2 backend on Windows.](https://docs.docker.com/desktop/windows/install/#wsl-2-backend)を参照してください。  |

### Clone Dify

ローカルにcloneする:

```bash
git clone https://github.com/langgenius/dify.git
```

### Start Dify
Docker ディレクトリに移動し、Difyを起動します

```bash
cd dify/docker
docker compose up -d
```

> システムに Docker Compose V1 ではなく V2 がインストールされている場合, `docker-compose`ではなく`docker compose` を使ってください. `$ docker compose version`を実行してご確認ください. [Read more information here](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command).

デプロイ結果:

```bash
[+] Running 7/7
 ✔ Container docker-web-1       Started                                                                                                                                                                                       1.0s 
 ✔ Container docker-redis-1     Started                                                                                                                                                                                       1.1s 
 ✔ Container docker-weaviate-1  Started                                                                                                                                                                                       0.9s 
 ✔ Container docker-db-1        Started                                                                                                                                                                                       0.0s 
 ✔ Container docker-worker-1    Started                                                                                                                                                                                       0.7s 
 ✔ Container docker-api-1       Started                                                                                                                                                                                       0.8s 
 ✔ Container docker-nginx-1     Started
```

最後に、コンテナが稼働していることをチェックしてください:

```bash
docker compose ps
```

三つのサービス:` api / worker / web`, 四つの underlying components: `weaviate / db / redis / nginx`.

```bash
NAME                IMAGE                              COMMAND                  SERVICE             CREATED             STATUS              PORTS
docker-api-1        langgenius/dify-api:0.3.2          "/entrypoint.sh"         api                 4 seconds ago       Up 2 seconds        80/tcp, 5001/tcp
docker-db-1         postgres:15-alpine                 "docker-entrypoint.s…"   db                  4 seconds ago       Up 2 seconds        0.0.0.0:5432->5432/tcp
docker-nginx-1      nginx:latest                       "/docker-entrypoint.…"   nginx               4 seconds ago       Up 2 seconds        0.0.0.0:80->80/tcp
docker-redis-1      redis:6-alpine                     "docker-entrypoint.s…"   redis               4 seconds ago       Up 3 seconds        6379/tcp
docker-weaviate-1   semitechnologies/weaviate:1.18.4   "/bin/weaviate --hos…"   weaviate            4 seconds ago       Up 3 seconds        
docker-web-1        langgenius/dify-web:0.3.2          "/entrypoint.sh"         web                 4 seconds ago       Up 3 seconds        80/tcp, 3000/tcp
docker-worker-1     langgenius/dify-api:0.3.2          "/entrypoint.sh"         worker              4 seconds ago       Up 2 seconds        80/tcp, 5001/tcp
```

### Upgrade Dify

Docker ディレクトリに移動し、次のコマンドを実行してください:

```bash
cd dify/docker
git pull origin main
docker compose down
docker compose pull
docker compose up -d
```

### Access Dify

ブラウザにて [http://localhost/install](http://localhost/install) を開きましょう。
