# Integrating Knowledge Base within the Application

### 1. Creating a Knowledge Base Application

A knowledge base can be used as external knowledge to provide precise answers to user questions through a large language model. You can associate an existing knowledge base with any application type in Dify.

Taking a chat assistant as an example, the process is as follows:

1. Go to **Studio -- Create Application -- Create Chat Assistant**
2. Enter **Context Settings**, click **Add**, and select the already created knowledge base
3. In **Context Settings -- Parameter Settings**, configure the **Recall Strategy**
4. Enable **Citation and Attribution** in **Add Features**
5. In **Debug and Preview**, input user questions related to the knowledge base for debugging
6. After debugging, **Save and Publish** as an AI knowledge base Q&A application

***

### Connecting Knowledge Bases and Specifying Recall Modes

In applications that utilize multiple knowledge bases, it is essential to configure the recall mode to enhance the precision of retrieved content. To set the recall mode for the knowledge bases, go to **Context -- Parameter Settings -- Recall Settings**.

#### N-to-1 Recall (Legacy)

The N-to-1 recall method operates through Function Call/ReAct, where each linked knowledge base serves as a functional tool. The LLM autonomously selects the most relevant knowledge base that aligns with the user's query for the search, based on the **semantic similarity between the user's question and the knowledge base description**.

The following diagram illustrates this principle:

<figure><img src="../../../zh_CN/.gitbook/assets/image (190).png" alt=""><figcaption></figcaption></figure>

For instance, in application A, if there are three associated knowledge bases K1, K2, and K3, when a user submits a question, the LLM will evaluate the descriptions of these knowledge bases, identify the best match, and utilize that content for the search.

![](../../../img/en-n-to-1.png)

