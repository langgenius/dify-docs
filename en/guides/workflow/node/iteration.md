# Iteration

### Definition

Sequentially performs the same operations on array elements until all results are outputted, functioning as a task batch processor. Iteration nodes typically work in conjunction with array variables.

For example, when processing long text translations, inputting all content directly into an LLM node may reach the single conversation limit. To address the issue, upstream nodes first split the long text into multiple chunks, then use iteration nodes to perform batch translations, thus avoiding the message limit of a single LLM conversation.

***

### Functional Description

Using iteration nodes requires input values to be formatted as list objects. The node sequentially processes all elements in the array variable from the iteration start node, applying identical processing steps to each element. Each processing cycle is called an iteration, culminating in the final output.

An iteration node consists of three core components: **Input Variables**, **Iteration Workflow**, and **Output Variables**.

**Input Variables:** Accepts only Array type data.

**Iteration Workflow:** Supports multiple workflow nodes to orchestrate task sequences within the iteration node.

**Output Variables:** Outputs only array variables (`Array[List]`). 

<figure><img src="https://assets-docs.dify.ai/2024/12/7c94bccbb6f8dc4570c69c2bf02ec6d3.png" alt=""><figcaption><p>Iteration Node Functional Description</p></figcaption></figure>

### Scenarios

#### **Example 1: Long Article Iteration Generator**

<figure><img src="https://assets-docs.dify.ai/img/en/node/ac0c75fcddc4462455bd8a25ef9ed8c6.webp" alt=""><figcaption><p>Long Story Generator</p></figcaption></figure>

1. Enter the story title and outline in the **Start Node**.
2. Use a **Generate Subtitles and Outlines Node** to use LLM to generate the complete content from user input.
3. Use a **Extract Subtitles and Outlines Node** to convert the complete content into an array format.
4. Use an **Iteration Node** to wrap an **LLM Node** and generate content for each chapter through multiple iterations.
5. Add a **Direct Answer Node** inside the iteration node to achieve streaming output after each iteration.

**Detailed Configuration Steps**

1. Configure the story title (title) and outline (outline) in the **Start Node**.

<figure><img src="https://assets-docs.dify.ai/img/en/node/c8b9606f6976af8a57e86281f575d41f.webp" alt="" width="375"><figcaption><p>Start Node Configuration</p></figcaption></figure>

2. Use a **Generate Subtitles and Outlines Node** to convert the story title and outline into complete text.

<figure><img src="https://assets-docs.dify.ai/img/en/node/c12c0dff663c082064b449e67dd0ff94.webp" alt="" width="375"><figcaption><p>Template Node</p></figcaption></figure>

3. Use a **Extract Subtitles and Outlines Node** to convert the story text into an array (Array) structure. The parameter to extract is `sections`, and the parameter type is `Array[Object]`.

<figure><img src="https://assets-docs.dify.ai/img/en/node/1581f742f3ff807be0e943bd049ffadb.webp" alt="" width="375"><figcaption><p>Parameter Extraction</p></figcaption></figure>

{% hint style="info" %}
The effectiveness of parameter extraction is influenced by the model's inference capability and the instructions given. Using a model with stronger inference capabilities and adding examples in the **instructions** can improve the parameter extraction results.
{% endhint %}

4. Use the array-formatted story outline as the input for the iteration node and process it within the iteration node using an **LLM Node**.

<figure><img src="https://assets-docs.dify.ai/img/en/node/2db01196a9f86eaee7526c436e54eb1b.webp" alt="" width="375"><figcaption><p>Configure Iteration Node</p></figcaption></figure>

Configure the input variables `GenerateOverallOutline/output` and `Iteration/item` in the LLM Node.

<figure><img src="https://assets-docs.dify.ai/img/en/node/5dbc272b4725337025332aa950b3919e.webp" alt="" width="375"><figcaption><p>Configure LLM Node</p></figcaption></figure>

{% hint style="info" %}
Built-in variables for iteration: `items[object]` and `index[number]`.

`items[object]` represents the input item for each iteration;

`index[number]` represents the current iteration round;
{% endhint %}

5. Configure a **Direct Reply Node** inside the iteration node to achieve streaming output after each iteration.

<figure><img src="https://assets-docs.dify.ai/img/en/node/d4801e73725bde928d3035ef14ed4e0b.webp" alt="" width="375"><figcaption><p>Configure Answer Node</p></figcaption></figure>

