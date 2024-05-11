# LLM

Invoking a Large Language Model for Question Answering or Natural Language Processing. Within an LLM node, you can select an appropriate model, compose prompts, set the context referenced in the prompts, configure memory settings, and adjust the memory window size.

<figure><img src="../../../.gitbook/assets/image (9) (1).png" alt=""><figcaption></figcaption></figure>

Configuring an LLM node primarily involves two steps:

1. Selecting a model
2. Composing system prompts

**Model Configuration**&#x20;

Before selecting a model suitable for your task, you must complete the model configuration in "System Settings—Model Provider". The specific configuration method can be referenced in the [model configuration instructions](https://docs.dify.ai/tutorials/model-configuration#model-integration-settings). After selecting a model, you can configure its parameters.

<figure><img src="../../../.gitbook/assets/image (10) (1).png" alt=""><figcaption></figcaption></figure>

**Write Prompts**

Within an LLM node, you can customize the model input prompts. If you choose a conversational model, you can customize the content of system prompts, user messages, and assistant messages.&#x20;

For instance, in a knowledge base Q\&A scenario, after linking the "Result" variable from the knowledge base retrieval node in "Context", inserting the "Context" special variable in the prompts will use the text retrieved from the knowledge base as the context background information for the model input.

<figure><img src="../../../.gitbook/assets/image (12) (1).png" alt=""><figcaption></figcaption></figure>

In the prompt editor, you can bring up the variable insertion menu by typing "/" or "{" to insert special variable blocks or variables from preceding flow nodes into the prompts as context content.

<figure><img src="../../../.gitbook/assets/image (13) (1).png" alt="" width="375"><figcaption></figcaption></figure>

If you opt for a completion model, the system provides preset prompt templates for conversational applications. You can customize the content of the prompts and insert special variable blocks like "Conversation History" and "Context" at appropriate positions by typing "/" or "{", enabling richer conversational functionalities.

<figure><img src="../../../.gitbook/assets/image (14) (1).png" alt=""><figcaption></figcaption></figure>

**Memory Toggle Settings**&#x20;

In conversational applications (Chatflow), the LLM node defaults to enabling system memory settings. In multi-turn dialogues, the system stores historical dialogue messages and passes them into the model. In workflow applications (Workflow), system memory is turned off by default, and no memory setting options are provided.

**Memory Window Settings**&#x20;

If the memory window setting is off, the system dynamically passes historical dialogue messages according to the model's context window. With the memory window setting on, you can configure the number of historical dialogue messages to pass based on your needs.

**Dialogue Role Name Settings**&#x20;

Due to differences in model training phases, different models adhere to role name commands to varying degrees, such as Human/Assistant, Human/AI, 人类/助手, etc. To adapt to the prompt response effects of multiple models, the system allows setting dialogue role names, modifying the role prefix in conversation history.
