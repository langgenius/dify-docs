# Start

### Definition

Define the initial parameters for starting a workflow.

You can customize the input variables for initiating the workflow in the start node. Every workflow requires a start node.

<figure><img src="../../../.gitbook/assets/start-node.png" alt="" width="375"><figcaption><p>Workflow Start Node</p></figcaption></figure>

The start node supports defining input variables of four types:

* Text
* Paragraph
* Dropdown Options
* Number
* File (coming soon)

<figure><img src="../../../.gitbook/assets/output (2) (1).png" alt=""><figcaption><p>Configure Start Node Variables</p></figcaption></figure>

Once configured, the workflow will prompt for the values of the variables defined in the start node during execution.

<figure><img src="../../../.gitbook/assets/output (3) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Tip: In Chatflow, the start node provides built-in system variables: `sys.query` and `sys.files`.

`sys.query` is used for user input questions in conversational applications.

`sys.files` is used for file uploads in conversations, such as uploading an image, which needs to be used in conjunction with an image understanding model.
{% endhint %}