6. Complete debugging and preview.

<figure><img src="https://assets-docs.dify.ai/img/en/node/0f31b88f930bf486c2c08f613629df4e.webp" alt=""><figcaption><p>Generate by Iterating Through Story Chapters</p></figcaption></figure>

#### **Example 2: Long Article Iteration Generator (Another Arrangement)**

<figure><img src="https://assets-docs.dify.ai/img/en/node/c2d70c33a3a116dfecded4f94026e0c4.webp" alt=""><figcaption></figcaption></figure>

* Enter the story title and outline in the **Start Node**.
* Use an **LLM Node** to generate subheadings and corresponding content for the article.
* Use a **Code Node** to convert the complete content into an array format.
* Use an **Iteration Node** to wrap an **LLM Node** and generate content for each chapter through multiple iterations.
* Use a **Template Conversion** Node to convert the string array output from the iteration node back to a string.
* Finally, add a **Direct Reply Node** to directly output the converted string.

***

### Advanced Feature

#### Parallel Mode

The iteration node supports parallel processing, improving execution efficiency when enabled.

<figure><img src="https://assets-docs.dify.ai/2024/12/516af5e7427fce9a58fa9d9b583230d4.png" alt=""><figcaption><p>Enable parallel mode</p></figcaption></figure>

Below illustrates the comparison between parallel and sequential execution in the iteration node.

<figure><img src="https://assets-docs.dify.ai/2024/12/2656dec26d6357556a280fcd69ccd9a7.png" alt=""><figcaption><p>Sequential and Parallel Processing Flow Diagram</p></figcaption></figure>

Parallel mode supports up to 10 concurrent iterations. When processing more than 10 tasks, the first 10 elements execute simultaneously, with remaining tasks processed after the completion of the initial batch.

{% hint style="info" %}
Avoid placing Direct Answer, Variable Assignment, or Tool nodes within the iteration node to prevent potential errors.
{% endhint %}

* **Error response method**

Iteration nodes process multiple tasks and may encounter errors during element processing. To prevent a single error from interrupting all tasks, configure the **Error Response Method**:

* **Terminated**: Terminates the iteration node and outputs error messages when an exception is detected.
* **Continue on error**: Ignores error messages and continues processing remaining elements. The output contains successful results with null values for errors.
* **Remove abnormal output**: Ignores error messages and continues processing remaining elements. The output contains only successful results.

Input and output variables maintain a one-to-one correspondence. For example:

* Input: \[1, 2, 3]
* Output: \[result-1, result-2, result-3]

Error handling examples:

* With **Continue on error**: \[result-1, null, result-3]
* With **Remove abnormal output**: \[result-1, result-3]

***

### Reference

#### How to Obtain Array-Formatted Content

Array variables can be generated via the following nodes as iteration node inputs:

* [Code Node](code.md)

<figure><img src="https://assets-docs.dify.ai/img/en/node/1581f742f3ff807be0e943bd049ffadb.webp" alt="" width="375"><figcaption><p>Parameter Extraction</p></figcaption></figure>

* [Parameter Extraction](parameter-extractor.md)

<figure><img src="https://assets-docs.dify.ai/img/en/node/11e57b386a281cea758b58e5de8e3d31.webp" alt="" width="375"><figcaption><p>Parameter Extraction</p></figcaption></figure>

* [Knowledge Base Retrieval](knowledge-retrieval.md)
* [Iteration](iteration.md)
* [Tools](tools.md)
* [HTTP Request](http-request.md)

***

#### How to Convert an Array to Text

The output variable of the iteration node is in array format and cannot be directly output. You can use a simple step to convert the array back to text.

**Convert Using a Code Node**

<figure><img src="https://assets-docs.dify.ai/img/en/node/ddc417809bf899067f2163ed62a1b96b.webp" alt="" width="334"><figcaption><p>Code Node Conversion</p></figcaption></figure>

CODE Example:

```python
def main(articleSections: list):
    data = articleSections
    return {
        "result": "/n".join(data)
    }
```

**Convert Using a Template Node**

<figure><img src="https://assets-docs.dify.ai/img/en/node/15cba62731a031ca6dd057e2fac61866.webp" alt="" width="332"><figcaption><p>Template Node Conversion</p></figcaption></figure>

CODE Example:

```django
{{ articleSections | join("/n") }}
```
