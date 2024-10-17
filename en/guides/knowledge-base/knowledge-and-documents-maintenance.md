# Knowledge Base and Document Maintenance

## Knowledge Base Management

> The knowledge base page is accessible only to the team owner, team administrators, and users with editor permissions.

On the Dify team homepage, click the "Knowledge Base" tab at the top, select the knowledge base you want to manage, then click **Settings** in the left navigation panel to make adjustments. You can modify the knowledge base name, description, visibility permissions, indexing mode, embedding model, and retrieval settings.

<figure><img src="../../.gitbook/assets/knowledge-settings-01.png" alt=""><figcaption><p>Knowledge Base Settings</p></figcaption></figure>

**Knowledge Base Name**: Used to distinguish among different knowledge bases.

**Knowledge Description**: Used to describe the information represented by the documents in the knowledge base.

**Visibility Permissions**: Defines access control for the knowledge base with three levels:

1. **"Only Me"**: Restricts access to the knowledge base owner.
2. **"All team members"**: Grants access to every member of the team.
3. **"Partial team members"**: Allows selective access to specific team members.

Users without appropriate permissions cannot access the knowledge base. When granting access to team members (options 2 or 3), authorized users receive full permissions, including view, edit, and delete rights for the knowledge base content.

**Indexing Mode**: For detailed explanations, please [refer to the documentation](https://docs.dify.ai/guides/knowledge-base/create-knowledge-and-upload-documents#5-indexing-method).

**Embedding Model**: Allows you to modify the embedding model for the knowledge base. Changing the embedding model will re-embed all documents in the knowledge base, and the original embeddings will be deleted.

**Retrieval Settings**: For detailed explanations, please [refer to the documentation](https://docs.dify.ai/guides/knowledge-base/create-knowledge-and-upload-documents#6-retrieval-settings).

***

### Knowledge Base API Management

Dify Knowledge Base provides a complete set of standard APIs. Developers can use API calls to perform daily management and maintenance operations such as adding, deleting, modifying, and querying documents and chunks in the knowledge base. Please refer to the [Knowledge Base API Documentation](maintain-dataset-via-api.md).

<figure><img src="../../.gitbook/assets/knowledge-base-api.png" alt=""><figcaption><p>Knowledge base API management</p></figcaption></figure>

## Maintaining Text in the Knowledge Base

### Viewing Text Chunks

Each document uploaded to the knowledge base is stored in the form of text chunks. You can view the specific text content of each chunks in the chunks list.

<figure><img src="../../.gitbook/assets/viewing-uploaded-document-segments.png" alt=""><figcaption><p>Viewing uploaded document chunks</p></figcaption></figure>

***

### Checking Chunk Quality

The quality of document chunk significantly affects the Q\&A performance of the knowledge base application. It is recommended to manually check the chunks quality before associating the knowledge base with the application.

Although automated chunk methods based on character length, identifiers, or NLP semantic chunk can significantly reduce the workload of large-scale text chunk, the quality of chunk is related to the text structure of different document formats and the semantic context. Manual checking and correction can effectively compensate for the shortcomings of machine chunk in semantic recognition.

When checking chunk quality, pay attention to the following situations:

* **Overly short text chunks**, leading to semantic loss;

<figure><img src="../../.gitbook/assets/short-text-segments.png" alt="" width="373"><figcaption><p>Overly short text chunks</p></figcaption></figure>

* **Overly long text chunks**, leading to semantic noise affecting matching accuracy;

<figure><img src="../../.gitbook/assets/long-text-segments.png" alt="" width="375"><figcaption><p>Overly long text chunks</p></figcaption></figure>

* **Obvious semantic truncation**, which occurs when using maximum segment length limits, leading to forced semantic truncation and missing content during recall;

<figure><img src="../../.gitbook/assets/semantic-truncation.png" alt="" width="357"><figcaption><p>Obvious semantic truncation</p></figcaption></figure>

***

### Adding Text Chunks

In the chunk list, click "Add Segment" to add one or multiple custom chunks to the document.

<figure><img src="../../.gitbook/assets/add-a-chunk.png" alt=""><figcaption></figcaption></figure>

Add a chunk

When adding chunks in bulk, you need to first download the CSV format chunk upload template, edit all the chunk content in Excel according to the template format, save the CSV file, and then upload it.

<figure><img src="../../.gitbook/assets/bulk-add-custom-segment (1).png" alt=""><figcaption><p>Bulk adding custom chunks</p></figcaption></figure>

***

### Editing Text Chunks

In the chunk list, you can directly edit the content of the added chunks, including the text content and keywords of the chunks.

<figure><img src="../../.gitbook/assets/edit-segment (1).png" alt=""><figcaption><p>Editing document chunks</p></figcaption></figure>

***

### Metadata Management

In addition to marking metadata information from different source documents, such as the title, URL, keywords, and description of web data, metadata will be used in the chunk recall process of the knowledge base as structured fields for recall filtering or displaying citation sources.

{% hint style="info" %}
The metadata filtering and citation source functions are not yet supported in the current version.
{% endhint %}

<figure><img src="../../.gitbook/assets/metadata.png" alt="" width="258"><figcaption><p>Add metadata</p></figcaption></figure>

***

### Adding Documents

In "Knowledge Base > Document List," click "Add File" to upload new documents or [Notion pages](sync-from-notion.md) to the created knowledge base.

A knowledge base (Knowledge) is a collection of documents (Documents). Documents can be uploaded by developers or operators, or synchronized from other data sources (usually corresponding to a file unit in the data source).

<figure><img src="../../.gitbook/assets/en-knowledge-add-document.png" alt=""><figcaption><p>Upload new document at Knowledge base</p></figcaption></figure>

***

### Document Disable and Archive

**Disable**: The dataset supports disabling documents or chunks that are temporarily not to be indexed. In the dataset document list, click the disable button to disable the document. You can also disable an entire document or a specific chunk in the document details. Disabled documents will not be indexed. Click enable on the disabled documents to cancel the disable status.

**Archive**: Old document data that is no longer in use can be archived if you do not want to delete it. Archived data can only be viewed or deleted, not edited. In the dataset document list, click the archive button to archive the document. You can also archive documents in the document details. Archived documents will not be indexed. Archived documents can also be unarchived.

***