Although this method does not require the configuration of a [Rerank](https://docs.dify.ai/learn-more/extended-reading/retrieval-augment/rerank) model, it only identifies one knowledge base. The effectiveness of this retrieval strategy relies heavily on the LLM's interpretation of the knowledge base description. This may lead to suboptimal judgments during the retrieval process, potentially resulting in incomplete or inaccurate answers, thereby impacting the quality of query outcomes.

Starting in September, this approach will be automatically transitioned to **multi-route recall**, so please prepare accordingly.

In N-to-1 mode, the effectiveness of retrieval is influenced by three primary factors:

* **The capability of the system inference model** Some models may inconsistently follow Function Call/ReAct instructions.
* **Clarity of the knowledge base description** A clear description significantly affects the LLM's reasoning regarding the user's question and the relevant knowledge bases.
* **The number of knowledge bases** An excessive number of knowledge bases can impair the accuracy of the LLM's reasoning and may exceed the context window limit of the inference model.

**Strategies to enhance retrieval effectiveness in N-to-1 mode:**

- Opt for a more effective system inference model, limit the number of associated knowledge bases, and provide clear descriptions for each knowledge base.

- When uploading content to a knowledge base, the system inference model will automatically generate a summary description. To achieve the best retrieval results in this mode, review the system-generated summary in “Knowledge Base -> Settings -> Knowledge Base Description” to ensure it effectively summarizes the content of the knowledge base.

#### Multi-route Recall (Recommended)

In the multi-route recall mode, the retriever scans all knowledge bases linked to the application for text content relevant to the user's question. The results are then consolidated. Below is the technical flowchart for the multi-route recall mode:

<figure><img src="../../../img/rerank-flow-chart.png" alt=""><figcaption></figcaption></figure>

This method simultaneously queries all knowledge bases listed in **"Context"**, seeking relevant text snippets across multiple knowledge bases, collecting all content that aligns with the user's question, and ultimately applying the Rerank strategy to identify the most appropriate content to respond to the user. This retrieval approach is more scientifically robust.

<figure><img src="../../../img/en-rag-multiple.png" alt=""><figcaption></figcaption></figure>

For example, in application A, with three knowledge bases K1, K2, and K3, when a user poses a question, multiple relevant pieces of content will be retrieved and combined from these knowledge bases. To ensure the most pertinent content is identified, the Rerank strategy is employed to find the content that best relates to the user's query, enhancing the precision and reliability of the results.

In practical Q&A scenarios, the sources of content and retrieval methods for each knowledge base may differ. To manage the mixed content returned from retrieval, the [Rerank strategy](https://docs.dify.ai/learn-more/extended-reading/retrieval-augment/rerank) acts as a refined sorting mechanism. It ensures that the candidate content aligns well with the user's question, optimizing the ranking of results across multiple knowledge bases to identify the most suitable content, thereby improving answer quality and overall user experience.

Considering the costs associated with using Rerank and the needs of the business, the multi-recall mode provides two Rerank settings:

##### Weight Settings

This setting does not require the configuration of an external Rerank model, meaning that reordering content incurs **no extra costs**. You can select the most appropriate content matching strategy by adjusting the weight ratio sliders for semantics or keywords.

- **Semantic Value of 1**

  This mode activates semantic retrieval only. By utilizing the Embedding model, the search depth can be enhanced even if the exact words from the query do not appear in the knowledge base, as it calculates vector distances to return the relevant content. Furthermore, when dealing with multilingual content, semantic retrieval can capture meanings across different languages, yielding more accurate cross-language search results.

- **Keyword Value of 1**

  This mode activates keyword retrieval only. It matches the user's input text against the full text of the knowledge base, making it ideal for scenarios where the user knows the exact information or terminology. This method is resource-efficient, making it suitable for quickly retrieving information from large document repositories.

- **Custom Keyword and Semantic Weights**

  In addition to enabling only semantic or keyword retrieval modes, we offer flexible custom weight settings. You can determine the best weight ratio for your business scenario by continuously adjusting the weights of both.

##### Rerank Model

The Rerank model is an external scoring system that calculates the relevance score between the user's question and each candidate document provided, improving the results of semantic ranking and returning a list of documents sorted by relevance from high to low.

While this method incurs some additional costs, it is more adept at handling complex knowledge base content, such as content that combines semantic queries and keyword matches, or cases involving multilingual returned content.

Click here to learn more about the [reordering](https://docs.dify.ai/learn-more/extended-reading/retrieval-augment/rerank) mechanism.

Dify currently supports multiple Rerank models. Enter the API Key for the Rerank model (such as Cohere, Jina, etc.) on the "Model Provider" page.

<figure><img src="../../../img/en-rerank-model-api.png" alt=""><figcaption><p>Configuring the Rerank model in the Model Provider</p></figcaption></figure>

##### Adjustable Parameters

- **TopK**

  This parameter filters the text segments that are most similar to the user's question. The system dynamically adjusts the number of segments based on the context window size of the selected model. A higher value results in more text segments being recalled.

- **Score Threshold**

  This parameter establishes the similarity threshold for filtering text segments. Only those segments with a vector retrieval similarity score exceeding the set threshold will be recalled. A higher threshold value results in fewer texts being recalled.

The multi-recall mode can achieve higher quality recall results when retrieving from multiple knowledge bases; therefore, it is **recommended to set the recall mode to multi-recall**.

### Frequently Asked Questions

1. **How should I choose Rerank settings in multi-recall mode?**

If users know the exact information or terminology, and keyword retrieval can accurately deliver matching results, it is advised to use the **keyword priority mode** in the "Weight Settings".

If the exact vocabulary does not appear in the knowledge base, or if there are cross-language queries, it is recommended to use the **semantic priority** mode in the "Weight Settings".

If business personnel are familiar with the actual questioning scenarios of users and wish to actively adjust the ratio of semantics or keywords, it is advisable to use the **custom mode** in the "Weight Settings".

If the content in the knowledge base is complex and cannot be matched by simple conditions such as semantics or keywords, while requiring precise answers, and if you are willing to incur additional costs, it is recommended to utilize the **Rerank model** for content retrieval.

2. **What should I do if I encounter issues finding the “Weight Settings” or the requirement to configure a Rerank model?**

Here’s how the retrieval method of the knowledge base affects multi-recall:

| Knowledge Base Index Mode | Knowledge Base Retrieval Settings | Embedding Model | Multi-recall Page Prompt | Reason |
| --- | --- | --- | --- | --- |
| Economy Type | Inverted Index | None | Weight configuration unavailable, Rerank model can be enabled | - |
| High Quality Type | 1. All knowledge bases use vector retrieval | Same Embedding model | Defaults to "Weight Settings," semantic value of 1 | Rerank settings align with knowledge base retrieval settings
| High Quality Type | 2. All knowledge bases use full-text retrieval | Same Embedding model | Defaults to "Weight Settings," keyword value of 1 | Rerank settings align with knowledge base retrieval settings |
| High Quality Type | 3. A mix of both | Same Embedding model | Defaults to "Weight Settings" custom configuration, ratio of semantic:keyword = 0.7:0.3 | Knowledge base content combines semantics and keywords, allowing customization of weight settings |
| Both Economy and High Quality | Different retrieval settings used | Different Embedding models | Rerank model needs to be enabled | Content sources are complex; enabling Rerank model is recommended to ensure quality of content return |
| High Quality | Same/different retrieval settings used | Different Embedding models | Rerank model needs to be enabled | ontent sources are not uniform, making it impossible to sort by the same standard. Configuring the Rerank model is necessary to enhance retrieval accuracy. |

3. **What should I do if I cannot adjust the “Weight Settings” when referencing multiple knowledge bases and an error message appears?**

This issue occurs because the embedding models used in the multiple referenced knowledge bases are inconsistent, prompting this notification to avoid conflicts in retrieval content. It is advisable to set and enable the Rerank model in the "Model Provider" or unify the retrieval settings of the knowledge bases.

4. **Why can't I find the “Weight Settings” option in multi-recall mode, and only see the Rerank model?**

Please check whether your knowledge base is using the “Economy” index mode. If so, switch it to the “High Quality” index mode.
