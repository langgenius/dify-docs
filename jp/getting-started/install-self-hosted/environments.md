# Environments

### Common Variables

#### CONSOLE\_API\_URL

The backend URL of the console API, used to concatenate the authorization callback. If empty, it is the same domain. Example: `https://api.console.dify.ai`

#### CONSOLE\_WEB\_URL

The front-end URL of the console web, used to concatenate some front-end addresses and for CORS configuration use. If empty, it is the same domain. Example: `https://console.dify.ai`

#### SERVICE\_API\_URL

Service API Url, used to display Service API Base Url to the front-end. If empty, it is the same domain. Example: `https://api.dify.ai`

#### APP\_API\_URL

WebApp API backend Url, used to declare the back-end URL for the front-end API. If empty, it is the same domain. Example: `https://app.dify.ai`

#### APP\_WEB\_URL

WebApp Url, used to display WebAPP API Base Url to the front-end. If empty, it is the same domain. Example: `https://api.app.dify.ai`

#### FILES\_URL

File preview or download URL prefix, used to display the file preview or download URL to the front-end or as a multi-modal model input; In order to prevent others from forging, the image preview URL is signed and has a 5-minute expiration time.

### Server

#### MODE

Startup mode, only available when starting with docker, not effective when starting from source code.

*   api

    Start API Server.
*   worker

    Start asynchronous queue worker.

#### DEBUG

Debug mode, default is false. It is recommended to turn on this configuration for local development to prevent some problems caused by monkey patch.

#### FLASK\_DEBUG

Flask debug mode, it can output trace information at the interface when turned on, which is convenient for debugging.

#### SECRET\_KEY

A key used to securely sign session cookies and encrypt sensitive information in the database.

This variable needs to be set when starting for the first time.

You can use `openssl rand -base64 42` to generate a strong key.

#### DEPLOY\_ENV

Deployment environment.

*   PRODUCTION (default)

    Production environment.
*   TESTING

    Testing environment. There will be a distinct color label on the front-end page, indicating that this environment is a testing environment.

#### LOG\_LEVEL

Log output level, default is INFO.

It is recommended to set it to ERROR for production.

#### MIGRATION\_ENABLED

When set to true, the database migration will be automatically executed when the container starts, only available when starting with docker, not effective when starting from source code.

You need to manually execute `flask db upgrade` in the api directory when starting from source code.

#### CHECK\_UPDATE\_URL

Whether to enable the version check policy. If set to false, `https://updates.dify.ai` will not be called for version check.

Since the version interface based on CloudFlare Worker cannot be directly accessed in China at present, setting this variable to empty can shield this interface call.

#### OPENAI\_API\_BASE

