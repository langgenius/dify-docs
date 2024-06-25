# 条件分支

### 定义

允许你根据 if/else 条件将 workflow 拆分成两个分支。

条件分支节点有三个部分：

* IF条件：选择变量，设置条件和满足条件的值；
* IF 条件判断为 `True`，执行 IF 路径；
* IF 条件判断为 `False`，执行 ELSE 路径；

**条件类型**

* 包含（Contains）
* 不包含（Not contains）
* 开始是（Start with）
* 结束是（End with）
* 是（Is）
* 不是（Is not）
* 为空（Is empty）
* 不为空（Is not empty）

***

### 场景

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

以上图**文本总结工作流**为例

* IF条件： 选择开始节点中的`summarystyle`变量，条件为 **包含**  `技术`；
* IF 条件判断为 `True`，执行 IF 路径，通过知识检索节点查询技术相关知识再到 LLM 节点回复（图中上半部分）；
* IF 条件判断为 `False`，即`summarystyle`变量输入 **不包含**  `技术`，执行 ELSE 路径，通过 LLM2 节点进行回复（图中下半部分）；

**多重条件判断**

涉及复杂的条件判断时，可以设置多重条件判断，在条件之间设置 **AND** 或者 **OR**，即在条件之间取**交集**或者**并集**。

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt="" width="369"><figcaption><p>多重条件判断</p></figcaption></figure>
