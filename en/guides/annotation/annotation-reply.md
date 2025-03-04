# Annotation Reply

The annotated replies feature provides customizable high-quality question-and-answer responses through manual editing and annotation.

Applicable scenarios:

* **Customized Responses for Specific Fields:** In customer service or knowledge base scenarios for enterprises, government, etc., service providers may want to ensure that certain specific questions are answered with definitive results. Therefore, it is necessary to customize the output for specific questions. For example, creating "standard answers" for certain questions or marking some questions as "unanswerable."
* **Rapid Tuning for POC or DEMO Products:** When quickly building prototype products, customized responses achieved through annotated replies can efficiently enhance the expected generation of Q\&A results, thereby improving customer satisfaction.

The annotated replies feature essentially provides another set of retrieval-enhanced systems, allowing you to bypass the LLM generation phase and avoid the hallucination issues of RAG.

### Workflow

1. After enabling the annotated replies feature, you can annotate the responses from LLM conversations. You can add high-quality answers from LLM responses directly as annotations or edit a high-quality answer according to your needs. These edited annotations will be saved persistently.
2. When a user asks a similar question again, the system will vectorize the question and search for similar annotated questions.
3. If a match is found, the corresponding answer from the annotation will be returned directly, bypassing the LLM or RAG process.
4. If no match is found, the question will continue through the regular process (passing to LLM or RAG).
5. Once the annotated replies feature is disabled, the system will no longer match responses from annotations.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/392c0d2847ce07c31d054f32c1103e4d.webp" alt="" width="563"><figcaption><p>Annotated Replies Workflow</p></figcaption></figure>

### Enabling Annotated Replies in Prompt Orchestration

Enable the annotated replies switch by navigating to **“Orchestrate -> Add Features”**:

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/11d3c1b21e275834befd34df0d74bfd0.webp" alt=""><figcaption><p>Enabling Annotated Replies in Prompt Orchestration</p></figcaption></figure>

When enabling, you need to set the parameters for annotated replies, which include: Score Threshold and Embedding Model.

**Score Threshold:** This sets the similarity threshold for matching annotated replies. Only annotations with scores above this threshold will be recalled.

**Embedding Model:** This is used to vectorize the annotated text. Changing the model will regenerate the embeddings.

Click save and enable, and the settings will take effect immediately. The system will generate embeddings for all saved annotations using the embedding model.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/483f9e6e1b8a222868ac32e9b0b12350.webp" alt=""><figcaption><p>Setting Parameters for Annotated Replies</p></figcaption></figure>

### Adding Annotations in the Conversation Debug Page

You can directly add or edit annotations on the model response information in the debug and preview pages.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/c753c1e2babd3cd4e40f349c53d03390.webp" alt=""><figcaption><p>Adding Annotated Replies</p></figcaption></figure>

Edit the response to the high-quality reply you need and save it.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/1cb0f1a4819287ca89c8e6ce3b56bbff.webp" alt=""><figcaption><p>Editing Annotated Replies</p></figcaption></figure>

Re-enter the same user question, and the system will use the saved annotation to reply to the user's question directly.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/6350513833017c827660c273cd3dcdba.webp" alt=""><figcaption><p>Replying to User Questions with Saved Annotations</p></figcaption></figure>

### Enabling Annotated Replies in Logs and Annotations

Enable the annotated replies switch by navigating to “Logs & Ann. -> Annotations”:

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/07c57ea858385985fa83ac30289cc138.webp" alt=""><figcaption><p>Enabling Annotated Replies in Logs and Annotations</p></figcaption></figure>

### Setting Parameters for Annotated Replies in the Annotation Backend

The parameters that can be set for annotated replies include: Score Threshold and Embedding Model.

**Score Threshold:** This sets the similarity threshold for matching annotated replies. Only annotations with scores above this threshold will be recalled.

**Embedding Model:** This is used to vectorize the annotated text. Changing the model will regenerate the embeddings.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/2eef1ac7dfeae549201c9e5e6ebbcdba.webp" alt=""><figcaption><p>Setting Parameters for Annotated Replies</p></figcaption></figure>

### Bulk Import of Annotated Q\&A Pairs

In the bulk import feature, you can download the annotation import template, edit the annotated Q\&A pairs according to the template format, and then import them in bulk.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/a362886fc1f3f1e05fc0386950bb5a0f.webp" alt=""><figcaption><p>Bulk Import of Annotated Q&A Pairs</p></figcaption></figure>

### Bulk Export of Annotated Q\&A Pairs

Through the bulk export feature, you can export all saved annotated Q\&A pairs in the system at once.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/2bd8b91e75d8754d944095d76e295508.webp" alt=""><figcaption><p>Bulk Export of Annotated Q&A Pairs</p></figcaption></figure>

### Viewing Annotation Hit History

In the annotation hit history feature, you can view the edit history of all hits on the annotation, the user's hit questions, the response answers, the source of the hits, the matching similarity scores, the hit time, and other information. You can use this information to continuously improve your annotated content.

<figure><img src="https://assets-docs.dify.ai//img/en/annotation/5b04cde5481067b07edbda3083fa9c8b.webp" alt=""><figcaption><p>Viewing Annotation Hit History</p></figcaption></figure>
