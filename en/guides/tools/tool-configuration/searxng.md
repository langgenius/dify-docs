# SearXNG
SearXNG is a free internet metasearch engine which aggregates results from various search services and databases. Users are neither tracked nor profiled. Now you can use this tool directly in Dify.

Below are the steps for integrating SearXNG into Dify using Docker in the [Community Edition](https://docs.dify.ai/getting-started/install-self-hosted/docker-compose).

> If you want to use SearXNG within the Dify cloud service, please refer to the [SearXNG installation documentation](https://docs.searxng.org/admin/installation.html) to set up your own service, then return to Dify and fill in the service's Base URL in the "Tools > SearXNG > Authenticate" page.

## 1. Modify Dify Configuration File

The configuration file is located at `dify/api/core/tools/provider/builtin/searxng/docker/settings.yml`, and you can refer to the config documentation [here](https://docs.searxng.org/admin/settings/index.html).

## 2. Start the Service

Start the Docker container in the dify root directory.

```bash
cd dify
docker run --rm -d -p 8081:8080 -v "${PWD}/api/core/tools/provider/builtin/searxng/docker:/etc/searxng" searxng/searxng
```

## 3. Use SearXNG

Fill in the access address in "Tools > SearXNG > Authenticate" to establish a connection between the Dify service and the SearXNG service. The Docker internal address for SearXNG is usually `http://host.docker.internal:8081`.

---

# Hosting SearXNG on a Linux VM for a Private Instance

This section covers how to host **SearXNG** on a **Linux VM** and make it accessible to Dify.

### 1. Prepare the Linux VM

Ensure your Linux VM has the following:

- A **fresh installation** of a supported Linux distribution (e.g., Ubuntu 24.04 or any Debian-based distribution).
- **Docker** and **Docker Compose** installed.

#### 1.1 Install Docker

Follow these commands to install Docker:

```bash
# Update your package list
sudo apt update

# Install necessary packages
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker's official repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

Verify Docker installation:

```bash
docker --version
```

#### 1.2 Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/2.32.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify Docker Compose installation:

```bash
docker-compose --version
```

### 2. Set Up SearXNG Docker Container

#### 2.1 Clone the SearXNG Docker Repository

Clone the SearXNG repository into your desired directory on the Linux VM:

```bash
git clone https://github.com/searxng/searxng-docker.git
cd searxng-docker
```

#### 2.2 Modify Docker Configuration

1. **Edit the `docker-compose.yaml` file** to bind SearXNG to port `8081` and configure Redis. Ensure it looks like this:

```yaml
version: '3'

services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8081:8080"
    volumes:
      - ./searxng:/etc/searxng
    networks:
      - searxng_network

  redis:
    image: valkey/valkey:8-alpine
    ports:
      - "6379:6379"
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

2. **Edit the `settings.yml`** configuration file to set the bind address and enable JSON format:

```yaml
server:
  bind_address: "0.0.0.0"  # Allow external access
  port: 8080

search:
  formats:
    - html
    - json
    - csv
    - rss
```

#### 2.3 Build and Start the Docker Containers

Once you’ve made the necessary changes, run the following command to start the containers:

```bash
docker-compose up -d
```

### 3. Expose SearXNG to the Public Network

By default, SearXNG in Docker will be bound to `localhost` or `127.0.0.1`. To make it accessible externally (especially for Dify to connect), ensure the port `8081` is open on your Linux VM and that you’re using the appropriate public IP address.

You can check your VM's IP address with:

```bash
ip addr show
```

For the SearXNG service to be accessed from other machines or services (like Dify), you need to replace the Docker internal URL with your VM's public IP address.

---

# 4. Connect SearXNG with Dify

Once your SearXNG instance is up and running on the Linux VM, you need to authenticate it in Dify.

### 4.1 Configure Dify

1. Go to **Tools > SearXNG > Authenticate** in the Dify platform.
2. Enter the **Base URL** of your self-hosted SearXNG instance, using your VM’s IP address:

```text
http://<your-linux-vm-ip>:8081
```

3. After entering the correct URL, save the configuration.

---

## 5. Testing SearXNG Integration

You can test if everything is working correctly by making a sample search using `curl`:

```bash
curl "http://<your-linux-vm-ip>:8081/search?q=apple&format=json&categories=general"
```

You should receive a JSON response with search results for "apple".

---

## Conclusion

By following these steps, you can successfully host a private instance of **SearXNG** on your **Linux VM** and integrate it with **Dify**. You’ll have your own self-hosted search engine, ensuring privacy and customization for your needs.
