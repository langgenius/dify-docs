# Code

## Introduction

The Code node lets you write Python / NodeJS code to perform data transformations not achievable via pre-defined nodes. It lends a lot of flexibility to your workflows and can be used to perform calculations, process JSON data, transform texts, and more.

<figure><img src="../../../.gitbook/assets/image (157).png" alt="" width="375"><figcaption></figcaption></figure>

## Including variables
If you need to use variables from other nodes within your code, you need to define the variable names in `input variables` and reference these variables, see [Variable Reference](../key_concept.md#variable) for details.

You will need to define the type of the output variable for 

## Use Cases
With the code node, you can perform the following common operations:

### Structured Data Processing
In workflows, it's often necessary to deal with unstructured data processing, such as parsing, extracting, and transforming JSON strings. A typical example is dealing with output from the [HTTP Request node](./http-request.md), where the data you need to extract might be nested under multiple layers within a JSON object. The code node can help you accomplish such tasks. Here's a simple example that extracts the `data.name` field from a JSON string returned by an HTTP node:

```python
def main(http_response: str) -> str:
    import json
    data = json.loads(http_response)
    return data['data']['name']
```

### Mathematical Calculations
You can also write custom code to calculate a complex mathematical formula or perform some statistical analysis on certain data. Here is a simple example that calculates the variance of a list:

```python
def main(x: list) -> float:
    return sum([(i - sum(x) / len(x)) ** 2 for i in x]) / len(x)
```

### Data Transformations

```python
def main(knowledge1: list, knowledge2: list) -> list:
    return knowledge1 + knowledge2
```

## Limitations
The execution environment is sandboxed for both Python and Javascript (If you are self-hosting Dify, a sandbox service would be started with Docker). 

This means that certain functionalities that require extensive system resources or pose security risks are not available. This includes, but is not limited to, direct file system access, network calls, and operating system-level commands.
