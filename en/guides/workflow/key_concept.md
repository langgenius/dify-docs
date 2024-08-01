# Key Concepts

### Nodes

**Nodes are the key components of a workflow**. By connecting nodes with different functionalities, you can execute a series of operations within the workflow.

For core workflow nodes, please refer to [Node Description](node/).

***

### Variables

**Variables are used to link the input and output of nodes within a workflow**, enabling complex processing logic throughout the process.

![](../../../img/en-variables.png)

* A workflow needs to define execution start variables, such as defining an input variable `sys.query` for a chatbot.
* Nodes generally need to define input variables, such as defining the input variable for a question classifier as `sys.query`.
* When referencing variables, only upstream node variables in the process can be referenced.
* To avoid variable name conflicts, node names must be unique.
* The output variables of nodes are generally system-fixed variables and cannot be edited.

***

### Environment Variables

**Environment variables are used to protect sensitive information involved in workflows**, such as API keys and database passwords used when running workflows. They are stored in the workflow rather than in the code, allowing them to be shared across different environments.

![](../../../img/en-env-variable.png)

Supports the following 3 data types:

- String
- Number
- Secret

Environmental variables have the following characteristics:

- Environment variables can be globally referenced within most nodes;
- Environment variable names cannot be duplicated;
- Output variables of nodes are generally read-only and cannot be written to.

***

### Chatflow and Workflow

**Application Scenarios**

* **Chatflow**: Designed for conversational scenarios, including customer service, semantic search, and other conversational applications that require multi-step logic in response construction.
* **Workflow**: Geared towards automation and batch processing scenarios, suitable for high-quality translation, data analysis, content generation, email automation, and more.

**Usage Entry Points**

<figure><img src="/en/.gitbook/assets/guides/workflow/key-concepts/output.png" alt=""><figcaption><p>Chatflow Entry</p></figcaption></figure>

<figure><img src="/en/.gitbook/assets/guides/workflow/key-concepts/output (4).png" alt=""><figcaption><p>Workflow Entry</p></figcaption></figure>

**Differences in Available Nodes**

1. The End node is an ending node for Workflow and can only be selected at the end of the process.
2. The Answer node is specific to Chatflow, used for streaming text output, and can output at intermediate steps in the process.
3. Chatflow has built-in chat memory (Memory) for storing and passing multi-turn conversation history, which can be enabled in nodes like LLM and question classifiers. Workflow does not have Memory-related configurations and cannot enable them.
4. Built-in variables for Chatflow's start node include: `sys.query`, `sys.files`, `sys.conversation_id`, `sys.user_id`. Built-in variables for Workflow's start node include: `sys.files`, `sys_id`.