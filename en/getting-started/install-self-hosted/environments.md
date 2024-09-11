# Environments

### Common Variables

#### CONSOLE_API_URL

The backend URL for the console API. This is used to construct the authorization callback. If left empty, it defaults to the same domain as the application. Example: `https://api.console.dify.ai`

#### CONSOLE_WEB_URL

The front-end URL of the console web interface. This is used to construct front-end addresses and for CORS configuration. If left empty, it defaults to the same domain as the application. Example: `https://console.dify.ai`

#### SERVICE_API_URL

The Service API URL, used to display Service API Base URL in the front-end. If left empty, it defaults to the same domain as the application. Example: `https://api.dify.ai`

#### APP_API_URL

The WebApp API backend URL, used to specify the backend URL for the front-end API. If left empty, it defaults to the same domain as the application. Example: `https://app.dify.ai`

#### APP_WEB_URL

The WebApp URL, used to display WebAPP API Base URL in the front-end. If left empty, it defaults to the same domain as the application. Example: `https://api.app.dify.ai`

#### FILES_URL

The prefix for file preview or download URLs, used to display these URLs in the front-end and provide them as input for multi-modal models. To prevent forgery, image preview URLs are signed and expire after 5 minutes.

***

### Server

#### MODE

Startup mode: This is only available when launched using docker. It is not applicable when running from source code.

- api

  Start API Server.

- worker

  Start asynchronous queue worker.

#### DEBUG

Debug mode: Disabled by default. It's recommended to enable this setting during local development to prevent issues caused by monkey patching.

#### FLASK_DEBUG

Flask debug mode: When enabled, it outputs trace information in the API responses, facilitating easier debugging.

#### SECRET_KEY

A secret key used for securely signing session cookies and encrypting sensitive information in the database.

This variable must be set before the first launch.

You can generate a strong key using `openssl rand -base64 42`.

#### DEPLOY_ENV

Deployment environment:

- PRODUCTION (default)

  Production environment.

- TESTING

  Testing environment. There will be a distinct color label on the front-end page, indicating that this environment is a testing environment.

#### LOG_LEVEL

The log output level. Default is INFO. For production environments, it's recommended to set this to ERROR.

#### MIGRATION_ENABLED

When set to true, database migrations are automatically executed on container startup. This is only available when launched using docker and does not apply when running from source code.

For source code launches, you need to manually run `flask db upgrade` in the api directory.

#### CHECK_UPDATE_URL

Controls the version checking policy. If set to false, the system will not call `https://updates.dify.ai` to check for updates.

Currently, the version check interface based on CloudFlare Worker is not directly accessible in China. Setting this variable to an empty value will disable this API call.

#### OPENAI_API_BASE

