---
title: "Data Source Plugin"
---

Data source plugins are a new type of plugin introduced in Dify 1.9.0. In a knowledge pipeline, they serve as the document data source and the starting point for the entire pipeline.

This article describes how to develop a data source plugin, covering plugin architecture, code examples, and debugging methods, to help you quickly develop and launch your data source plugin.

## Prerequisites

Before reading on, ensure you have a basic understanding of the knowledge pipeline and some knowledge of plugin development. You can find relevant information here:

- [Step 2: Knowledge Pipeline Orchestration](/en/guides/knowledge-base/knowledge-pipeline/knowledge-pipeline-orchestration)
- [Dify Plugin Development: Hello World Guide](/plugin-dev-en/0211-getting-started-dify-tool)

## **Data Source Plugin Types**

Dify supports three types of data source plugins: web crawler, online document, and online drive. When implementing the plugin code, the class that provides the plugin's functionality must inherit from a specific data source class. Each of the three plugin types corresponds to a different parent class.

<Info>
  To learn how to inherit from a parent class to implement plugin functionality, see [Dify Plugin Development: Hello World Guide - 4.4 Implementing Tool Logic](/plugin-dev-en/0211-getting-started-dify-tool#4-4-implementing-tool-logic).
</Info>

Each data source plugin type supports multiple data sources. For example:

- **Web Crawler**: Jina Reader, FireCrawl
- **Online Document**: Notion, Confluence, GitHub
- **Online Drive**: OneDrive, Google Drive, Box, AWS S3, Tencent COS

The relationship between data source types and data source plugin types is illustrated below.

![](/images/data_source_type.png)

## Develop a Data Source Plugin

### Create a Data Source Plugin

You can use the scaffolding command-line tool to create a data source plugin by selecting the `datasource` type. After completing the setup, the command-line tool will automatically generate the plugin project code.

```powershell
dify plugin init
```

![](/images/datasource_plugin_init.png)

<Info>
  Typically, a data source plugin does not need to use other features of the Dify platform, so no additional permissions are required.
</Info>

#### Data Source Plugin Structure

A data source plugin consists of three main components:

- The `manifest.yaml` file: Describes the basic information about the plugin.
- The `provider` directory: Contains the plugin provider's description and authentication implementation code.
- The `datasources` directory: Contains the description and core logic for fetching data from the data source.

```
├── _assets
│   └── icon.svg
├── datasources
│   ├── your_datasource.py
│   └── your_datasource.yaml
├── main.py
├── manifest.yaml
├── PRIVACY.md
├── provider
│   ├── your_datasource.py
│   └── your_datasource.yaml
├── README.md
└── requirements.txt
```

#### Set the Correct Version and Tag

- In the `manifest.yaml` file, set the minimum supported Dify version as follows:

  ```yaml
  minimum_dify_version: 1.9.0
  ```
- In the `manifest.yaml` file, add the following tag to display the plugin under the data source category in the Dify Marketplace:

  ```yaml
  tags:
    - rag
  ```
- In the `requirements.txt` file, set the plugin SDK version used for data source plugin development as follows:

  ```yaml
  dify-plugin>=0.5.0,<0.6.0
  ```

### Add the Data Source Provider

#### Create the Provider YAML File

The content of a provider YAML file is essentially the same as that for tool plugins, with only the following two differences:

```yaml
# Specify the provider type for the data source plugin: online_drive, online_document, or website_crawl
provider_type: online_drive # online_document, website_crawl

# Specify data sources
datasources:
  - datasources/PluginName.yaml
```

<Info>
  For more about creating a provider YAML file, see [Dify Plugin Development: Hello World Guide-4.3 Configuring Provider Credentials](/plugin-dev-en/0211-getting-started-dify-tool#4-3-configuring-provider-credentials).
</Info>

<Info>
  Data source plugins support authentication via OAuth 2.0 or API Key.

  To configure OAuth, see [Add OAuth Support to Your Tool Plugin](/plugin-dev-en/0222-tool-oauth).
</Info>

#### Create the Provider Code File

- When using API Key authentication mode, the provider code file for data source plugins is identical to that for tool plugins. You only need to change the parent class inherited by the provider class to `DatasourceProvider`.

  ```python
  class YourDatasourceProvider(DatasourceProvider):
  
      def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
          try:
              """
              IMPLEMENT YOUR VALIDATION HERE
              """
          except Exception as e:
              raise ToolProviderCredentialValidationError(str(e))
  ```
- When using OAuth authentication mode, data source plugins differ slightly from tool plugins. When obtaining access permissions via OAuth, data source plugins can simultaneously return the username and avatar to be displayed on the frontend. Therefore, `_oauth_get_credentials` and `_oauth_refresh_credentials` need to return a `DatasourceOAuthCredentials` type that contains `name`, `avatar_url`, `expires_at`, and `credentials`.

  The `DatasourceOAuthCredentials` class is defined as follows and must be set to the corresponding type when returned:

  ```python
  class DatasourceOAuthCredentials(BaseModel):
      name: str | None = Field(None, description="The name of the OAuth credential")
      avatar_url: str | None = Field(None, description="The avatar url of the OAuth")
      credentials: Mapping[str, Any] = Field(..., description="The credentials of the OAuth")
      expires_at: int | None = Field(
          default=-1,
          description="""The expiration timestamp (in seconds since Unix epoch, UTC) of the credentials.
          Set to -1 or None if the credentials do not expire.""",
      )
  ```

The function signatures for `_oauth_get_authorization_url`, `_oauth_get_credentials`, and `_oauth_refresh_credentials` are as follows:

<Tabs>
  <Tab title="_oauth_get_authorization_url">
    ```python
    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    """
    Generate the authorization URL for {{ .PluginName }} OAuth.
    """
    try:
        """
        IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
        """
    except Exception as e:
        raise DatasourceOAuthError(str(e))
    return ""
    ```
  </Tab>
  <Tab title="_oauth_get_credentials">
    ```python
    def _oauth_get_credentials(
    self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    ) -> DatasourceOAuthCredentials:
    """
    Exchange code for access_token.
    """
    try:
        """
        IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
        """
    except Exception as e:
        raise DatasourceOAuthError(str(e))
    return DatasourceOAuthCredentials(
        name="",
        avatar_url="",
        expires_at=-1,
        credentials={},
    )
    ```
  </Tab>
  <Tab title="_oauth_refresh_credentials">
    ```python
    def _oauth_refresh_credentials(
    self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    ) -> DatasourceOAuthCredentials:
    """
    Refresh the credentials
    """
    return DatasourceOAuthCredentials(
        name="",
        avatar_url="",
        expires_at=-1,
        credentials={},
    )
    ```
  </Tab>
</Tabs>

### Add the Data Source

The YAML file format and data source code format vary across the three types of data sources.

#### Web Crawler

In the provider YAML file for a web crawler data source plugin, `output_schema` must always return four parameters: `source_url`, `content`, `title`, and `description`.

```yaml
output_schema:
    type: object
    properties:
      source_url:
        type: string
        description: the source url of the website
      content:
        type: string
        description: the content from the website
      title:
        type: string
        description: the title of the website
      "description":
        type: string
        description: the description of the website
```

In the main logic code for a web crawler plugin, the class must inherit from `WebsiteCrawlDatasource` and implement the `_get_website_crawl` method. You then need to use the `create_crawl_message` method to return the web crawl message.

To crawl multiple web pages and return them in batches, you can set `WebSiteInfo.status` to `processing` and use the `create_crawl_message` method to return each batch of crawled pages. After all pages have been crawled, set `WebSiteInfo.status` to `completed`.

```python
class YourDataSource(WebsiteCrawlDatasource):

    def _get_website_crawl(
        self, datasource_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:

        crawl_res = WebSiteInfo(web_info_list=[], status="", total=0, completed=0)
        crawl_res.status = "processing"
        yield self.create_crawl_message(crawl_res)
        
        ### your crawl logic
           ...
        crawl_res.status = "completed"
        crawl_res.web_info_list = [
            WebSiteInfoDetail(
                title="",
                source_url="",
                description="",
                content="",
            )
        ]
        crawl_res.total = 1
        crawl_res.completed = 1

        yield self.create_crawl_message(crawl_res)
```

#### Online Document

The return value for an online document data source plugin must include at least a `content` field to represent the document's content. For example:

```yaml
output_schema:
    type: object
    properties:
      workspace_id:
        type: string
        description: workspace id
      page_id:
        type: string
        description: page id
      content:
        type: string
        description: page content
```

In the main logic code for an online document plugin, the class must inherit from `OnlineDocumentDatasource` and implement two methods: `_get_pages` and `_get_content`.

When a user runs the plugin, it first calls the `_get_pages` method to retrieve a list of documents. After the user selects a document from the list, it then calls the `_get_content` method to fetch the document's content.

<Tabs>
  <Tab title="_get_pages">
    ```python
    def _get_pages(self, datasource_parameters: dict[str, Any]) -> DatasourceGetPagesResponse:
        # your get pages logic
        response = requests.get(url, headers=headers, params=params, timeout=30)
        pages = []
        for item in  response.json().get("results", []):
            page = OnlineDocumentPage(
                page_name=item.get("title", ""),
                page_id=item.get("id", ""),
                type="page",  
                last_edited_time=item.get("version", {}).get("createdAt", ""),
                parent_id=item.get("parentId", ""),
                page_icon=None, 
            )
            pages.append(page)
        online_document_info = OnlineDocumentInfo(
            workspace_name=workspace_name,
            workspace_icon=workspace_icon,
            workspace_id=workspace_id,
            pages=[page],
            total=pages.length(),
        )
        return DatasourceGetPagesResponse(result=[online_document_info])
    ```
  </Tab>
  <Tab title="_get_content">
    ```python
    def _get_content(self, page: GetOnlineDocumentPageContentRequest) -> Generator[DatasourceMessage, None, None]:
    # your fetch content logic, example
    response = requests.get(url, headers=headers, params=params, timeout=30)
    ...
    yield self.create_variable_message("content", "")
    yield self.create_variable_message("page_id", "")
    yield self.create_variable_message("workspace_id", "")
    ```
  </Tab>
</Tabs>

#### Online Drive

An online drive data source plugin returns a file, so it must adhere to the following specification:

```yaml
output_schema:
    type: object
    properties:
      file:
        $ref: "https://dify.ai/schemas/v1/file.json"
```

In the main logic code for an online drive plugin, the class must inherit from `OnlineDriveDatasource` and implement two methods: `_browse_files` and `_download_file`.

When a user runs the plugin, it first calls `_browse_files` to get a file list. At this point, `prefix` is empty, indicating a request for the root directory's file list. The file list contains both folder and file type variables. If the user opens a folder, the `_browse_files` method is called again. At this point, the `prefix` in `OnlineDriveBrowseFilesRequest` will be the folder ID used to retrieve the file list within that folder.

After a user selects a file, the plugin uses the `_download_file` method and the file ID to get the file's content. You can use the `_get_mime_type_from_filename` method to get the file's MIME type, allowing the pipeline to handle different file types appropriately.

When the file list contains multiple files, you can set `OnlineDriveFileBucket.is_truncated` to `True` and set `OnlineDriveFileBucket.next_page_parameters` to the parameters needed to fetch the next page of the file list, such as the next page's request ID or URL, depending on the service provider.

<Tabs>
  <Tab title="_browse_files">
    ```python
    def _browse_files(
    self, request: OnlineDriveBrowseFilesRequest
    ) -> OnlineDriveBrowseFilesResponse:
    
    credentials = self.runtime.credentials
    bucket_name = request.bucket
    prefix = request.prefix or ""  # Allow empty prefix for root folder; When you browse the folder, the prefix is the folder id
    max_keys = request.max_keys or 10
    next_page_parameters = request.next_page_parameters or {}
    
    files = []
    files.append(OnlineDriveFile(
        id="", 
        name="", 
        size=0, 
        type="folder" # or "file"
    ))
    
    return OnlineDriveBrowseFilesResponse(result=[
        OnlineDriveFileBucket(
            bucket="", 
            files=files, 
            is_truncated=False, 
            next_page_parameters={}
        )
    ])
    ```
  </Tab>
  <Tab title="_download_file">
    ```python
    def _download_file(self, request: OnlineDriveDownloadFileRequest) -> Generator[DatasourceMessage, None, None]:
    credentials = self.runtime.credentials
    file_id = request.id
    
    file_content = bytes()
    file_name = ""
    
    mime_type = self._get_mime_type_from_filename(file_name)
    
    yield self.create_blob_message(file_content, meta={
        "file_name": file_name,
        "mime_type": mime_type
    })
    
    def _get_mime_type_from_filename(self, filename: str) -> str:
    """Determine MIME type from file extension."""
    import mimetypes
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"
    ```
  </Tab>
</Tabs>

For storage services like AWS S3, the `prefix`, `bucket`, and `id` variables have special uses and can be applied flexibly as needed during development:

- `prefix`: Represents the file path prefix. For example, `prefix=container1/folder1/` retrieves the files or file list from the `folder1` folder in the `container1` bucket.
- `bucket`: Represents the file bucket. For example, `bucket=container1` retrieves the files or file list in the `container1` bucket. This field can be left blank for non-standard S3 protocol drives.
- `id`: Since the `_download_file` method does not use the `prefix` variable, the full file path must be included in the `id`. For example, `id=container1/folder1/file1.txt` indicates retrieving the `file1.txt` file from the `folder1` folder in the `container1` bucket.

<Tip>
  You can refer to the specific implementations of the [official Google Drive plugin](https://github.com/langgenius/dify-official-plugins/blob/main/datasources/google_cloud_storage/datasources/google_cloud_storage.py) and the [official AWS S3 plugin](https://github.com/langgenius/dify-official-plugins/blob/main/datasources/aws_s3_storage/datasources/aws_s3_storage.py).
</Tip>

## Debug the Plugin

Data source plugins support two debugging methods: remote debugging or installing as a local plugin for debugging. Note the following:

- If the plugin uses OAuth authentication, the `redirect_uri` for remote debugging differs from that of a local plugin. Update the relevant configuration in your service provider's OAuth App accordingly.
- While data source plugins support single-step debugging, we still recommend testing them in a complete knowledge pipeline to ensure full functionality.

## Final Checks

Before packaging and publishing, make sure you've completed all of the following:

- Set the minimum supported Dify version to `1.9.0`.
- Set the SDK version to `dify-plugin>=0.5.0,<0.6.0`.
- Write the `README.md` and `PRIVACY.md` files.
- Include only English content in the code files.
- Replace the default icon with the data source provider's logo.

## Package and Publish

In the plugin directory, run the following command to generate a `.difypkg` plugin package:

```
dify plugin package . -o your_datasource.difypkg
```

Next, you can:

- Import and use the plugin in your Dify environment.
- Publish the plugin to Dify Marketplace by submitting a pull request.

<Info>
  For the plugin publishing process, see [Publishing Plugins](/plugin-dev-en/0321-release-overview).
</Info>

{/*
Contributing Section
DO NOT edit this section!
It will be automatically generated by the script.
*/}

---

[Edit this page](https://github.com/langgenius/dify-docs/edit/main/plugin-dev-en/0222-datasource-plugin.mdx) | [Report an issue](https://github.com/langgenius/dify-docs/issues/new?template=docs.yml)

