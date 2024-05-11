# Knowledge Retrieval

\
The Knowledge Base Retrieval Node is designed to query text content related to user questions from the Dify Knowledge Base, which can then be used as context for subsequent answers by the Large Language Model (LLM).

<figure><img src="../../../.gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

Configuring the Knowledge Base Retrieval Node involves three main steps:

1. **Selecting the Query Variable**
2. **Choosing the Knowledge Base for Query**
3. **Configuring the Retrieval Strategy**

**Selecting the Query Variable**

In knowledge base retrieval scenarios, the query variable typically represents the user's input question. In the "Start" node of conversational applications, the system pre-sets "sys.query" as the user input variable. This variable can be used to query the knowledge base for text segments most closely related to the user's question.

**Choosing the Knowledge Base for Query**

Within the knowledge base retrieval node, you can add an existing knowledge base from Dify. For instructions on creating a knowledge base within Dify, please refer to the knowledge base [help documentation](https://docs.dify.ai/features/datasets).

**Configuring the Retrieval Strategy**

It's possible to modify the indexing strategy and retrieval mode for an individual knowledge base within the node. For a detailed explanation of these settings, refer to the knowledge base [help documentation](https://docs.dify.ai/features/retrieval-augment/hybrid-search).

<figure><img src="../../../.gitbook/assets/image (49).png" alt=""><figcaption></figcaption></figure>

Dify offers two recall strategies for different knowledge base retrieval scenarios: "N-choose-1 Recall" and "Multi-way Recall". In the N-choose-1 mode, knowledge base queries are executed through function calling, requiring the selection of a system reasoning model. In the multi-way recall mode, a Rerank model needs to be configured for result re-ranking. For a detailed explanation of these two recall strategies, refer to the retrieval mode explanation in the [help documentation](https://docs.dify.ai/features/retrieval-augment/retrieval).

<figure><img src="../../../.gitbook/assets/image (51).png" alt=""><figcaption></figcaption></figure>