Used to change the OpenAI base address, default is [https://api.openai.com/v1](https://api.openai.com/v1).

When OpenAI cannot be accessed in China, replace it with a domestic mirror address, or when a local model provides OpenAI compatible API, it can be replaced.

#### Container Startup Related Configuration

Only effective when starting with docker image or docker-compose.

- DIFY_BIND_ADDRESS

  API service binding address, default: 0.0.0.0, i.e., all addresses can be accessed.

- DIFY_PORT

  API service binding port number, default to 5001.

- SERVER_WORKER_AMOUNT

  The number of API server workers, i.e., the number of gevent workers. Formula: `number of cpu cores x 2 + 1`

  Reference: [https://docs.gunicorn.org/en/stable/design.html#how-many-workers](https://docs.gunicorn.org/en/stable/design.html#how-many-workers)

- SERVER_WORKER_CLASS

  Defaults to gevent. If using windows, it can be switched to sync or solo.

- GUNICORN_TIMEOUT

  Request handling timeout. Default is 200. Recommended value is 360 to support longer SSE (Server-Sent Events) connection times.

- CELERY_WORKER_CLASS

  Similar to `SERVER_WORKER_CLASS`. Default is gevent. If using windows, it can be switched to sync or solo.

- CELERY_WORKER_AMOUNT

  The number of Celery workers. The default is 1, and can be set as needed.

#### Database Configuration

The database uses PostgreSQL. Please use the public schema.

- DB_USERNAME: username
- DB_PASSWORD: password
- DB_HOST: database host
- DB_PORT: database port number, default is 5432
- DB_DATABASE: database name
- SQLALCHEMY_POOL_SIZE: The size of the database connection pool. The default is 30 connections, which can be appropriately increased.
- SQLALCHEMY_POOL_RECYCLE: Database connection pool recycling time, the default is 3600 seconds.
- SQLALCHEMY_ECHO: Whether to print SQL, default is false.

#### Redis Configuration

This Redis configuration is used for caching and for pub/sub during conversation.

- REDIS_HOST: Redis host
- REDIS_PORT: Redis port, default is 6379
- REDIS_DB: Redis Database, default is 0. Please use a different Database from Session Redis and Celery Broker.
- REDIS_USERNAME: Redis username, default is empty
- REDIS_PASSWORD: Redis password, default is empty. It is strongly recommended to set a password.
- REDIS_USE_SSL: Whether to use SSL protocol for connection, default is false
- REDIS_USE_SENTINEL: Use Redis Sentinel to connect to Redis servers
- REDIS_SENTINELS: Sentinel nodes, format: `<sentinel1_ip>:<sentinel1_port>,<sentinel2_ip>:<sentinel2_port>,<sentinel3_ip>:<sentinel3_port>`
- REDIS_SENTINEL_SERVICE_NAME: Sentinel service name, same as Master Name
- REDIS_SENTINEL_USERNAME: Username for Sentinel
- REDIS_SENTINEL_PASSWORD: Password for Sentinel
- REDIS_SENTINEL_SOCKET_TIMEOUT: Sentinel timeout, default value: 0.1, unit: seconds


#### Celery Configuration

- CELERY_BROKER_URL

  Format as follows(direct connection mode):

  ```
  redis://<redis_username>:<redis_password>@<redis_host>:<redis_port>/<redis_database>
  ```

  Example: `redis://:difyai123456@redis:6379/1`

  Sentinel mode:

  ```
  sentinel://<sentinel_username>:<sentinel_password>@<sentinel_host>:<sentinel_port>/<redis_database>
  ```

  Example: `sentinel://localhost:26379/1;sentinel://localhost:26380/1;sentinel://localhost:26381/1`

- BROKER_USE_SSL

  If set to true, use SSL protocol for connection, default is false

- CELERY_USE_SENTINEL

  If set to true, Sentinel mode will be enabled, default is false

- CELERY_SENTINEL_MASTER_NAME

  The service name of Sentinel, i.e., Master Name

- CELERY_SENTINEL_SOCKET_TIMEOUT

  Timeout for connecting to Sentinel, default value: 0.1, unit: seconds

#### CORS Configuration

Used to set the front-end cross-domain access policy.

- CONSOLE_CORS_ALLOW_ORIGINS

  Console CORS cross-domain policy, default is `*`, that is, all domains can access.

- WEB_API_CORS_ALLOW_ORIGINS

  WebAPP CORS cross-domain policy, default is `*`, that is, all domains can access.

#### File Storage Configuration

Used to store uploaded data set files, team/tenant encryption keys, and other files.

- STORAGE_TYPE

  Type of storage facility

  - local (default)

    Local file storage, if this option is selected, the following `STORAGE_LOCAL_PATH` configuration needs to be set.

  - s3

    S3 object storage, if this option is selected, the following S3\_ prefixed configurations need to be set.

  - azure-blob

    Azure Blob object storage, if this option is selected, the following AZURE_BLOB\_ prefixed configurations need to be set.

  - huawei-obs

    Huawei OBS object storage, if this option is selected, the following HUAWEI_OBS\_ prefixed configurations need to be set.

  - volcengine-tos

    Volcengine TOS object storage, if this option is selected, the following VOLCENGINE_TOS\_ prefixed configurations need to be set.

- STORAGE_LOCAL_PATH

  Default is storage, that is, it is stored in the storage directory of the current directory.

  If you are deploying with docker or docker-compose, be sure to mount the `/app/api/storage` directory in both containers to the same local directory, otherwise, you may encounter file not found errors.

- S3_ENDPOINT: S3 endpoint address
- S3_BUCKET_NAME: S3 bucket name
- S3_ACCESS_KEY: S3 Access Key
- S3_SECRET_KEY: S3 Secret Key
- S3_REGION: S3 region information, such as: us-east-1
- AZURE_BLOB_ACCOUNT_NAME: your-account-name eg, 'difyai'
- AZURE_BLOB_ACCOUNT_KEY: your-account-key eg, 'difyai'
- AZURE_BLOB_CONTAINER_NAME: your-container-name eg, 'difyai-container'
- AZURE_BLOB_ACCOUNT_URL: 'https://\<your_account_name>.blob.core.windows.net'
- ALIYUN_OSS_BUCKET_NAME: your-bucket-name eg, 'difyai'
- ALIYUN_OSS_ACCESS_KEY: your-access-key eg, 'difyai'
- ALIYUN_OSS_SECRET_KEY: your-secret-key eg, 'difyai'
- ALIYUN_OSS_ENDPOINT: https://oss-ap-southeast-1-internal.aliyuncs.com # reference: https://www.alibabacloud.com/help/en/oss/user-guide/regions-and-endpoints
- ALIYUN_OSS_REGION: ap-southeast-1 # reference: https://www.alibabacloud.com/help/en/oss/user-guide/regions-and-endpoints
- ALIYUN_OSS_AUTH_VERSION: v4
- ALIYUN_OSS_PATH: your-path # Don't start with '/'. OSS doesn't support leading slash in object names. reference: https://www.alibabacloud.com/help/en/oss/support/0016-00000005
- HUAWEI_OBS_BUCKET_NAME: your-bucket-name eg, 'difyai'
- HUAWEI_OBS_SECRET_KEY: your-secret-key eg, 'difyai'
- HUAWEI_OBS_ACCESS_KEY: your-access-key eg, 'difyai'
- HUAWEI_OBS_SERVER: your-server-url # reference: https://support.huaweicloud.com/sdk-python-devg-obs/obs_22_0500.html
- VOLCENGINE_TOS_BUCKET_NAME: your-bucket-name eg, 'difyai'
- VOLCENGINE_TOS_SECRET_KEY: your-secret-key eg, 'difyai'
- VOLCENGINE_TOS_ACCESS_KEY: your-access-key eg, 'difyai'
- VOLCENGINE_TOS_REGION: your-region eg, 'cn-guangzhou' # reference: https://www.volcengine.com/docs/6349/107356
- VOLCENGINE_TOS_ENDPOINT: your-endpoint eg, 'tos-cn-guangzhou.volces.com' # reference: https://www.volcengine.com/docs/6349/107356

#### Vector Database Configuration

- VECTOR_STORE
  - **Available enumeration types include：**
    - `weaviate`
    - `qdrant`
    - `milvus`
    - `zilliz` (share the same configuration as `milvus`)
    - `myscale`
    - `pinecone` (not yet open)
- WEAVIATE_ENDPOINT

  Weaviate endpoint address, such as: `http://weaviate:8080`.

- WEAVIATE_API_KEY

  The api-key credential used to connect to Weaviate.

- WEAVIATE_BATCH_SIZE

  The number of index Objects created in batches in Weaviate, default is 100.

  Refer to this document: [https://weaviate.io/developers/weaviate/manage-data/import#how-to-set-batch-parameters](https://weaviate.io/developers/weaviate/manage-data/import#how-to-set-batch-parameters)

- WEAVIATE_GRPC_ENABLED

  Whether to use the gRPC method to interact with Weaviate, performance will greatly increase when enabled, may not be usable locally, default is true.

- QDRANT_URL

  Qdrant endpoint address, such as: `https://your-qdrant-cluster-url.qdrant.tech/`

- QDRANT_API_KEY

  The api-key credential used to connect to Qdrant.

- PINECONE_API_KEY

  The api-key credential used to connect to Pinecone.

- PINECONE_ENVIRONMENT

  The environment where Pinecone is located, such as: `us-east4-gcp`

- MILVUS_URI

  Milvus uri configuration. e.g.http://localhost:19530. For Zilliz Cloud, adjust the uri and token to the [Public Endpoint and Api key](https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details).

- MILVUS_TOKEN

  Milvus token configuration, default is empty.

- MILVUS_USER

  Milvus user configuration, default is empty.

- MILVUS_PASSWORD

  Milvus password configuration, default is empty.

- MYSCALE_HOST

  MyScale host configuration.

- MYSCALE_PORT

  MyScale port configuration.

- MYSCALE_USER

  MyScale user configuration, default is `default`.

- MYSCALE_PASSWORD

  MyScale password configuration, default is empty.

- MYSCALE_DATABASE

  MyScale database configuration, default is `default`.

- MYSCALE_FTS_PARAMS

  MyScale text-search params, check [MyScale docs](https://myscale.com/docs/en/text-search/#understanding-fts-index-parameters) for multi-language support, default is empty.

#### Knowledge Configuration

- UPLOAD_FILE_SIZE_LIMIT:

  Upload file size limit, default 15M.

- UPLOAD_FILE_BATCH_LIMIT

  The maximum number of files that can be uploaded at a time, default 5.

- ETL_TYPE

  **Available enumeration types include:**

  - dify

    Dify's proprietary file extraction scheme

  - Unstructured

    Unstructured.io file extraction scheme

- UNSTRUCTURED_API_URL

  Unstructured API path, needs to be configured when ETL_TYPE is Unstructured.

  For example: `http://unstructured:8000/general/v0/general`

#### Multi-modal Configuration

- MULTIMODAL_SEND_IMAGE_FORMAT

  The format of the image sent when the multi-modal model is input, the default is `base64`, optional `url`. The delay of the call in `url` mode will be lower than that in `base64` mode. It is generally recommended to use the more compatible `base64` mode. If configured as `url`, you need to configure `FILES_URL` as an externally accessible address so that the multi-modal model can access the image.

- UPLOAD_IMAGE_FILE_SIZE_LIMIT

  Upload image file size limit, default 10M.

#### Sentry Configuration

Used for application monitoring and error log tracking.

- SENTRY_DSN

  Sentry DSN address, default is empty, when empty, all monitoring information is not reported to Sentry.

- SENTRY_TRACES_SAMPLE_RATE

  The reporting ratio of Sentry events, if it is 0.01, it is 1%.

- SENTRY_PROFILES_SAMPLE_RATE

  The reporting ratio of Sentry profiles, if it is 0.01, it is 1%.

#### Notion Integration Configuration

Notion integration configuration variables can be obtained by applying for Notion integration: [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)

- NOTION_INTEGRATION_TYPE: Configure as "public" or "internal". Since Notion's OAuth redirect URL only supports HTTPS, if deploying locally, please use Notion's internal integration.
- NOTION_CLIENT_SECRET: Notion OAuth client secret (used for public integration type)
- NOTION_CLIENT_ID: OAuth client ID (used for public integration type)
- NOTION_INTERNAL_SECRET: Notion internal integration secret. If the value of `NOTION_INTEGRATION_TYPE` is "internal", you need to configure this variable.

#### Mail related configuration

- MAIL_TYPE
  - resend
    - MAIL_DEFAULT_SEND_FROM\
      The sender's email name, such as: no-reply [no-reply@dify.ai](mailto:no-reply@dify.ai), not mandatory.
    - RESEND_API_KEY\
      API-Key for the Resend email provider, can be obtained from API-Key.
  - smtp
    - SMTP_SERVER\
      SMTP server address
    - SMTP_PORT\
      SMTP server port number
    - SMTP_USERNAME\
      SMTP username
    - SMTP_PASSWORD\
      SMTP password
    - SMTP_USE_TLS\
      Whether to use TLS, default is false
    - MAIL_DEFAULT_SEND_FROM\
      The sender's email name, such as: no-reply [no-reply@dify.ai](mailto:no-reply@dify.ai), not mandatory.

#### ModelProvider & Tool Position Configuration

Used to specify the model providers and tools that can be used in the app. These settings allow you to customize which tools and model providers are available, as well as their order and inclusion/exclusion in the app's interface.

For a list of available [tools](https://github.com/langgenius/dify/blob/main/api/core/tools/provider/_position.yaml) and [model providers](https://github.com/langgenius/dify/blob/main/api/core/model_runtime/model_providers/_position.yaml), please refer to the provided links.

- POSITION_TOOL_PINS

  Pin specific tools to the top of the list, ensuring they appear first in the interface. (Use comma-separated values with **no spaces** between items.)

  Example: `POSITION_TOOL_PINS=bing,google`

- POSITION_TOOL_INCLUDES

  Specify the tools to be included in the app. Only the tools listed here will be available for use. If not set, all tools will be included unless specified in POSITION_TOOL_EXCLUDES. (Use comma-separated values with **no spaces** between items.)

  Example: `POSITION_TOOL_INCLUDES=bing,google`

- POSITION_TOOL_EXCLUDES

  Exclude specific tools from being displayed or used in the app. Tools listed here will be omitted from the available options, except for pinned tools. (Use comma-separated values with **no spaces** between items.)

  Example: `POSITION_TOOL_EXCLUDES=yahoo,wolframalpha`

- POSITION_PROVIDER_PINS

  Pin specific model providers to the top of the list, ensuring they appear first in the interface. (Use comma-separated values with **no spaces** between items.)

  Example: `POSITION_PROVIDER_PINS=openai,openllm`

- POSITION_PROVIDER_INCLUDES

  Specify the model providers to be included in the app. Only the providers listed here will be available for use. If not set, all providers will be included unless specified in POSITION_PROVIDER_EXCLUDES. (Use comma-separated values with **no spaces** between items.)

  Example: `POSITION_PROVIDER_INCLUDES=cohere,upstage`

- POSITION_PROVIDER_EXCLUDES

  Exclude specific model providers from being displayed or used in the app. Providers listed here will be omitted from the available options, except for pinned providers. (Use comma-separated values with **no spaces** between items.)

  Example: `POSITION_PROVIDER_EXCLUDES=openrouter,ollama`

#### Others

- INVITE_EXPIRY_HOURS: Member invitation link valid time (hours), Default: 72.

---

### Web Frontend

#### SENTRY_DSN

Sentry DSN address, default is empty, when empty, all monitoring information is not reported to Sentry.

## Deprecated

#### CONSOLE_URL

> ⚠️ Modified in 0.3.8, will be deprecated in 0.4.9, replaced by: `CONSOLE_API_URL` and `CONSOLE_WEB_URL`.

Console URL, used to concatenate the authorization callback, console front-end address, and CORS configuration use. If empty, it is the same domain. Example: `https://console.dify.ai`.

#### API_URL

> ⚠️ Modified in 0.3.8, will be deprecated in 0.4.9, replaced by `SERVICE_API_URL`.

API URL, used to display Service API Base URL to the front-end. If empty, it is the same domain. Example: `https://api.dify.ai`

#### APP_URL

> ⚠️ Modified in 0.3.8, will be deprecated in 0.4.9, replaced by `APP_API_URL` and `APP_WEB_URL`.

WebApp Url, used to display WebAPP API Base Url to the front-end. If empty, it is the same domain. Example: `https://api.app.dify.ai`

#### Session Configuration

> ⚠️ This configuration is no longer valid since v0.3.24.

Only used by the API service for interface identity verification.

- SESSION_TYPE：

  Session component type

  - redis (default)

    If you choose this, you need to set the environment variables starting with SESSION_REDIS\_ below.

  - sqlalchemy

    If you choose this, the current database connection will be used and the sessions table will be used to read and write session records.

- SESSION_REDIS_HOST: Redis host
- SESSION_REDIS_PORT: Redis port, default is 6379
- SESSION_REDIS_DB: Redis Database, default is 0. Please use a different Database from Redis and Celery Broker.
- SESSION_REDIS_USERNAME: Redis username, default is empty
- SESSION_REDIS_PASSWORD: Redis password, default is empty. It is strongly recommended to set a password.
- SESSION_REDIS_USE_SSL: Whether to use SSL protocol for connection, default is false

#### Cookie Policy Configuration

> ⚠️ This configuration is no longer valid since v0.3.24.

Used to set the browser policy for session cookies used for identity verification.

- COOKIE_HTTPONLY

  Cookie HttpOnly configuration, default is true.

- COOKIE_SAMESITE

  Cookie SameSite configuration, default is Lax.

- COOKIE_SECURE

  Cookie Secure configuration, default is false.
