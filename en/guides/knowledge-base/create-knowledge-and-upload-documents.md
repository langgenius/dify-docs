# Create Knowledge Base & Upload Documents

**Steps to upload documents into Knowledge:**

1. Select the document you need to upload from your local files;
2. Segment and clean the document, and preview the effect;
3. Choose and configure Index Mode and Retrieval Settings;
4. Wait for the chunks to be embedded;
5. Upload completed, now you can use it in your applications 🎉

### 1 Creating a Knowledge Base

Click on Knowledge in the main navigation bar of Dify. On this page, you can see your existing knowledge bases. Click **Create Knowledge** to enter the setup wizard:

* Drag and drop or select files to upload. The number of files allowed for batch upload depends on your [subscription plan](https://dify.ai/pricing);
* If you have not prepared any documents yet, you can first create an empty knowledge base;
*   When creating a knowledge base with an external data source (such as Notion or Sync from website), the knowledge base type becomes immutable. This restriction prevents management complexities that could arise from multiple data sources within a single knowledge base.

    For scenarios requiring multiple data sources, we recommend creating separate knowledge bases for each source. You can then utilize the [Multiple-Retrieval](integrate-knowledge-within-application.md) feature to reference multiple knowledge bases within the same application.

**Limitations for uploading documents:**

* The upload size limit for a single document is 15MB;
* Different [subscription plans](https://dify.ai/pricing) for the SaaS version limit **batch upload numbers, total document uploads, and vector storage**;

<figure><img src="../../../img/create-knowledge-base-2.png" alt=""><figcaption><p>Creating Knowledge Base</p></figcaption></figure>

***

### 2 Text Preprocessing and Cleaning

After uploading content to the knowledge base, it needs to undergo chunking and data cleaning. This stage can be understood as content preprocessing and structuring.

<details>

<summary>What is text chunking and cleaning?</summary>

**Chunking**: LLMs have a limited context window, usually requiring the entire text to be segmented and then recalling the most relevant segments to the user’s question, known as the segment TopK recall mode. Additionally, appropriate segment sizes help match the most relevant text content and reduce information noise when semantically matching user questions with text segments.

**Cleaning**: To ensure the quality of text recall, it is usually necessary to clean the data before passing it into the model. For example, unwanted characters or blank lines in the output may affect the quality of the response. To help users solve this problem, Dify provides various cleaning methods to help clean the output before sending it to downstream applications, check [ETL](create-knowledge-and-upload-documents.md#optional-etl-configuration) to know more details.

</details>

Two strategies are supported:

* Automatic mode
* Custom mode

{% tabs %}
{% tab title="Automatic" %}
#### Automatic

The Automated mode is designed for users unfamiliar with segmentation and preprocessing techniques. In this mode, Dify automatically segments and sanitizes content files, streamlining the document preparation process.

<figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption><p>Automatic mode</p></figcaption></figure>
{% endtab %}

{% tab title="Custom" %}
#### Custom

Custom mode is tailored for advanced users with specific text processing requirements. This mode allows manual configuration of chunking rules and cleaning strategies based on different document formats and scenario demands.

**Chunking Rules:**

1. **Delimiter**: Specify a delimiter for text segmentation. For example, `\n` (newline character in [regex](https://regexr.com/)) will chunk text at each line break.
2. **Maximum chunk length**: Set the maximum character count per segment. Chunk exceeding this limit will be forcibly divided. The maximum length for a segment is 4000 tokens.
3. **Chunk overlap**: Define the overlap between adjacent chunks. This overlap enhances information retention and analysis accuracy, improving recall effectiveness. Recommended setting is 10-25% of the segment length in tokens.

**Text Preprocessing Rules**: These rules help filter out insignificant content from the knowledge base.

* Replace consecutive spaces, newlines, and tabs.
* Delete all URLs and email addresses.

<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption><p>Custom mode</p></figcaption></figure>
{% endtab %}
{% endtabs %}

***

### 3 Indexing Mode

You need to choose the **indexing method** for the text to specify the data matching method. The indexing strategy is often related to the retrieval method, and you need to choose the appropriate [retrieval settings](create-knowledge-and-upload-documents.md#id-4-retrieval-settings) according to the scenario.

* **High-Quality Mode**
* **Economical Mode**
* **Q\&A Mode**

{% tabs %}
{% tab title="High Quality" %}
In High-Quality mode, the system first leverages an configurable Embedding model (which can be switched) to convert chunk text into numerical vectors. This process facilitates efficient compression and persistent storage of large-scale textual data, while simultaneously enhancing the accuracy of LLM-user interactions.

The High-Quality indexing method offers three retrieval settings: vector retrieval, full-text retrieval, and hybrid retrieval. For more details on retrieval settings, please check ["Retrieval Settings"](create-knowledge-and-upload-documents.md#id-4-retrieval-settings).

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption><p>High Quality</p></figcaption></figure>
{% endtab %}

{% tab title="Economical" %}
This mode employs an offline vector engine and keyword indexing, which reduces accuracy but eliminates additional token consumption and associated costs. The indexing method is limited to inverted indexing. For detailed specifications, please refer to the section below.

<figure><img src="../../.gitbook/assets/image (6).png" alt="" width="375"><figcaption><p>Economical mode</p></figcaption></figure>
{% endtab %}

{% tab title="Q&A Mode (community version only)" %}
When documents are uploaded to the knowledge base, the system segments the text and generates Q\&A pairs for each segment through summarization. Unlike the "Q to P" (Question to Paragraph) strategy employed in High-Quality and Economy modes, the QA mode adopts a "Q to Q" (Question to Question) approach.

This methodology is preferred **because question texts typically exhibit complete grammatical structures in natural language**. The Q to Q matching paradigm facilitates clearer chunk understanding and matching, while also accommodating scenarios involving high-frequency and highly similar queries.

Upon user inquiry, the system identifies the most semantically similar question and returns the corresponding text segment as the answer. This method offers enhanced precision as it directly matches against user queries, thereby more accurately retrieving the information users genuinely require.

<figure><img src="../../.gitbook/assets/guides/knowledge-base/Q&#x26;A-pair.png" alt=""><figcaption><p>Texts summarized into multiple Q&#x26;A pairs in Q&#x26;A segment mode</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/guides/knowledge-base/q2p-and-q2q.png" alt=""><figcaption><p>Difference between Q to P and Q to Q indexing modes</p></figcaption></figure>
{% endtab %}
{% endtabs %}

***

### 4 Retrieval Settings

In high-quality indexing mode, Dify offers three retrieval settings:

* **Vector Search**
* **Full-Text Search**
* **Hybrid Search**

{% tabs %}
{% tab title="Vector Search" %}
#### Vector Search

**Definition**: The system vectorizes the user's input query to generate a query vector. It then computes the distance between this query vector and the text vectors in the knowledge base to identify the most semantically proximate text chunks.

<figure><img src="../../.gitbook/assets/image (8).png" alt=""><figcaption><p>Vector Search Settings</p></figcaption></figure>

**Vector Search Settings：**

**Rerank Model**: After configuring the API key for the Rerank model on the "Model Provider" page, you can enable the “Rerank Model” in the retrieval settings. The system will then perform semantic reordering of the retrieved document results after hybrid retrieval, optimizing the ranking results. Once the Rerank model is established, the TopK and Score Threshold settings will only take effect during the reranking step.

**TopK**: This parameter filters the text chucks that are most similar to the user's question. The system dynamically adjusts the number of snippets based on the context window size of the selected model. The default value is 3, meaning a higher value results in more text segments being retrieved.

**Score Threshold**: This parameter sets the similarity threshold for filtering text chucks. Only text chucks that exceed the specified score will be recalled. By default, this setting is off, meaning there will be no filtering of similarity values for recalled text chucks. When enabled, the default value is 0.5. A higher value is likely to yield fewer recalled texts.

> The TopK and Score configurations are only effective during the Rerank phase. Therefore, to apply either of these settings, it is necessary to add and enable a Rerank model.
{% endtab %}

{% tab title="Full-Text Search" %}
#### Full-Text Search

**Definition:** Indexing all terms in the document, allowing users to query any terms and return text fragments containing those terms.

<figure><img src="../../.gitbook/assets/guides/knowledge-base/full-text-search.png" alt="" width="563"><figcaption><p>Full-Text Search Settings</p></figcaption></figure>

**Rerank Model**: After configuring the API key for the Rerank model on the "Model Provider" page, you can enable the “Rerank Model” in the retrieval settings. The system will then perform semantic reordering of the retrieved document results after hybrid retrieval, optimizing the ranking results. Once the Rerank model is established, the TopK and Score Threshold settings will only take effect during the reranking step.

**TopK**: This parameter filters the text chucks that are most similar to the user's question. The system dynamically adjusts the number of snippets based on the context window size of the selected model. The default value is 3, meaning a higher value results in more text segments being retrieved.

**Score Threshold**: This parameter sets the similarity threshold for filtering text chucks. Only text chucks that exceed the specified score will be recalled. By default, this setting is off, meaning there will be no filtering of similarity values for recalled text chucks. When enabled, the default value is 0.5. A higher value is likely to yield fewer recalled texts.

> The TopK and Score configurations are only effective during the Rerank phase. Therefore, to apply either of these settings, it is necessary to add and enable a Rerank model.
{% endtab %}

{% tab title="Hybrid Search" %}
#### **Hybrid Search**

**Definition:** This process performs both full-text search and vector search simultaneously, incorporating a reordering step to select the best results that match the user's query from both types of search outcomes. In this mode, users can specify "weight settings" without needing to configure the Rerank model API, or they can opt for a Rerank model for retrieval.

<figure><img src="../../../img/hybrid-search.png" alt="" width="563"><figcaption><p>Hybrid Retrieval Setting</p></figcaption></figure>

**Weight Settings:** This feature enables users to set custom weights for semantic priority and keyword priority. Keyword search refers to performing a full-text search within the knowledge base, while semantic search involves vector search within the knowledge base.

* **Semantic Value of 1**

This activates only the semantic search mode. Utilizing embedding models, even if the exact terms from the query do not appear in the knowledge base, the search can delve deeper by calculating vector distances, thus returning relevant content. Additionally, when dealing with multilingual content, semantic search can capture meaning across different languages, providing more accurate cross-language search results.

* **Keyword Value of 1**

This activates only the keyword search mode. It performs a full match against the input text in the knowledge base, suitable for scenarios where the user knows the exact information or terminology. This approach consumes fewer computational resources and is ideal for quick searches within a large document knowledge base.

* **Custom Keyword and Semantic Weights**

In addition to enabling only semantic search or keyword search, we provide flexible custom weight settings. You can continuously adjust the weights of the two methods to identify the optimal weight ratio that suits your business scenario.

***

**Rerank Model**: After configuring the API key for the Rerank model on the "Model Provider" page, you can enable the “Rerank Model” in the retrieval settings. The system will then perform semantic reordering of the retrieved document results after hybrid retrieval, optimizing the ranking results. Once the Rerank model is established, the TopK and Score Threshold settings will only take effect during the reranking step.

***

The **"Weight Settings"** and **"Rerank Model"** settings support the following options:

**TopK**: This parameter filters the text chucks that are most similar to the user's question. The system dynamically adjusts the number of snippets based on the context window size of the selected model. The default value is 3, meaning a higher value results in more text segments being retrieved.

**Score Threshold**: This parameter sets the similarity threshold for filtering text chucks. Only text chucks that exceed the specified score will be recalled. By default, this setting is off, meaning there will be no filtering of similarity values for recalled text chucks. When enabled, the default value is 0.5. A higher value is likely to yield fewer recalled texts.
{% endtab %}
{% endtabs %}

In the **Economical indexing** mode, Dify offers a single retrieval setting:

#### Inverted Index:

An inverted index is an index structure designed for rapid keyword retrieval in documents. Its fundamental principle involves mapping keywords from documents to lists of documents containing those keywords, thereby enhancing search efficiency. For a detailed explanation of the underlying mechanism, please refer to the ["Inverted Index"](https://en.wikipedia.org/wiki/Inverted\_index).

**TopK：**

This parameter filters the text chucks that are most similar to the user's question. The system dynamically adjusts the number of snippets based on the context window size of the selected model. The default value is 3, meaning a higher value results in more text segments being retrieved.

<figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption><p>Inverted Index</p></figcaption></figure>

***

### Reference

#### Optional ETL Configuration

In production-level applications of RAG, to achieve better data recall, multi-source data needs to be preprocessed and cleaned, i.e., ETL (extract, transform, load). To enhance the preprocessing capabilities of unstructured/semi-structured data, Dify supports optional ETL solutions: **Dify ETL** and [**Unstructured ETL**](https://unstructured.io/).

> Unstructured can efficiently extract and transform your data into clean data for subsequent steps.

ETL solution choices in different versions of Dify:

* The SaaS version defaults to using Unstructured ETL and cannot be changed;
* The community version defaults to using Dify ETL but can enable Unstructured ETL through [environment variables](../../getting-started/install-self-hosted/environments.md#zhi-shi-ku-pei-zhi);

Differences in supported file formats for parsing:

| DIFY ETL                                                | Unstructured ETL                                                                        |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| txt, markdown, md, pdf, html, htm, xlsx, xls, docx, csv | txt, markdown, md, pdf, html, htm, xlsx, xls, docx, csv, eml, msg, pptx, ppt, xml, epub |

{% hint style="info" %}
Different ETL solutions may have differences in file extraction effects. For more information on Unstructured ETL’s data processing methods, please refer to the [official documentation](https://docs.unstructured.io/open-source/core-functionality/partitioning).
{% endhint %}

#### Embedding Model

**Embedding** transforms discrete variables (words, sentences, documents) into continuous vector representations, mapping high-dimensional data to lower-dimensional spaces. This technique preserves crucial semantic information while reducing dimensionality, enhancing content retrieval efficiency.

**Embedding models**, specialized large language models, excel at converting text into dense numerical vectors, effectively capturing semantic nuances for improved data processing and analysis.

