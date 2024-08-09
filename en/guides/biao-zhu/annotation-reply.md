# Annotated Replies

The annotated replies feature provides customizable high-quality question-and-answer responses through manual editing and annotation.

Applicable scenarios:

* **Customized Responses for Specific Fields:** In customer service or knowledge base scenarios for enterprises, government, etc., service providers may want to ensure that certain specific questions are answered with definitive results. Therefore, it is necessary to customize the output for specific questions. For example, creating "standard answers" for certain questions or marking some questions as "unanswerable."
* **Rapid Tuning for POC or DEMO Products:** When quickly building prototype products, customized responses achieved through annotated replies can efficiently enhance the expected generation of Q&A results, thereby improving customer satisfaction.

The annotated replies feature essentially provides another set of retrieval-enhanced systems, allowing you to bypass the LLM generation phase and avoid the hallucination issues of RAG.

### Workflow

1. After enabling the annotated replies feature, you can annotate the responses from LLM conversations. You can add high-quality answers from LLM responses directly as annotations or edit a high-quality answer according to your needs. These edited annotations will be saved persistently.
2. When a user asks a similar question again, the system will vectorize the question and search for similar annotated questions.
3. If a match is found, the corresponding answer from the annotation will be returned directly, bypassing the LLM or RAG process.
4. If no match is found, the question will continue through the regular process (passing to LLM or RAG).
5. Once the annotated replies feature is disabled, the system will no longer match responses from annotations.

<figure><img src="/en/.gitbook/assets/guides/biao-zhu/annotation-reply/image (130).png" alt="" width="563"><figcaption><p>Annotated Replies Workflow</p></figcaption></figure>

### Enabling Annotated Replies in Prompt Orchestration

Enable the annotated replies switch by navigating to **“Orchestrate -> Add Features”**:

<figure><img src="../../../img/annotated-replies.png" alt=""><figcaption><p>Enabling Annotated Replies in Prompt Orchestration</p></figcaption></figure>

When enabling, you need to set the parameters for annotated replies, which include: Score Threshold and Embedding Model.

**Score Threshold:** This sets the similarity threshold for matching annotated replies. Only annotations with scores above this threshold will be recalled.

**Embedding Model:** This is used to vectorize the annotated text. Changing the model will regenerate the embeddings.

Click save and enable, and the settings will take effect immediately. The system will generate embeddings for all saved annotations using the embedding model.

<figure><img src="../../../img/setting-parameters-for-annotated-replies.png" alt=""><figcaption><p>Setting Parameters for Annotated Replies</p></figcaption></figure>

### Adding Annotations in the Conversation Debug Page

You can directly add or edit annotations on the model response information in the debug and preview pages.

<figure><img src="../../../img/add-annotation-reply.png" alt=""><figcaption><p>Adding Annotated Replies</p></figcaption></figure>

Edit the response to the high-quality reply you need and save it.

<figure><img src="../../../img/editing-annotated-replies.png" alt=""><figcaption><p>Editing Annotated Replies</p></figcaption></figure>

Re-enter the same user question, and the system will use the saved annotation to reply to the user's question directly.

<figure><img src="../../../img/annotaiton-reply.png" alt=""><figcaption><p>Replying to User Questions with Saved Annotations</p></figcaption></figure>

### Enabling Annotated Replies in Logs and Annotations

Enable the annotated replies switch by navigating to “Logs & Ann. -> Annotations”:

<figure><img src="../../../img/logs-annotation-switch.png" alt=""><figcaption><p>Enabling Annotated Replies in Logs and Annotations</p></figcaption></figure>

### Setting Parameters for Annotated Replies in the Annotation Backend

The parameters that can be set for annotated replies include: Score Threshold and Embedding Model.

**Score Threshold:** This sets the similarity threshold for matching annotated replies. Only annotations with scores above this threshold will be recalled.

**Embedding Model:** This is used to vectorize the annotated text. Changing the model will regenerate the embeddings.

<figure><img src="../../../img/annotated-replies-initial.png" alt=""><figcaption><p>Setting Parameters for Annotated Replies</p></figcaption></figure>

### Bulk Import of Annotated Q&A Pairs

In the bulk import feature, you can download the annotation import template, edit the annotated Q&A pairs according to the template format, and then import them in bulk.

<figure><img src="../../../img/bulk-import-annotated.png" alt=""><figcaption><p>Bulk Import of Annotated Q&A Pairs</p></figcaption></figure>

### Bulk Export of Annotated Q&A Pairs

Through the bulk export feature, you can export all saved annotated Q&A pairs in the system at once.

<figure><img src="../../../img/bulk-export-annotations.png" alt=""><figcaption><p>Bulk Export of Annotated Q&A Pairs</p></figcaption></figure>

### Viewing Annotation Hit History

In the annotation hit history feature, you can view the edit history of all hits on the annotation, the user's hit questions, the response answers, the source of the hits, the matching similarity scores, the hit time, and other information. You can use this information to continuously improve your annotated content.

<figure><img src="../../../img/view-annotation-hit-history.png" alt=""><figcaption><p>Viewing Annotation Hit History</p></figcaption></figure>