Used to change the OpenAI base address, default is [https://api.openai.com/v1](https://api.openai.com/v1).

When OpenAI cannot be accessed in China, replace it with a domestic mirror address, or when a local model provides OpenAI compatible API, it can be replaced.

#### Container Startup Related Configuration

Only effective when starting with docker image or docker-compose.

*   DIFY\_BIND\_ADDRESS

    API service binding address, default: 0.0.0.0, i.e., all addresses can be accessed.
*   DIFY\_PORT

    API service binding port number, default 5001.
*   SERVER\_WORKER\_AMOUNT

    The number of API server workers, i.e., the number of gevent workers. Formula: `number of cpu cores x 2 + 1`

    Reference: [https://docs.gunicorn.org/en/stable/design.html#how-many-workers](https://docs.gunicorn.org/en/stable/design.html#how-many-workers)
*   SERVER\_WORKER\_CLASS

    Defaults to gevent. If using windows, it can be switched to sync or solo.
*   GUNICORN\_TIMEOUT

    Request handling timeout. The default is 200, it is recommended to set it to 360 to support a longer sse connection time.
*   CELERY\_WORKER\_CLASS

    Similar to `SERVER_WORKER_CLASS`. Default is gevent. If using windows, it can be switched to sync or solo.
*   CELERY\_WORKER\_AMOUNT

    The number of Celery workers. The default is 1, and can be set as needed.

#### Database Configuration

The database uses PostgreSQL. Please use the public schema.

* DB\_USERNAME: username
* DB\_PASSWORD: password
* DB\_HOST: database host
* DB\_PORT: database port number, default is 5432
* DB\_DATABASE: database name
* SQLALCHEMY\_POOL\_SIZE: The size of the database connection pool. The default is 30 connections, which can be appropriately increased.
* SQLALCHEMY\_POOL\_RECYCLE: Database connection pool recycling time, the default is 3600 seconds.
* SQLALCHEMY\_ECHO: Whether to print SQL, default is false.

#### Redis Configuration

This Redis configuration is used for caching and for pub/sub during conversation.

* REDIS\_HOST: Redis host
* REDIS\_PORT: Redis port, default is 6379
* REDIS\_DB: Redis Database, default is 0. Please use a different Database from Session Redis and Celery Broker.
* REDIS\_USERNAME: Redis username, default is empty
* REDIS\_PASSWORD: Redis password, default is empty. It is strongly recommended to set a password.
* REDIS\_USE\_SSL: Whether to use SSL protocol for connection, default is false

#### Celery Configuration

*   CELERY\_BROKER\_URL

    Format as follows:

    ```
    redis://<redis_username>:<redis_password>@<redis_host>:<redis_port>/<redis_database>
    ```

    Example: `redis://:difyai123456@redis:6379/1`
*   BROKER\_USE\_SSL

    If set to true, use SSL protocol for connection, default is false

#### CORS Configuration

Used to set the front-end cross-domain access policy.

*   CONSOLE\_CORS\_ALLOW\_ORIGINS

    Console CORS cross-domain policy, default is `*`, that is, all domains can access.
*   WEB\_API\_CORS\_ALLOW\_ORIGINS

    WebAPP CORS cross-domain policy, default is `*`, that is, all domains can access.

#### File Storage Configuration

Used to store uploaded data set files, team/tenant encryption keys, and other files.

*   STORAGE\_TYPE

    Type of storage facility

    *   local (default)

        Local file storage, if this option is selected, the following `STORAGE_LOCAL_PATH` configuration needs to be set.
    *   s3

        S3 object storage, if this option is selected, the following S3\_ prefixed configurations need to be set.
    *   azure-blob

        Azure Blob object storage, if this option is selected, the following AZURE\_BLOB\_ prefixed configurations need to be set.
*   STORAGE\_LOCAL\_PATH

    Default is storage, that is, it is stored in the storage directory of the current directory.

    If you are deploying with docker or docker-compose, be sure to mount the `/app/api/storage` directory in both containers to the same local directory, otherwise, you may encounter file not found errors.
* S3\_ENDPOINT: S3 endpoint address
* S3\_BUCKET\_NAME: S3 bucket name
* S3\_ACCESS\_KEY: S3 Access Key
* S3\_SECRET\_KEY: S3 Secret Key
* S3\_REGION: S3 region information, such as: us-east-1
* AZURE\_BLOB\_ACCOUNT\_NAME: your-account-name eg, 'difyai'
* AZURE\_BLOB\_ACCOUNT\_KEY: your-account-key eg, 'difyai'
* AZURE\_BLOB\_CONTAINER\_NAME: your-container-name eg, 'difyai-container'
* AZURE\_BLOB\_ACCOUNT\_URL: 'https://\<your\_account\_name>.blob.core.windows.net'

#### Vector Database Configuration

* VECTOR\_STORE
  * **Available enumeration types include：**
    * `weaviate`
    * `qdrant`
    * `milvus`
    * `zilliz` (share the same configuration as `milvus`)
    * `pinecone` (not yet open)
*   WEAVIATE\_ENDPOINT

    Weaviate endpoint address, such as: `http://weaviate:8080`.
*   WEAVIATE\_API\_KEY

    The api-key credential used to connect to Weaviate.
*   WEAVIATE\_BATCH\_SIZE

    The number of index Objects created in batches in Weaviate, default is 100.

    Refer to this document: [https://weaviate.io/developers/weaviate/manage-data/import#how-to-set-batch-parameters](https://weaviate.io/developers/weaviate/manage-data/import#how-to-set-batch-parameters)
*   WEAVIATE\_GRPC\_ENABLED

    Whether to use the gRPC method to interact with Weaviate, performance will greatly increase when enabled, may not be usable locally, default is true.
*   QDRANT\_URL

    Qdrant endpoint address, such as: `https://your-qdrant-cluster-url.qdrant.tech/`
*   QDRANT\_API\_KEY

    The api-key credential used to connect to Qdrant.
*   PINECONE\_API\_KEY

    The api-key credential used to connect to Pinecone.
*   PINECONE\_ENVIRONMENT

    The environment where Pinecone is located, such as: `us-east4-gcp`
*   MILVUS\_HOST

    Milvus host configuration.
*   MILVUS\_PORT

    Milvus port configuration.
*   MILVUS\_USER

    Milvus user configuration, default is empty.
*   MILVUS\_PASSWORD

    Milvus password configuration, default is empty.
*   MILVUS\_SECURE

    Whether Milvus uses SSL connection, default is false.

#### Knowledge Configuration

*   UPLOAD\_FILE\_SIZE\_LIMIT:

    Upload file size limit, default 15M.
*   UPLOAD\_FILE\_BATCH\_LIMIT

    The maximum number of files that can be uploaded at a time, default 5.
*   ETL\_TYPE

    **Available enumeration types include:**

    *   dify

        Dify's proprietary file extraction scheme
    *   Unstructured

        Unstructured.io file extraction scheme
*   UNSTRUCTURED\_API\_URL

    Unstructured API path, needs to be configured when ETL\_TYPE is Unstructured.

    For example: `http://unstructured:8000/general/v0/general`

#### Multi-modal Configuration

*   MULTIMODAL\_SEND\_IMAGE\_FORMAT

    The format of the image sent when the multi-modal model is input, the default is `base64`, optional `url`. The delay of the call in `url` mode will be lower than that in `base64` mode. It is generally recommended to use the more compatible `base64` mode. If configured as `url`, you need to configure `FILES_URL` as an externally accessible address so that the multi-modal model can access the image.
*   UPLOAD\_IMAGE\_FILE\_SIZE\_LIMIT

    Upload image file size limit, default 10M.

#### Sentry Configuration

Used for application monitoring and error log tracking.

*   SENTRY\_DSN

    Sentry DSN address, default is empty, when empty, all monitoring information is not reported to Sentry.
*   SENTRY\_TRACES\_SAMPLE\_RATE

    The reporting ratio of Sentry events, if it is 0.01, it is 1%.
*   SENTRY\_PROFILES\_SAMPLE\_RATE

    The reporting ratio of Sentry profiles, if it is 0.01, it is 1%.

#### Notion Integration Configuration

Notion integration configuration variables can be obtained by applying for Notion integration: [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

* NOTION\_INTEGRATION\_TYPE: Configure as "public" or "internal". Since Notion's OAuth redirect URL only supports HTTPS, if deploying locally, please use Notion's internal integration.
* NOTION\_CLIENT\_SECRET: Notion OAuth client secret (used for public integration type)
* NOTION\_CLIENT\_ID: OAuth client ID (used for public integration type)
* NOTION\_INTERNAL\_SECRET: Notion internal integration secret. If the value of `NOTION_INTEGRATION_TYPE` is "internal", you need to configure this variable.

#### Mail related configuration

* MAIL\_TYPE
  * resend
    * MAIL\_DEFAULT\_SEND\_FROM\
      The sender's email name, such as: no-reply [no-reply@dify.ai](mailto:no-reply@dify.ai), not mandatory.
    * RESEND\_API\_KEY\
      API-Key for the Resend email provider, can be obtained from API-Key.
  * smtp
    * SMTP\_SERVER\
      SMTP server address
    * SMTP\_PORT\
      SMTP server port number
    * SMTP\_USERNAME\
      SMTP username
    * SMTP\_PASSWORD\
      SMTP password
    * SMTP\_USE\_TLS\
      Whether to use TLS, default is false
    * MAIL\_DEFAULT\_SEND\_FROM\
      The sender's email name, such as: no-reply [no-reply@dify.ai](mailto:no-reply@dify.ai), not mandatory.

#### Others

* INVITE\_EXPIRY\_HOURS: Member invitation link valid time (hours), Default: 72.

***

### Web Frontend

#### SENTRY\_DSN

Sentry DSN address, default is empty, when empty, all monitoring information is not reported to Sentry.

## Deprecated

#### CONSOLE\_URL

> ⚠️ Modified in 0.3.8, will be deprecated in 0.4.9, replaced by: `CONSOLE_API_URL` and `CONSOLE_WEB_URL`.

Console URL, used to concatenate the authorization callback, console front-end address, and CORS configuration use. If empty, it is the same domain. Example: `https://console.dify.ai`.

#### API\_URL

> ⚠️ Modified in 0.3.8, will be deprecated in 0.4.9, replaced by `SERVICE_API_URL`.

API URL, used to display Service API Base URL to the front-end. If empty, it is the same domain. Example: `https://api.dify.ai`

#### APP\_URL

> ⚠️ Modified in 0.3.8, will be deprecated in 0.4.9, replaced by `APP_API_URL` and `APP_WEB_URL`.

WebApp Url, used to display WebAPP API Base Url to the front-end. If empty, it is the same domain. Example: `https://api.app.dify.ai`

#### Session Configuration

> ⚠️ This configuration is no longer valid since v0.3.24.

Only used by the API service for interface identity verification.

*   SESSION\_TYPE：

    Session component type

    *   redis (default)

        If you choose this, you need to set the environment variables starting with SESSION\_REDIS\_ below.
    *   sqlalchemy

        If you choose this, the current database connection will be used and the sessions table will be used to read and write session records.
* SESSION\_REDIS\_HOST: Redis host
* SESSION\_REDIS\_PORT: Redis port, default is 6379
* SESSION\_REDIS\_DB: Redis Database, default is 0. Please use a different Database from Redis and Celery Broker.
* SESSION\_REDIS\_USERNAME: Redis username, default is empty
* SESSION\_REDIS\_PASSWORD: Redis password, default is empty. It is strongly recommended to set a password.
* SESSION\_REDIS\_USE\_SSL: Whether to use SSL protocol for connection, default is false

#### Cookie Policy Configuration

> ⚠️ This configuration is no longer valid since v0.3.24.

Used to set the browser policy for session cookies used for identity verification.

*   COOKIE\_HTTPONLY

    Cookie HttpOnly configuration, default is true.
*   COOKIE\_SAMESITE

    Cookie SameSite configuration, default is Lax.
*   COOKIE\_SECURE

    Cookie Secure configuration, default is false.
