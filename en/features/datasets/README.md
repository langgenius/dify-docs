# Knowledge Import

Most language models use outdated training data and have length limitations for the context of each request. For example, GPT-3.5 is trained on corpora from 2021 and has a limit of approximately 4k tokens per request. This means that developers who want their AI applications to be based on the latest and private context conversations must use techniques like embedding.

Dify' knowledge feature allows developers (and even non-technical users) to easily manage knowledge and automatically integrate them into AI applications. All you need to do is prepare text content, such as:

* Long text content (TXT, Markdown, DOCX, HTML, JSONL, or even PDF files)
* Structured data (CSV, Excel, etc.)

Additionally, we are gradually supporting syncing data from various data sources to knowledge, including:

* GitHub
* Databases
* Webpages
* ...

{% hint style="info" %}
**Practice**: If your company wants to build an AI customer service assistant based on existing knowledge bases and product documentation, you can upload the documents to a knowledge base in Dify and create a conversational application. This might have taken you several weeks in the past and been difficult to maintain continuously.
{% endhint %}

### Knowledge and Documents

In Dify, knowledge bases are collections of documents. A knowledge base can be integrated as a whole into an application to be used as context. Documents can be uploaded by developers or operations staff, or synced from other data sources (typically corresponding to a file unit in the data source).

**Steps to upload a document:**

1. Upload your file, usually a long text file or a spreadsheet
2. Segment, clean, and preview
3. Dify submits it to the LLM provider for embedding as vector data and storage
4. Set metadata for the document
5. Ready to use in the application!

#### How to write a good knowledge description

When multiple knowledge bases are referenced in an application, AI uses the description of the knowledge and the user's question to determine which knowledge base to use to answer the user's question. Therefore, a well-written knowledge description can improve the accuracy of AI in selecting knowledge.

The key to writing a good knowledge description is to clearly describe the content and characteristics of the knowledge. **It is recommended that the knowledge description begin with this: `Useful only when the question you want to answer is about the following: specific description`**. Here is an example of a real estate knowledge description:

> Useful only when the question you want to answer is about the following: global real estate market data from 2010 to 2020. This data includes information such as the average housing price, property sales volume, and housing types for each city. In addition, this knowledge base also includes some economic indicators such as GDP and unemployment rate, as well as some social indicators such as population and education level. These indicators can help analyze the trends and influencing factors of the real estate market. With this data, we can understand the development trends of the global real estate market, analyze the changes in housing prices in various cities, and understand the impact of economic and social factors on the real estate market.

### Create a knowledge

1. Click on knowledge in the main navigation bar of Dify. On this page, you can see the existing knowledge bases. Click on "Create Knowledge" to enter the creation wizard.
2. If you have already prepared your files, you can start by uploading the files.
3. If you haven't prepared your documents yet, you can create an empty knowledge base first.

### Uploading Documents By upload file

1. Select the file you want to upload.We support batch uploads
2. Preview the full text
3. Perform segmentation and cleaning
4. Wait for Dify to process the data for you; this step usually consumes tokens in the LLM provider

### Text Preprocessing and Cleaning

Text Preprocessing and cleaning refers to Dify automatically segmenting and vectorizing your data documents so that user's questions (input) can match relevant paragraphs (Q to P), and generate results.

When uploading a knowledge base, you need to select a **indexing mode** to specify how data is matched. This affects the accuracy of AI replies.

In **High Quality mode**, OpenAI's embedding API is used for higher accuracy in user queries.

In **Economic mode**, offline vector engines, keyword indexing etc. are used to reduce costs at the expense of lower accuracy.

In **Segmenting in Question & Answer format**, instead of normal "Q to P" (question matches paragraphs), it uses "Q to Q" (question matches question) matching. After segmentation, Q\&A pairs are generated for each passage. When users ask questions, the system finds the most similar question and returns the corresponding passage as the answer. This is more precise because it directly matches the user's question and retrieves the information they need.

> Questions have complete syntax while keywords lack semantics and context. So Q to Q improves clarity and handles similar high-frequency questions better.

<figure><img src="../../.gitbook/assets/segment-list.png" alt=""><figcaption><p>In Segmenting in Question &#x26; Answer format, the text is summarized into multiple QA pairs</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (63).png" alt=""><figcaption><p>The difference between Q to P and Q to Q indexing modes</p></figcaption></figure>

