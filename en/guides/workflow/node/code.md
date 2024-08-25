# Code Execution

## Table of Contents
- [Introduction](#introduction)
- [Usage Scenarios](#usage-scenarios)
- [Local Deployment](#local-deployment)
- [Security Policies](#security-policies)

## Introduction

The code node supports running Python/NodeJS code to perform data transformations within a workflow. It can simplify your workflow and is suitable for scenarios such as arithmetic operations, JSON transformations, text processing, and more.

This node significantly enhances the flexibility for developers, allowing them to embed custom Python or JavaScript scripts within the workflow and manipulate variables in ways that preset nodes cannot achieve. Through configuration options, you can specify the required input and output variables and write the corresponding execution code:

<figure><img src="/en/.gitbook/assets/guides/workflow/node/code/image (157).png" alt="" width="375"><figcaption></figcaption></figure>

## Configuration
If you need to use variables from other nodes in the code node, you must define the variable names in the `input variables` and reference these variables. You can refer to [Variable References](../key-concept.md#variables).

## Usage Scenarios
Using the code node, you can perform the following common operations:

### Structured Data Processing
In workflows, you often have to deal with unstructured data processing, such as parsing, extracting, and transforming JSON strings. A typical example is data processing from an HTTP node. In common API return structures, data may be nested within multiple layers of JSON objects, and you need to extract certain fields. The code node can help you perform these operations. Here is a simple example that extracts the `data.name` field from a JSON string returned by an HTTP node:

```python
def main(http_response: str) -> str:
    import json
    data = json.loads(http_response)
    return {
        # Note to declare 'result' in the output variables
        'result': data['data']['name'] 
    }
```

### Mathematical Calculations
When you need to perform complex mathematical calculations in a workflow, you can also use the code node. For example, calculating a complex mathematical formula or performing some statistical analysis on data. Here is a simple example that calculates the variance of an array:

```python
def main(x: list) -> float:
    return {
        # Note to declare 'result' in the output variables
        'result': sum([(i - sum(x) / len(x)) ** 2 for i in x]) / len(x)
    }
```

### Data Concatenation
Sometimes, you may need to concatenate multiple data sources, such as multiple knowledge retrievals, data searches, API calls, etc. The code node can help you integrate these data sources together. Here is a simple example that merges data from two knowledge bases:

```python
def main(knowledge1: list, knowledge2: list) -> list:
    return {
        # Note to declare 'result' in the output variables
        'result': knowledge1 + knowledge2
    }
```

## Local Deployment
If you are a local deployment user, you need to start a sandbox service to ensure that malicious code is not executed. This service requires the use of Docker. You can find specific information about the sandbox service [here](https://github.com/langgenius/dify/tree/main/docker/docker-compose.middleware.yaml). You can also start the service directly via `docker-compose`:

```bash
docker-compose -f docker-compose.middleware.yaml up -d
```

## Limitations
Both Python and JavaScript execution environments are strictly isolated (sandboxed) to ensure security. This means that developers cannot use functions that consume large amounts of system resources or may pose security risks, such as direct file system access, making network requests, or executing operating system-level commands. These limitations ensure the safe execution of the code while avoiding excessive consumption of system resources.