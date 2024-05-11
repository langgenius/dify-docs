# Vector Database Migrate Tool

When you want to switch to another vector database, you can deactivate or delete the original vector database after switching.

## How to use

### Step:

1. If you are starting from local source code, modify the environment variable in the `.env` file to the vector database you want to migrate to.

For example:&#x20;

```
VECTOR_STORE=qdrant
```

2. If you are starting from `docker compose`, modify the environment variable in the `docker-compose.yaml` file to the vector database you want to migrate to, both api and worker are all needed.

For example:

```
# The type of vector store to use. Supported values are `weaviate`, `qdrant`, `milvus`.
VECTOR_STORE: qdrant
```

3. run the below command in your terminal or docker container

```
flask vdb-migrarte
```
