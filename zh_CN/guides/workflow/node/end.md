# 结束

### 1 定义

定义一个工作流程结束的最终输出内容。每一个工作流在完整执行后都需要至少一个结束节点，用于输出完整执行的最终结果。

结束节点为流程终止节点，后面无法再添加其他节点，工作流应用中只有运行到结束节点才会输出执行结果。若流程中出现条件分叉，则需要定义多个结束节点。

结束节点需要声明一个或多个输出变量，声明时可以引用任意上游节点的输出变量。

{% hint style="info" %}
Chatflow 内不支持结束节点
{% endhint %}

***

### 2 场景

在以下[长故事生成工作流](iteration.md#shi-li-2-chang-wen-zhang-die-dai-sheng-cheng-qi-ling-yi-zhong-bian-pai-fang-shi)中，结束节点声明的变量 `Output` 为上游代码节点的输出，即该工作流会在 Code3 节点执行完成之后结束，并输出 Code3 的执行结果。

<figure><img src="../../../.gitbook/assets/image (284).png" alt=""><figcaption><p>结束节点-长故事生成示例</p></figcaption></figure>

**单路执行示例：**

<figure><img src="../../../.gitbook/assets/output (5).png" alt=""><figcaption></figcaption></figure>

**多路执行示例：**

<figure><img src="../../../.gitbook/assets/output (1) (3).png" alt=""><figcaption></figcaption></figure>
