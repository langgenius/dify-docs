# Agent

## Definition

An Agent Node is a component in Dify Chatflow/Workflow that enables autonomous tool invocation. By integrating different Agent reasoning strategies, LLMs can dynamically select and execute tools at runtime, thereby performing multi-step reasoning.

## Configuration Steps

### Add the Node

In the Dify Chatflow/Workflow editor, drag the Agent node from the components panel onto the canvas.

<figure><img src="../../../.gitbook/assets/en-1-9-1.png" alt=""><figcaption></figcaption></figure>

### Select an Agent Strategy

In the node configuration panel, click Agent Strategy.

<figure><img src="../../../.gitbook/assets/en-1-9-0.png" alt=""><figcaption></figcaption></figure>

From the dropdown menu, select the desired Agent reasoning strategy. Dify provides two built-in strategies, **Function Calling and ReAct**, which can be installed from the **Marketplace → Agent Strategies category**.

<figure><img src="../../../.gitbook/assets/en-1-9-2.png" alt=""><figcaption></figcaption></figure>

#### 1. Function Calling

Function Calling maps user commands to predefined functions or tools. The LLM first identifies user intent, then decides which function to call and extracts the required parameters. Its core mechanism involves explicitly calling external functions or tools.

Pros:

**• Precision:** For well-defined tasks, it can call the corresponding tool directly without requiring complex reasoning.

**• Easier external feature integration:** Various external APIs or tools can be wrapped into functions for the model to call.

**• Structured output:** The model outputs structured information about function calls, facilitating processing by downstream nodes.

<figure><img src="../../../.gitbook/assets/en-agent-1.png" alt=""><figcaption></figcaption></figure>

#### 2. ReAct (Reason + Act)

ReAct enables the Agent to alternate between reasoning and taking action: the LLM first thinks about the current state and goal, then selects and calls the appropriate tool. The tool’s output in turn informs the LLM’s next step of reasoning and action. This cycle continues until the problem is resolved.

Pros:

**• Effective external information use:** It can leverage external tools to retrieve information and handle tasks that the model alone cannot accomplish.

**• Improved explainability:** Because reasoning and actions are interwoven, there is a certain level of traceability in the Agent’s thought process.

**• Wide applicability:** Suitable for scenarios that require external knowledge or need to perform specific actions, such as Q\&A, information retrieval, and task execution.

<figure><img src="../../../.gitbook/assets/en-agent-2.png" alt=""><figcaption></figcaption></figure>

Developers can contribute Agent strategy plugins to the public [repository](https://github.com/langgenius/dify-plugins). After review, these plugins will be listed in the Marketplace for others to install.

### Configure Node Parameters

After choosing the Agent strategy, the configuration panel will display the relevant options. For the Function Calling and ReAct strategies that ship with Dify, the available configuration items include:

1. **Model:** Select the large language model that drives the Agent.
2. **Tools List:** The approach to using tools is defined by the Agent strategy. Click + to add and configure tools the Agent can call.
   * Search: Select an installed tool plugin from the dropdown.
   * Authorization: Provide API keys and other credentials to enable the tool.
   * Tool Description and Parameter Settings: Provide a description to help the LLM understand when and why to use the tool, and configure any functional parameters.
3. **Instruction**: Define the Agent’s task goals and context. Jinja syntax is supported to reference upstream node variables.
4. **Query**: Receives user input.
5. **Maximum Iterations:** Set the maximum number of execution steps for the Agent.
6. **Output Variables:** Indicates the data structure output by the node.

<figure><img src="../../../.gitbook/assets/en-1-9-3.png" alt=""><figcaption></figcaption></figure>

## Logs

During execution, the Agent node generates detailed logs. You can see overall node execution information—including inputs and outputs, token usage, time spent, and status. Click Details to view the output from each round of Agent strategy execution.

<figure><img src="../../../.gitbook/assets/en-1-9-6.png" alt=""><figcaption></figcaption></figure>
