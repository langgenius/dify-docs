# Integrate W&B Weave

### What is W&b Weave

Weights & Biases (W&B) Weave is a framework for tracking, experimenting with, evaluating, deploying, and improving LLM-based applications. Designed for flexibility and scalability, Weave supports every stage of your LLM application development workflow:

{% hint style="info" %}
For more details, please refer to [Weave](https://weave-docs.wandb.ai/).
{% endhint %}

***

### How to Configure Weave

#### 1. Register/Login to [W&B Weave](https://wandb.ai/signup)
Get your API key

Then, create a Weights & Biases (W&B) account at https://wandb.ai and copy your API key from https://wandb.ai/authorize


#### 2. Integrating W&B Weave with Dify

Configure Weave in the Dify application. Open the application you need to monitor, open **Monitoring** in the side menu, and select **Tracing app performance** on the page.

<figure><img src="../../../.gitbook/assets/tracing-app-performance-weave.png" alt=""><figcaption><p>Tracing app performance (Weave)</p></figcaption></figure>

After clicking configure, paste the **API Key** and **project name**, also specify the **W&B entity**(optionally, default is your username) into the configuration and save.

<figure><img src="../../../.gitbook/assets/config-weave.png" alt=""><figcaption><p>Configure W&B Weave</p></figcaption></figure>

Once successfully saved, you can view the monitoring status on the current page.

<figure><img src="../../../.gitbook/assets/integrate-with-weave.png" alt=""><figcaption><p>View configuration status</p></figcaption></figure>

### Viewing Monitoring Data in Weave

Once configured, the debug or production data from applications within Dify can be monitored in Weave.

<figure><img src="../../../.gitbook/assets/debug-app-in-dify.png" alt=""><figcaption><p>Debugging Applications in Dify</p></figcaption></figure>

When you switch to Weave, you can view detailed operation logs of Dify applications in the dashboard.

<figure><img src="../../../.gitbook/assets/viewing-app-data-in-weave.png" alt=""><figcaption><p>Viewing application data in Weave</p></figcaption></figure>

Detailed LLM operation logs through Weave will help you optimize the performance of your Dify application.

### Monitoring Data List

#### **Workflow/Chatflow Trace Information**

**Used to track workflows and chatflows**

| Workflow                                 | Weave Trace                  |
| ---------------------------------------- | ---------------------------- |
| workflow\_app\_log\_id/workflow\_run\_id | id                           |
| user\_session\_id                        | - placed in metadata         |
| workflow\_{id}                           | name                         |
| start\_time                              | start\_time                  |
| end\_time                                | end\_time                    |
| inputs                                   | inputs                       |
| outputs                                  | outputs                      |
| Model token consumption                  | usage\_metadata              |
| metadata                                 | extra                        |
| error                                    | error                        |
| \[workflow]                              | tags                         |
| "conversation\_id/none for workflow"     | conversation\_id in metadata |
| conversion\_id                           | parent\_run\_id              |

**Workflow Trace Info**

* workflow\_id - Unique identifier of the workflow
* conversation\_id - Conversation ID
* workflow\_run\_id - ID of the current run
* tenant\_id - Tenant ID
* elapsed\_time - Time taken for the current run
* status - Run status
* version - Workflow version
* total\_tokens - Total tokens used in the current run
* file\_list - List of processed files
* triggered\_from - Source that triggered the current run
* workflow\_run\_inputs - Input data for the current run
* workflow\_run\_outputs - Output data for the current run
* error - Errors encountered during the current run
* query - Query used during the run
* workflow\_app\_log\_id - Workflow application log ID
* message\_id - Associated message ID
* start\_time - Start time of the run
* end\_time - End time of the run
* workflow node executions - Information about workflow node executions
* Metadata
  * workflow\_id - Unique identifier of the workflow
  * conversation\_id - Conversation ID
  * workflow\_run\_id - ID of the current run
  * tenant\_id - Tenant ID
  * elapsed\_time - Time taken for the current run
  * status - Run status
  * version - Workflow version
  * total\_tokens - Total tokens used in the current run
  * file\_list - List of processed files
  * triggered\_from - Source that triggered the current run

#### **Message Trace Information**

**Used to track LLM-related conversations**

| Chat                             | Weave Trace                  |
| -------------------------------- | ---------------------------- |
| message\_id                      | id                           |
| user\_session\_id                | - placed in metadata         |
| “message\_{id}"                  | name                         |
| start\_time                      | start\_time                  |
| end\_time                        | end\_time                    |
| inputs                           | inputs                       |
| outputs                          | outputs                      |
| Model token consumption          | usage\_metadata              |
| metadata                         | extra                        |
| error                            | error                        |
| \["message", conversation\_mode] | tags                         |
| conversation\_id                 | conversation\_id in metadata |
| conversion\_id                   | parent\_run\_id              |

**Message Trace Info**

* message\_id - Message ID
* message\_data - Message data
* user\_session\_id - User session ID
* conversation\_model - Conversation mode
* message\_tokens - Number of tokens in the message
* answer\_tokens - Number of tokens in the answer
* total\_tokens - Total number of tokens in the message and answer
* error - Error information
* inputs - Input data
* outputs - Output data
* file\_list - List of processed files
* start\_time - Start time
* end\_time - End time
* message\_file\_data - File data associated with the message
* conversation\_mode - Conversation mode
* Metadata
  * conversation\_id - Conversation ID
  * ls\_provider - Model provider
  * ls\_model\_name - Model ID
  * status - Message status
  * from\_end\_user\_id - ID of the sending user
  * from\_account\_id - ID of the sending account
  * agent\_based - Whether the message is agent-based
  * workflow\_run\_id - Workflow run ID
  * from\_source - Message source

#### **Moderation Trace Information**

**Used to track conversation moderation**

| Moderation    | Weave Trace          |
| ------------- | -------------------- |
| user\_id      | - placed in metadata |
| “moderation"  | name                 |
| start\_time   | start\_time          |
| end\_time     | end\_time            |
| inputs        | inputs               |
| outputs       | outputs              |
| metadata      | extra                |
| \[moderation] | tags                 |
| message\_id   | parent\_run\_id      |

**Moderation Trace Info**

* message\_id - Message ID
* user\_id: User ID
* workflow\_app\_log\_id - Workflow application log ID
* inputs - Moderation input data
* message\_data - Message data
* flagged - Whether the content is flagged for attention
* action - Specific actions taken
* preset\_response - Preset response
* start\_time - Moderation start time
* end\_time - Moderation end time
* Metadata
  * message\_id - Message ID
  * action - Specific actions taken
  * preset\_response - Preset response

#### **Suggested Question Trace Information**

**Used to track suggested questions**

| Suggested Question     | Weave Trace          |
| ---------------------- | -------------------- |
| user\_id               | - placed in metadata |
| suggested\_question    | name                 |
| start\_time            | start\_time          |
| end\_time              | end\_time            |
| inputs                 | inputs               |
| outputs                | outputs              |
| metadata               | extra                |
| \[suggested\_question] | tags                 |
| message\_id            | parent\_run\_id      |

**Message Trace Info**

* message\_id - Message ID
* message\_data - Message data
* inputs - Input content
* outputs - Output content
* start\_time - Start time
* end\_time - End time
* total\_tokens - Number of tokens
* status - Message status
* error - Error information
* from\_account\_id - ID of the sending account
* agent\_based - Whether the message is agent-based
* from\_source - Message source
* model\_provider - Model provider
* model\_id - Model ID
* suggested\_question - Suggested question
* level - Status level
* status\_message - Status message
* Metadata
  * message\_id - Message ID
  * ls\_provider - Model provider
  * ls\_model\_name - Model ID
  * status - Message status
  * from\_end\_user\_id - ID of the sending user
  * from\_account\_id - ID of the sending account
  * workflow\_run\_id - Workflow run ID
  * from\_source - Message source

#### **Dataset Retrieval Trace Information**

**Used to track knowledge base retrieval**

| Dataset Retrieval     | Weave Trace          |
| --------------------- | -------------------- |
| user\_id              | - placed in metadata |
| dataset\_retrieval    | name                 |
| start\_time           | start\_time          |
| end\_time             | end\_time            |
| inputs                | inputs               |
| outputs               | outputs              |
| metadata              | extra                |
| \[dataset\_retrieval] | tags                 |
| message\_id           | parent\_run\_id      |

**Dataset Retrieval Trace Info**

* message\_id - Message ID
* inputs - Input content
* documents - Document data
* start\_time - Start time
* end\_time - End time
* message\_data - Message data
* Metadata
  * message\_id - Message ID
  * ls\_provider - Model provider
  * ls\_model\_name - Model ID
  * status - Message status
  * from\_end\_user\_id - ID of the sending user
  * from\_account\_id - ID of the sending account
  * agent\_based - Whether the message is agent-based
  * workflow\_run\_id - Workflow run ID
  * from\_source - Message source

#### **Tool Trace Information**

**Used to track tool invocation**

| Tool                  | Weave Trace          |
| --------------------- | -------------------- |
| user\_id              | - placed in metadata |
| tool\_name            | name                 |
| start\_time           | start\_time          |
| end\_time             | end\_time            |
| inputs                | inputs               |
| outputs               | outputs              |
| metadata              | extra                |
| \["tool", tool\_name] | tags                 |
| message\_id           | parent\_run\_id      |

#### **Tool Trace Info**

* message\_id - Message ID
* tool\_name - Tool name
* start\_time - Start time
* end\_time - End time
* tool\_inputs - Tool inputs
* tool\_outputs - Tool outputs
* message\_data - Message data
* error - Error information, if any
* inputs - Inputs for the message
* outputs - Outputs of the message
* tool\_config - Tool configuration
* time\_cost - Time cost
* tool\_parameters - Tool parameters
* file\_url - URL of the associated file
* Metadata
  * message\_id - Message ID
  * tool\_name - Tool name
  * tool\_inputs - Tool inputs
  * tool\_outputs - Tool outputs
  * tool\_config - Tool configuration
  * time\_cost - Time cost
  * error - Error information, if any
  * tool\_parameters - Tool parameters
  * message\_file\_id - Message file ID
  * created\_by\_role - Role of the creator
  * created\_user\_id - User ID of the creator

**Generate Name Trace Information**

**Used to track conversation title generation**

| Generate Name     | Weave Trace          |
| ----------------- | -------------------- |
| user\_id          | - placed in metadata |
| generate\_name    | name                 |
| start\_time       | start\_time          |
| end\_time         | end\_time            |
| inputs            | inputs               |
| outputs           | outputs              |
| metadata          | extra                |
| \[generate\_name] | tags                 |

**Generate Name Trace Info**

* conversation\_id - Conversation ID
* inputs - Input data
* outputs - Generated conversation name
* start\_time - Start time
* end\_time - End time
* tenant\_id - Tenant ID
* Metadata
  * conversation\_id - Conversation ID
  * tenant\_id - Tenant ID
