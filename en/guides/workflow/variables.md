# Variables

**Workflow** and **Chatflow** Application are composed of independent nodes. Most nodes have input and output items, but the input and output information for each node is not consistent and dynamic.

**How to use a fixed symbol to refer dynamically changing content?**  Variables, as dynamic data containers, can store and transmit unfixed content, being referenced mutually within different nodes, providing flexible information mobility between nodes.

### System Variables

System variables refer to pre-set system-level parameters within Chatflow / Workflow App that can be globally read by other nodes. All system-level variables begin with `sys.`

#### Workflow

Workflow type application provides the system variables below:

<table><thead><tr><th>Variables name</th><th>Data Type</th><th width="297">Description</th><th>Remark</th></tr></thead><tbody><tr><td><code>sys.files</code></td><td> Array[File]</td><td>File Parameter: Stores images uploaded by users</td><td>The image upload function needs to be enabled in the 'Features' section in the upper right corner of the application orchestration page</td></tr><tr><td><code>sys.user_id</code></td><td>String</td><td>User ID: A unique identifier automatically assigned by the system to each user when they use a workflow application. It is used to distinguish different users</td><td></td></tr></tbody></table>

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption><p>Workflow App System Variables</p></figcaption></figure>

#### Chatflow

Chatflow type application provides the following system variables:

<table><thead><tr><th>Variables name</th><th>Data Type</th><th width="283">Description</th><th>Remark</th></tr></thead><tbody><tr><td><code>sys.query</code></td><td> String</td><td>Content entered by the user in the chatting box.</td><td></td></tr><tr><td><code>sys.files</code></td><td> Array[File]</td><td>File Parameter: Stores images uploaded by users</td><td>The image upload function needs to be enabled in the 'Features' section in the upper right corner of the application orchestration page</td></tr><tr><td><code>sys.dialogue_count</code></td><td>Number</td><td><p>The number of conversations turns during the user's interaction with a Chatflow application. The count automatically increases by one after each chat round and can be combined with if-else nodes to create rich branching logic.<br></p><p>For example, at the Xth conversation turn, LLM will review the conversation history and automatically provide an analysis.</p></td><td></td></tr><tr><td><code>sys.conversation_id</code></td><td>String</td><td>A unique ID for the chatting box interaction session, grouping all related messages into the same conversation, ensuring that the LLM continues the chatting on the same topic and context.</td><td></td></tr><tr><td><code>sys.user_id</code></td><td>String</td><td>A unique ID is assigned for each application user to distinguish different conversation users.</td><td></td></tr></tbody></table>

<figure><img src="../../.gitbook/assets/image (1).png" alt="chatflow app system variables"><figcaption><p>Chatflow App System Variables</p></figcaption></figure>

### Environment Variables

**Environment variables are used to protect sensitive information involved in workflows**, such as API keys and database passwords used when running workflows. They are stored in the workflow rather than in the code, allowing them to be shared across different environments.

<figure><img src="../../../img/en-env-variable.png" alt="Environment Variables"><figcaption><p>Environment Variables</p></figcaption></figure>

Supports the following 3 data types:

* String
* Number
* Secret

Environmental variables have the following characteristics:

* Environment variables can be globally referenced within most nodes;
* Environment variable names cannot be duplicated;
* Output variables of nodes are generally read-only and cannot be written to.

***

### Conversation Variables

> Conversation variables are only applicable to [Chatflow](variables.md#chatflow-and-workflow) App.

**Conversation variables allow application developers to specify particular information that needs to be temporarily stored within the same Chatflow session, ensuring that this information can be referenced across multiple rounds of chatting within the current chatflow**. This can include context, files uploaded to the chatting box(coming soon), user preferences input during the conversation, etc. It's like providing a "memo" for the LLM that can be checked at any time, avoiding information bias caused by LLM memory errors.

For example, you can store the language preference input by the user in the first round of chatting in a conversation variable. The LLM will refer to the information in the conversation variable when answering and use the specified language to reply to the user in subsequent chats.

<figure><img src="../../../img/conversation-var.png" alt=""><figcaption><p>Conversation Variable</p></figcaption></figure>

**Conversation variables** support the following six data types:

* String
* Number
* Object
* Array\[string]
* Array\[number]
* Array\[object]

**Conversation variables** have the following features:

* Conversation variables can be referenced globally within most nodes in the same Chatflow App;
* Writing to conversation variables requires using the [Variable Assigner](https://docs.dify.ai/guides/workflow/node/variable-assignment) node;
* Conversation variables are read-write variables;

About how to use conversation variables with the Variable Assigner node, please refer to the [Variable Assigner](node/variable-assignment.md).

### Notice

* To avoid variable name duplication, node naming must not be repeated
* The output variables of nodes are generally fixed variables and cannot be edited
