# RAG (Retrieval Augmented Generation)

## The concept of the RAG

The RAG architecture, with vector retrieval at its core, has become the leading technological framework for addressing two major challenges of large models: acquiring the latest external knowledge and mitigating issues of generating hallucinations. This architecture has been widely implemented in numerous practical application scenarios.

Developers can utilize this technology to cost-effectively build AI-powered customer service bots, corporate knowledge bases, AI search engines, etc. These systems interact with various forms of organized knowledge through natural language input. A representative example of a RAG application is as follows:

In the diagram below, when a user asks, "Who is the President of the United States?", the system doesn't directly relay the question to the large model for an answer. Instead, it first conducts a vector search in a knowledge base (like Wikipedia, as shown in the diagram) for the user's query. It finds relevant content through semantic similarity matching (for instance, "Biden is the current 46th President of the United States…"), and then provides the user's question along with the found knowledge to the large model. This enables the model to have sufficient and complete knowledge to answer the question, thereby yielding a more reliable response.

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1).png" alt=""><figcaption><p>Basic Architecture of RAG</p></figcaption></figure>

## Why is this necessary?

We can liken a large model to a super-expert, knowledgeable in various human domains. However, this expert has its limitations; for example, it doesn't know your personal situation, as such information is private and not publicly available on the internet, and therefore, it hasn't had the opportunity to learn it beforehand.

When you want to hire this super-expert as your family financial advisor, you need to allow them to review your investment records, household expenses, and other relevant data before they can respond to your inquiries. This enables them to provide professional advice tailored to your personal circumstances.

**This is what the RAG system does: it helps the large model temporarily acquire external knowledge it doesn't possess, allowing it to search for answers before responding to a question.**

Based on this example, it's evident that the most critical aspect of the RAG system is the retrieval of external knowledge. The expert's ability to provide professional financial advice depends on accurately finding the necessary information. If the expert retrieves information unrelated to financial investments, like a family weight loss plan, even the most capable expert would be ineffective.
