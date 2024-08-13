# SearXNG
SearXNG is a free internet metasearch engine which aggregates results from various search services and databases. Users are neither tracked nor profiled. Dify has implemented the interface to access the SearXNG, so you can use it directly in Dify. Below are the steps for integrating SearXNG with Dify using Docker. If you wish to install SearXNG through other methods, please refer to [here](https://docs.searxng.org/admin/installation.html).

## 1. Modify the configuration as needed, or you can use the default settings.   
The configuration file is located at `dify/api/core/tools/provider/builtin/searxng/docker/settings.yml`, and you can refer to the config documentation [here](https://docs.searxng.org/admin/settings/index.html).


## 2. Start the Docker container in the dify root directory.
```
cd dify
docker run --rm -d -p 8081:8080 -v "${PWD}/api/core/tools/provider/builtin/searxng/docker:/etc/searxng" searxng/searxng
```

## 3. Integrate SearXNG in Dify  
In `Tools > SearXNG > To Authorize`, enter the access address. If you are using Dify deployed with docker, this address is usually `http://host.docker.internal:8081`.
