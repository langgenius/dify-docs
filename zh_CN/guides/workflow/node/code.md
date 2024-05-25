# 代码执行

## 目录
- [介绍](#介绍)
- [使用场景](#使用场景)
- [本地部署](#本地部署)
- [安全策略](#安全策略)

## 介绍

代码节点支持运行 Python / NodeJS 代码以在工作流程中执行数据转换。它可以简化您的工作流程，适用于Arithmetic、JSON transform、文本处理等情景。

该节点极大地增强了开发人员的灵活性，使他们能够在工作流程中嵌入自定义的 Python 或 Javascript 脚本，并以预设节点无法达到的方式操作变量。通过配置选项，你可以指明所需的输入和输出变量，并撰写相应的执行代码：

<figure><img src="../../../.gitbook/assets/image (157).png" alt="" width="375"><figcaption></figcaption></figure>

## 配置
如果您需要在代码节点中使用其他节点的变量，您需要在`输入变量`中定义变量名，并引用这些变量，可以参考[变量引用](../key_concept.md#变量)。

您可以在高级依赖中在添加一些预加载需要消耗较多时间，或不是默认内置的依赖包，为了安全性考虑，目前仅支持下面这些依赖包 (截止2024年6月)。

| 模块名称 | 模块功能 |
| -------- | -------- |
| jinja2   | 一个为Python设计的现代模板语言，其原型来自Django的模板。 |
| httpx    | 为Python 3提供的全功能HTTP客户端，提供同步和异步API。 |
| requests | Python中一个简单的HTTP库。 |

在代码框中，您可以选择运行 Python 或 JavaScript，这里的代码块必须使用下面的格式：

{% tabs %}
{% tab title="Python" %} 
```python

def main(arg1: DataType, arg2: DataType) -> dict:
    result = statements(arg1, arg2)
    return {
        "result": result,
    }

```
{% endtab %}

{% tab title="JavaScript" %} 
```JavaScript
function main({arg1, arg2}) {
    statements; 
    return {
        result: arg1 + arg2
    }
}

```
{% endtab %}
{% endtabs %}

这一段代码块的输出变量必须在处于一个字典中，并且必须在代码块的下方定义变量名和数据类型，支持的数据类型有：字符串 String, 数字 Number, 数组 Array[Number], 数组 Array[String], 数组 Array[Object], 和 对象 Object。

## 使用场景
使用代码节点，您可以完成以下常见的操作：

### 结构化数据处理
在工作流中，经常要面对非结构化的数据处理，如JSON字符串的解析、提取、转换等。最典型的例子就是HTTP节点的数据处理，在常见的API返回结构中，数据可能会被嵌套在多层JSON对象中，而我们需要提取其中的某些字段。代码节点可以帮助您完成这些操作，下面是一个简单的例子，它从HTTP节点返回的JSON字符串中提取了`data.name`字段：

```python
def main(http_response: str) -> str:
    import json
    data = json.loads(http_response)
    return {
        # 注意在输出变量中声明result
        'result': data['data']['name'] 
    }
```

### 数学计算
当工作流中需要进行一些复杂的数学计算时，也可以使用代码节点。例如，计算一个复杂的数学公式，或者对数据进行一些统计分析。下面是一个简单的例子，它计算了一个数组的平方差：

```python
def main(x: list) -> float:
    return {
        # 注意在输出变量中声明result
        'result' : sum([(i - sum(x) / len(x)) ** 2 for i in x]) / len(x)
    }
```

### 拼接数据
有时，也许您需要拼接多个数据源，如多个知识检索、数据搜索、API调用等，代码节点可以帮助您将这些数据源整合在一起。下面是一个简单的例子，它将两个知识库的数据合并在一起：

```python
def main(knowledge1: list, knowledge2: list) -> list:
    return {
        # 注意在输出变量中声明result
        'result': knowledge1 + knowledge2
    }
```

## 本地部署
如果您是本地部署的用户，您需要启动一个沙盒服务，它会确保恶意代码不会被执行，同时，启动该服务需要使用Docker服务，您可以在[这里](https://github.com/langgenius/dify/tree/main/docker/docker-compose.middleware.yaml)找到Sandbox服务的具体信息，您也可以直接通过`docker-compose`启动服务：

```bash
docker-compose -f docker-compose.middleware.yaml up -d
```

## 限制
无论是Python还是Javascript，它们的执行环境都被严格隔离（沙箱化），以确保安全性。这意味着开发者不能使用那些消耗大量系统资源或可能引发安全问题的功能，如直接访问文件系统、进行网络请求或执行操作系统级别的命令。这些限制保证了代码的安全执行，同时避免了对系统资源的过度消耗。