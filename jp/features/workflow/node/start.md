# Start

Defining initial parameters for a workflow process initiation allows for customization at the start node, where you input variables to kick-start the workflow. Every workflow necessitates a start node, acting as the entry point and foundation for the workflow's execution path.

<figure><img src="../../../.gitbook/assets/image (20).png" alt=""><figcaption></figcaption></figure>

Within the "Start" node, you can define input variables of four types:

* **Text**: For short, simple text inputs like names, identifiers, or any other concise data.
* **Paragraph**: Supports longer text entries, suitable for descriptions, detailed queries, or any extensive textual data.
* **Dropdown Options**: Allows the selection from a predefined list of options, enabling users to choose from a set of predetermined values.
* **Number**: For numeric inputs, whether integers or decimals, to be used in calculations, quantities, identifiers, etc.

<figure><img src="../../../.gitbook/assets/image (24).png" alt=""><figcaption></figcaption></figure>

Once the configuration is completed, the workflow's execution will prompt for the values of the variables defined in the start node. This step ensures that the workflow has all the necessary information to proceed with its designated processes.

<figure><img src="../../../.gitbook/assets/image (37).png" alt=""><figcaption></figcaption></figure>

**Tip:** In Chatflow, the start node provides system-built variables: `sys.query` and `sys.files`. `sys.query` is utilized for user question input in conversational applications, enabling the system to process and respond to user queries. `sys.files` is used for file uploads within the conversation, such as uploading an image to understand its content. This requires the integration of image understanding models or tools designed for processing image inputs, allowing the workflow to interpret and act upon the uploaded files effectively.
