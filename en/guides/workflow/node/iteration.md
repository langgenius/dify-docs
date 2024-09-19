# Iteration

### Definition

Execute multiple steps on an array until all results are output.

The iteration step performs the same steps on each item in a list. To use iteration, ensure that the input value is formatted as a list object. The iteration node allows AI workflows to handle more complex processing logic. It is a user-friendly version of the loop node, making some compromises in customization to allow non-technical users to quickly get started.

***

### Scenarios

#### **Example 1: Long Article Iteration Generator**

<figure><img src="../../../../img/long-article-iteration-generator.png" alt=""><figcaption><p>Long Story Generator</p></figcaption></figure>

1. Enter the story title and outline in the **Start Node**.
2. Use a **Generate Subtitles and Outlines Node** to use LLM to generate the complete content from user input.
3. Use a **Extract Subtitles and Outlines Node** to convert the complete content into an array format.
4. Use an **Iteration Node** to wrap an **LLM Node** and generate content for each chapter through multiple iterations.
5. Add a **Direct Answer Node** inside the iteration node to achieve streaming output after each iteration.

**Detailed Configuration Steps**

1. Configure the story title (title) and outline (outline) in the **Start Node**.

<figure><img src="../../../../img/workflow-start-node.png" alt="" width="375"><figcaption><p>Start Node Configuration</p></figcaption></figure>

2. Use a **Generate Subtitles and Outlines Node** to convert the story title and outline into complete text.

<figure><img src="../../../../img/workflow-generate-subtitles-node.png" alt="" width="375"><figcaption><p>Template Node</p></figcaption></figure>

3. Use a **Extract Subtitles and Outlines Node** to convert the story text into an array (Array) structure. The parameter to extract is `sections`, and the parameter type is `Array[Object]`.

<figure><img src="../../../../img/workflow-extract-subtitles-and-outlines.png" alt="" width="375"><figcaption><p>Parameter Extraction</p></figcaption></figure>

{% hint style="info" %}
The effectiveness of parameter extraction is influenced by the model's inference capability and the instructions given. Using a model with stronger inference capabilities and adding examples in the **instructions** can improve the parameter extraction results.
{% endhint %}

4. Use the array-formatted story outline as the input for the iteration node and process it within the iteration node using an **LLM Node**.

<figure><img src="../../../../img/workflow-iteration-node.png" alt="" width="375"><figcaption><p>Configure Iteration Node</p></figcaption></figure>

Configure the input variables `GenerateOverallOutline/output` and `Iteration/item` in the LLM Node.

<figure><img src="../../../../img/workflow-iteration-llm-node.png" alt="" width="375"><figcaption><p>Configure LLM Node</p></figcaption></figure>

{% hint style="info" %}
Built-in variables for iteration: `items[object]` and `index[number]`.

`items[object]` represents the input item for each iteration;

`index[number]` represents the current iteration round;
{% endhint %}

1. Configure a **Direct Reply Node** inside the iteration node to achieve streaming output after each iteration.

<figure><img src="../../../../img/workflow-configure-answer-node.png" alt="" width="375"><figcaption><p>Configure Answer Node</p></figcaption></figure>

6. Complete debugging and preview.

<figure><img src="../../../../img/iteration-node-iteration-through-story-chapters.png" alt=""><figcaption><p>Generate by Iterating Through Story Chapters</p></figcaption></figure>

#### **Example 2: Long Article Iteration Generator (Another Arrangement)**

<figure><img src="../../../../img/iteration-node-iteration-long-article-iteration-generator.png" alt=""><figcaption></figcaption></figure>

* Enter the story title and outline in the **Start Node**.
* Use an **LLM Node** to generate subheadings and corresponding content for the article.
* Use a **Code Node** to convert the complete content into an array format.
* Use an **Iteration Node** to wrap an **LLM Node** and generate content for each chapter through multiple iterations.
* Use a **Template Conversion** Node to convert the string array output from the iteration node back to a string.
* Finally, add a **Direct Reply Node** to directly output the converted string.

### What is Array Content

A list is a specific data type where elements are separated by commas and enclosed in `[` and `]`. For example:

**Numeric:**

```
[0,1,2,3,4,5]
```

**String:**

```
["Monday", "Tuesday", "Wednesday", "Thursday"]
```

**JSON Object:**

```
[
    {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    },
    {
        "name": "Bob",
        "age": 25,
        "email": "bob@example.com"
    },
    {
        "name": "Charlie",
        "age": 35,
        "email": "charlie@example.com"
    }
]
```

***

### Nodes Supporting Array Return

* Code Node
* Parameter Extraction
* Knowledge Base Retrieval
* Iteration
* Tools
* HTTP Request

### How to Obtain Array-Formatted Content

**Return Using the CODE Node**

<figure><img src="../../../../img/workflow-extract-subtitles-and-outlines.png" alt="" width="375"><figcaption><p>Parameter Extraction</p></figcaption></figure>

**Return Using the Parameter Extraction Node**

<figure><img src="../../../../img/workflow-parameter-extraction-node.png" alt="" width="375"><figcaption><p>Parameter Extraction</p></figcaption></figure>

### How to Convert an Array to Text

The output variable of the iteration node is in array format and cannot be directly output. You can use a simple step to convert the array back to text.

**Convert Using a Code Node**

<figure><img src="../../../../img/iteration-code-node-convert.png" alt="" width="334"><figcaption><p>Code Node Conversion</p></figcaption></figure>

CODE Example:

```python
def main(articleSections: list):
    data = articleSections
    return {
        "result": "/n".join(data)
    }
```

**Convert Using a Template Node**

<figure><img src="../../../../img/workflow-template-node.png" alt="" width="332"><figcaption><p>Template Node Conversion</p></figcaption></figure>

CODE Example:

```django
{{ articleSections | join("/n") }}
```
