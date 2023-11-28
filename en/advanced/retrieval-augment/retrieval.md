# Retrieval

When users build knowledge base Q\&A AI applications, if multiple datasets are associated within the application, Dify supports two retrieval modes: N-to-1 retrieval and Multi-path retrieval.

<figure><img src="../../.gitbook/assets/screenshot-20231119-191531.png" alt=""><figcaption><p>Retrieval Settings</p></figcaption></figure>

## Retrieval **Settings**

### **N-to-1 Retrieval**&#x20;

Based on user intent and knowledge description, the Agent independently determines and selects the most matching single knowledge for querying relevant text. This mode is suitable for applications with distinct datasets and a smaller number of datasets. N-to-1 retrieval relies on the model's inference capability to choose the most relevant knowledge based on user intent. When inferring the knowledge, the knowledge serves as a tool for the Agent, chosen through intent inference; the tool description is essentially the knowledge description.

When users upload datasets, the system automatically creates a summary description of each knowledge. To achieve the best retrieval results in this mode, you can view the system-generated summary description under “Knowledge -> Settings -> Knowledge Description” and check if this content clearly summarizes the knowledge's content.

Here is the technical flowchart for N-to-1 retrieval:

<figure><img src="../../.gitbook/assets/spaces_CdDIVDY6AtAz028MFT4d_uploads_LgAOVtxy9kQ0B8e2qaQl_image.webp" alt=""><figcaption><p>N-to-1 Retrieval </p></figcaption></figure>

Therefore, this mode's recall effectiveness can be impacted when there are too many datasets or when the knowledge descriptions lack sufficient distinction. This mode is more suitable for applications with fewer datasets.&#x20;

Tip: OpenAI Function Call already supports multiple tool calls, and Dify plans to upgrade this mode to "N-to-M retrieval" in future versions.

### Multi-path Retrieval

Based on user intent, this mode matches all datasets simultaneously, queries relevant text chunks from multiple datasets, and after a re-ranking step, selects the best results matching the user's question from the multi-path query results. Configuring the Rerank model API is required. In Multi-path retrieval mode, the search engine retrieves text content related to the user's query from all datasets associated with the application, merges the results from multi-path recall, and re-ranks the retrieved documents semantically using the Rerank model.

In Multi-path retrieval mode, configuring the Rerank model is necessary. How to configure the Rerank model: 🔗

Here is the technical flowchart for Multi-path retrieval:&#x20;

<figure><img src="../../.gitbook/assets/spaces_CdDIVDY6AtAz028MFT4d_uploads_xfMNnsyD506TOoynHdgU_image.webp" alt=""><figcaption><p>Multi-path retrieval</p></figcaption></figure>

As Multi-path retrieval does not rely on the model's inferencing capability or knowledge descriptions, this mode can achieve higher quality recall results in multi-knowledge searches. Additionally, incorporating the Rerank step can effectively improve document recall. Therefore, when creating a knowledge base Q\&A application associated with multiple datasets, we recommend configuring the retrieval mode as Multi-path retrieval.
