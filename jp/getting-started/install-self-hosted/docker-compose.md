# Docker Compose 配備

### 前提条件

| オペレーティングシステム      | ソフトウェア                                                             | 説明                                                                                                                                                                                     |
| -------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| macOS 10.14以降            | Docker Desktop                                                 | Docker仮想マシン (VM) を少なくとも2つの仮想CPU (vCPU) と8 GBの初期メモリを使用するように設定してください。そうしないと、インストールが失敗する可能性があります。詳細については[MacにDocker Desktopをインストール](https://docs.docker.com/desktop/mac/install/)を参照してください。 |
| Linuxプラットフォーム       | <p>Docker 19.03以降<br>Docker Compose 1.25.1以降</p>          | 詳細については[Dockerのインストール](https://docs.docker.com/engine/install/)および[Docker Composeのインストール](https://docs.docker.com/compose/install/)を参照してください。 |
| WSL 2を有効にしたWindows | <p>Docker Desktop<br></p>                                      | ソースコードやその他のデータをLinuxコンテナにバインドする際には、それらをWindowsファイルシステムではなくLinuxファイルシステムに保存することをお勧めします。詳細については[WSL 2バックエンドを使用してWindowsにDocker Desktopをインストール](https://docs.docker.com/desktop/windows/install/#wsl-2-backend)を参照してください。 |

### Clone Dify

Difyのソースコードをローカルにクローン

```bash
git clone https://github.com/langgenius/dify.git
```

### Difyを開始

difyソースコードのdockerディレクトリに入り、一括起動コマンドを実行：

```Shell
cd dify/docker
docker compose up -d
```

> システムにDocker Compose V1ではなくV2がインストールされている場合は、`docker-compose`ではなく`docker compose`を使用してください。このことは`$ docker compose version`で確認できます。詳細については[こちら](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command)を参照してください。

デプロイメント結果：

```Shell
[+] Running 7/7
 ✔ Container docker-web-1       Started                                                                                                                                                                                       1.0s 
 ✔ Container docker-redis-1     Started                                                                                                                                                                                       1.1s 
 ✔ Container docker-weaviate-1  Started                                                                                                                                                                                       0.9s 
 ✔ Container docker-db-1        Started                                                                                                                                                                                       0.0s 
 ✔ Container docker-worker-1    Started                                                                                                                                                                                       0.7s 
 ✔ Container docker-api-1       Started                                                                                                                                                                                       0.8s 
 ✔ Container docker-nginx-1     Started
```

最後に、すべてのコンテナが正常に稼働しているか確認：

```bash
docker compose ps
```

3つのビジネスサービス `api / worker / web` と4つの基礎コンポーネント `weaviate / db / redis / nginx` が含まれます。

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

### Difyをアップグレード

difyソースコードのdockerディレクトリに入り、以下のコマンドを順に実行：

```bash
cd dify/docker
git pull origin main
docker compose down
docker compose pull
docker compose up -d
```
### Difyにアクセス

ブラウザで `http://localhost` を入力してDifyにアクセス。