### Modify Documents

Modify Documents For technical reasons, if developers make the following changes to documents, Dify will create a new document for you, and the old document will be archived and deactivated:

1. Adjust segmentation and cleaning settings
2. Re-upload the file

Dify support customizing the segmented and cleaned text by adding, deleting, and editing paragraphs. You can dynamically adjust your segmentation to make your knowledge more accurate. Click **Document --> paragraph --> Edit** in the knowledge to modify paragraphs content and custom keywords. Click **Document --> paragraph --> Add segment --> Add a segment** to manually add new paragraph. Or click **Document --> paragraph --> Add segment --> Batch add** to batch add new paragraph.

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1) (1).png" alt=""><figcaption><p>Edit</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption><p>add</p></figcaption></figure>

### Disabling and Archiving of Documents

* **Disable, cancel disable**: The knowledge supports disabling documents or chunks that you temporarily do not want indexed. In the knowledge's document list, click the Disable button and the document will be disabled. You can also click the Disable button in the document details to disable the entire document or a segment. Disabled documents will not be indexed. To cancel the disable, click Enable on a disabled document.
* **Archive, Unarchive:** Some unused old document data can be archived if you don't want to delete it. After archiving, the data can only be viewed or deleted, not edited. In the document list of the knowledge, click the Archive button to archive the document. Documents can also be archived in the document details page. Archived documents will not be indexed. Archived documents can also be unarchived by clicking the Unarchive button.

### Maintain Knowledge via API

Head to [maintain-dataset-via-api.md](maintain-dataset-via-api.md "mention").

### Knowledge Settings

Click **Settings** in the left navigation of the knowledge. You can change the following settings for the knowledge:

* Knowledge **name** for identifying a knowledge base
* Knowledge **description** to allow AI to better use the knowledge appropriately. If the description is empty, Dify's automatic indexing strategy will be used.
* **Permissions** can be set to Only Me or All Team Members. Those without permissions cannot view and edit the knowledge.
* **Indexing mode**: In High Quality mode, OpenAI's embedding interface will be called to process and provide higher accuracy when users query. In Economic mode, offline vector engines, keyword indexing, etc. will be used to reduce accuracy without consuming tokens.

Note: Upgrading the indexing mode from Economic to High Quality will incur additional token consumption. Downgrading from High Quality to Economic will not consume tokens.

### Integrate into Applications

Once the knowledge base is ready, it needs to be integrated into the application. When the AI application processes will automatically use the associated knowledge content as a reference context.

1. Go to the application - Prompt Arrangement page
2. In the context options, select the knowledge you want to integrate
3. Save the settings to complete the integration

### Q\&A

**Q: What should I do if the PDF upload is garbled?**

A: If your PDF parsing appears garbled under certain formatted contents, you could consider converting the PDF to Markdown format, which currently offers higher accuracy, or you could reduce the use of images, tables, and other formatted content in the PDF. We are researching ways to optimize the experience of using PDFs.

**Q: How does the consumption mechanism of context work?** A: With a knowledge base added, each query will consume segmented content (currently embedding two chunks) + question + prompt + chat history combined. However, it will not exceed model limitations, such as 4096.

**Q: Where does the embedded knowledge appear when asking questions?** A: It will be embedded as context before the question.

**Q: Is there any priority between the added knowledge and OpenAI's answers?** A: The knowledge serves as context and is used together with questions for LLM to understand and answer; there is no priority relationship.

**Q: Why can I hit in test but not in application?** A: You can troubleshoot issues by following these steps:

1. Make sure you have added text on the prompt page and clicked on the save button in the top right corner.
2. Test whether it responds normally in the prompt debugging interface.
3. Try again in a new WebApp session window.
4. Optimize your data format and quality. For practice reference, visit [https://github.com/langgenius/dify/issues/90](https://github.com/langgenius/dify/issues/90) If none of these steps solve your problem, please join our community for help.

**Q: Will APIs related to hit testing be opened up so that dify can access knowledge bases and implement dialogue generation using custom models?** A: We plan to open up Webhooks later on; however, there are no current plans for this feature. You can achieve your requirements by connecting to any vector database.

**Q: How do I add multiple knowledge bases?** A: Due to short-term performance considerations, we currently only support one knowledge base. If you have multiple sets of data, you can upload them within the same knowledge base for use.
