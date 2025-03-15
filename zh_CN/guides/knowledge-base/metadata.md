# 元数据

## 什么是元数据？

### 定义

元数据是用于描述其他数据的信息。简单来说，它是“关于数据的数据”。它就像一本书的目录或标签，可以为你介绍数据的内容、来源和用途。
通过提供数据的上下文，元数据能帮助你在知识库内快速查找和管理数据。

### 其他相关定义

-   **元数据字段（Metadata Field）**：元数据字段是用于描述文档特定属性的标识项，每个字段代表文档的某个特征或信息。例如，“author”字段用于描述该文档的作者。

-   **字段值计数（Value Count）**：字段值计数是指在某条元数据字段中不同字段值的数量。例如，此处的“3”是字段值计数，指该字段中有 3 个独特的字段值。

<p align="center">
  <img src="https://assets-docs.dify.ai/2025/03/330f26e90438cf50167c4cb6ce30e458.png" width="300" alt="metadata_field">
</p>

-   **字段名（Field Name）**：字段名是对该元数据的简短描述，它表示该字段所代表的内容。例如“author”“language”等。

-   **字段值（Value）**：字段值是该字段的具体信息或属性，例如“Jack”“English”。

<p align="center">
  <img src="https://assets-docs.dify.ai/2025/03/b6a197aa21ab92db93869fcbfa156b62.png" width="300" alt="field_name_and_value">
</p>

-   **值类型（Value Type）**：值类型指字段值的类型。
    -   目前，Dify 的元数据功能仅支持以下三种值类型：
        -   **字符串**（String）：文本值。
        -   **数字**（Number）：数值。
        -   **时间**（Time）：日期和时间。

<p align="center">
  <img src="https://assets-docs.dify.ai/2025/03/c208291ea8abae500819d195c2d52d65.png" width="280" alt="value_type">
</p>

## 如何管理知识库元数据？

### 管理知识库元数据字段

在知识库管理界面，你可以创建、修改和删除元数据字段。

> 注意：所有在此界面进行的更新均为**全局更新**，这意味着对元数据字段列表的任何更改都会影响整个知识库，包括所有文档中标记的元数据。

#### 元数据管理界面简介

##### 入口

在知识库管理界面，点击右上方的 **元数据** 按钮，进入元数据管理界面。

![metadata_entrance](https://assets-docs.dify.ai/2025/03/bd43305d49cc1511683b4a098c8f6e5a.png)

![metadata_panel](https://assets-docs.dify.ai/2025/03/6000c85b5d2e29a2a5af5e0a047a7a59.png)

##### 功能

-   **查看元数据字段**：你可以查看知识库的内置元数据和自定义元数据。**内置元数据（Built-in）** 是系统自动生成的字段；**自定义元数据** 是用户根据需求手动添加的字段。

-   **新增元数据字段**：通过点击 **+添加元数据** 按钮，你可以添加新的元数据字段并选择字段值类型与填写字段名。

-   **编辑元数据字段**：通过点击每条元数据字段旁的编辑图标，你可以修改字段的名称。

-   **删除元数据字段**：通过点击每条元数据字段旁的删除图标，你可以移除不再需要的字段。


##### 价值

**元数据管理界面支持用户集中管理知识库中的元数据字段。** 这一界面能帮助用户灵活地调整文档的标识属性，使得文档在检索和访问时更加高效、准确。

##### 知识库元数据字段的类型

在知识库中，元数据字段分为两类：**内置元数据（Built-in）** 和 **自定义元数据**。

<table border="0" cellspacing="0" cellpadding="10" style="width: 100%; border-collapse: collapse;">
    <tr>
        <th style="width: 15%; text-align: center; background-color: #f5f5f5;"></th>
        <th style="width: 42.5%; text-align: center; background-color: #f5f5f5;">内置元数据（Built-in）</th>
        <th style="width: 42.5%; text-align: center; background-color: #f5f5f5;">自定义元数据</th>
    </tr>
    <tr>
        <td style="text-align: center;">显示位置</td>
        <td>知识库界面 元数据 栏的下半部分。</td>
        <td>知识库界面 元数据 栏的上半部分。</td>
    </tr>
    <tr>
        <td style="text-align: center;">示例图</td>
        <td><img src="https://assets-docs.dify.ai/2025/03/5d03e958ed936badf4eb1ca955372c8b.png" style="max-width: 100%;"></td>
        <td><img src="https://assets-docs.dify.ai/2025/03/692a2824501f4e2f5fcc016e27159859.png" style="max-width: 100%;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">启用方式</td>
        <td>默认禁用，需要手动开启才能生效。</td>
        <td>由用户根据需求自由添加。</td>
    </tr>
    <tr>
        <td style="text-align: center;">生成方式</td>
        <td>启用后，由系统自动提取相关信息并生成字段值。</td>
        <td>用户手动添加，完全由用户自定义。</td>
    </tr>
    <tr>
        <td style="text-align: center;">修改权限</td>
        <td>一旦生成，无法修改字段与字段值。</td>
        <td>可以删除或编辑字段名称，也可以修改字段值。</td>
    </tr>
    <tr>
        <td style="text-align: center;">应用范围</td>
        <td>启用后，适用于已上传和新上传的所有文档。</td>
        <td>添加元数据字段后，字段会储存在知识库的元数据列表中/需要手动设置，才能将该字段应用于具体文档。</td>
    </tr>
    <tr>
        <td style="text-align: center;">字段</td>
        <td>
            由系统预定义，包括：<br>
            • Original filename (string)：原始文件名<br>
            • Uploader (string)：上传者<br>
            • Upload date (time)：上传日期<br>
            • Last update date (time)：最后更新时间<br>
            • Source (string)：文件来源
        </td>
        <td>在初始状态下，知识库无自定义元数据字段，需要用户手动添加。</td>
    </tr>
    <tr>
        <td style="text-align: center;">字段值类型</td>
        <td colspan="2">
            用户可以自由选择字段值类型，目前，Dify的元数据功能仅支持以下三种值类型：<br>
            • 字符串 (string)：文本值<br>
            • 数字 (number)：数值<br>
            • 时间 (time)：日期和时间
        </td>
    </tr>
    <tr>
        <td style="text-align: center;">使用场景</td>
        <td>适用于存储和展示文档的基本信息，如文件名、上传者、上传日期等。</td>
        <td>适用于需要根据特定业务需求自定义的元数据字段，如文档的保密级别、标签等。</td>
    </tr>
</table>

#### 新建元数据字段

1.  点击 **+添加元数据** 按钮，弹出 **新建元数据** 弹窗。

![new_metadata](https://assets-docs.dify.ai/2025/03/5086db42c40be64e54926b645c38c9a0.png)

2.  在 **字段值类型** 中选择元数据字段的值类型。
    -   **字符串**（String）：文本值。
    -   **数字**（Number）：数值。
    -   **时间**（Time）：日期和时间。

3.  在 **名称** 框中填写字段的名称。

> 字段名仅支持小写字母、数字和下划线（_）字符，不支持空格和大写字母。

<p align="center">
  <img src="https://assets-docs.dify.ai/2025/03/24e85f14d4c7c3bcade25a7abfc15467.png" width="250" alt="field_name">
</p>

4.  点击 **保存** 按钮，保存字段。

> 如果新建单条字段，该字段将在知识库的所有文档中同步更新。

![save_field](https://assets-docs.dify.ai/2025/03/f44114cc58d4ba11ba60adb2d04c9b4c.png)

#### 修改元数据字段

1.  点击单条元数据字段右侧的编辑按钮，弹出 **重命名** 弹窗。

![rename_field_1](https://assets-docs.dify.ai/2025/03/94327185cbe366bf99221abf2f5ef55a.png)

2.  在 **名称** 框中修改字段名称。

> 此弹窗仅支持修改字段名称，不支持修改字段值类型。

<p align="center">
  <img src="https://assets-docs.dify.ai/2025/03/216ec7d9227bb7b2a199c1bd5d3d812c.png" width="300" alt="rename_field_2">
</p>

3.  点击 **保存** 按钮，保存修改后的字段。

![same_renamed_field](https://assets-docs.dify.ai/2025/03/022e42c170b40c35622b9b156c8cc159.png)

#### 删除元数据字段

点击单条元数据字段右侧的删除按钮，可以删除该字段。

> 如果删除单条字段，该字段及该字段下包含的字段值将从知识库的所有文档中删除。

![delete_field](https://assets-docs.dify.ai/2025/03/022e42c170b40c35622b9b156c8cc159.png)

### 编辑文档元数据信息

#### 批量编辑文档元数据信息

你可以在知识库管理界面批量编辑文档的元数据信息。

##### 编辑元数据弹窗简介

###### 入口

1. 打开知识库管理界面，在文档列表左侧的白色方框中勾选你希望批量操作的文档。勾选后，页面下方会弹出操作选项。

![edit_metadata_entrance](https://assets-docs.dify.ai/2025/03/18b0c435604db6173acba41662474446.png)

2. 点击操作选项中的 **元数据**，弹出 **编辑元数据** 弹窗。

![edit_metadata](https://assets-docs.dify.ai/2025/03/719f3c31498f23747fed7d7349fd64ba.png)

###### 功能

-   **查看选中文档的元数据信息：** 在弹窗的上半部分的 **已有元数据** 区和下半部分的 **新增元数据** 区，你会看到所有选中文档的元数据字段和此次操作新增的元数据字段。

{% hint style="info" %}
每个字段的左侧会显示该字段的编辑状态：
未编辑：字段左侧为空白，表示该字段未进行修改。
已编辑：字段左侧显示蓝色圆点，表示该字段已经被编辑。
重置：将光标悬停在蓝色圆点上时，圆点会变为 **重置** 按钮。点击后，该字段的内容会恢复到未编辑时的状态。
{% endhint %}

-   **删改字段值：** 你可以在每条字段右侧的矩形框中删改其字段值。

{% hint style="info" %}
如果某个字段只有一个值，你会看到该字段的值直接显示在字段右侧的矩形框中，可以直接修改或删除。
如果某个字段有多个值，矩形框内会显示 **多个值** 卡片。如果删除该卡片，所有选中文档的该字段值将被清空，矩形框内会显示 **空** 标识。
{% endhint %}

-   **新增元数据字段：** 如果你需要为选中的文档添加新的元数据字段，可以点击弹窗正下方的 **+添加元数据** 按钮，在弹出的弹窗中 **新建字段、添加已创建的字段** 或 **管理已创建的字段**。

-   **删除元数据字段：** 通过点击每条元数据字段旁边的 **删除** 标识，你可以删除所有选中文档的该字段。

-   **选择是否将操作应用于所有选中的文档：** 通过界面底部的选框，你可以选择是否将编辑后的元数据内容应用于所有选中的文档。

##### 批量新增元数据信息

1.  在 **编辑元数据** 弹窗中点击底部的 **+添加元数据** 按钮，弹出操作弹窗。
![add_metadata](https://assets-docs.dify.ai/2025/03/868f51bbd6893e32bf23952c6d0aa079.png)

    -  如需为选中文档新建字段，可以点击弹窗下方的 **+新建元数据** 按钮，并参考前文的 **新建元数据字段** 章节新建字段。
    
     > 在 **编辑元数据** 弹窗中新建的元数据字段，将自动同步至知识库字段列表中。

    ![new_metadata_field](https://assets-docs.dify.ai/2025/03/e32211f56421f61b788943ba40c6959e.png)

    -  如需为选中文档添加已创建的字段：

        -   可以从下拉列表中选择已有的字段，添加到字段列表中。

        -   可以在 **搜索元数据** 搜索框中搜索你需要的字段，添加到该文档的字段列表中。
    
    ![existing_field](https://assets-docs.dify.ai/2025/03/ea9aab2c4071bf2ec75409b05725ac1f.png)
    
    -  如需管理已创建的字段，可以点击该弹窗右下角的 **管理** 按钮，跳转到知识库的管理界面。

    ![manage_field](https://assets-docs.dify.ai/2025/03/82561edeb747b100c5295483c6238ffa.png)

2.  *（可选）* 新增字段后，在字段值框内填写该字段相应的字段值。
![value_for_field](https://assets-docs.dify.ai/2025/03/34c77cbf60fa524456aa8f3df8d7a576.png)

    -  如果值类型为 **时间**，在填写字段值时会弹出时间选择器，供你选择具体时间。

    ![date_picker](https://assets-docs.dify.ai/2025/03/8c991925c204703a4dceab42a23d684e.png)

3.  点击 **保存** 按钮，保存操作。

##### 批量删改元数据信息

1.  在 **编辑元数据** 弹窗中删改元数据信息：

    -   **添加字段值：** 在需要添加元数据值的字段框内直接输入所需值。

    -   **重置字段值：** 将光标悬停在字段名左侧的蓝色圆点上，蓝点将变为 **重置** 按钮。点击蓝点，将字段框内修改后的内容重置为原始元数据值。
    ![reset_values](https://assets-docs.dify.ai/2025/03/01c0cde5a6eafa48e1c6e5438fc2fa6b.png)

    -   **删除字段值：**
        -   删除一个字段值：在需要删除字段值的字段框内直接删除该字段值。

        -   删除多个字段值：点击 **多个值** 卡片的删除图标，清空所有选中文档的该元数据字段的值。

        ![multiple_values](https://assets-docs.dify.ai/2025/03/9cea5f8d4e2f1fb5bbd4812c875210f4.png)

    -   **删除单条元数据字段：** 点击字段最右侧的删除符号，删除该字段。删除后，该字段会被横线划掉且置灰。
    
        > 此操作仅会删除已选文档的该字段与字段值，字段本身依然保留在知识库中。
        
        ![delete_fields](https://assets-docs.dify.ai/2025/03/ed8c9143ba9a8eae6efcb76e309dbec1.png)

2.  点击 **保存** 按钮，保存操作。

##### 调整批量操作的应用范围

你可以使用 **编辑元数据** 弹窗左下角的 **应用于所有文档** 选框来调整编辑模式中改动的应用范围。

-   **否（默认）：** 如果不选中该选项，编辑模式中的改动仅对原本已有该元数据字段的文档生效，其他文档不会受到影响。

-   **是：** 如果选中该选项，编辑模式中的改动会对所有选中的文档生效。原本没有该字段的文档，会自动添加该字段。

![apply_all_changes](https://assets-docs.dify.ai/2025/03/4f95cdd2daef1cdbc63f8e249da71f1c.png)

#### 编辑单篇文档元数据信息

你可以在文档详情界面中编辑单篇文档的元数据信息。

##### 进入文档元数据编辑模式

1.  在文档详情界面，点击信息栏上方的 **开始标记** 按钮。

![details_page](https://assets-docs.dify.ai/2025/03/066cb8eaa89f6ec17aacd8b09f06771c.png)

2.  进入文档元数据编辑模式。

![start_labeling](https://assets-docs.dify.ai/2025/03/4806c56e324589e1711c407f6a1443de.png)

##### 新增文档元数据信息

1.  在文档的元数据编辑模式中，点击 **+添加元数据** 按钮，弹出操作弹窗。
![add_metadata](https://assets-docs.dify.ai/2025/03/f9ba9b10bbcf6eaca787eed4fcde44da.png)

    -  如需使用新建字段为该文档标记字段值，可以点击弹窗左下角的 **+ 新建元数据** 按钮，并参考前文的 **新建元数据字段** 章节新建字段。

    > 在文档页面新建的元数据字段，将自动同步至知识库字段列表中。
        
    ![new_fields](https://assets-docs.dify.ai/2025/03/739e7e51436259fca45d16065509fabb.png)

    -  如需使用知识库已有的字段为该文档标记字段值，可以选择下列任意一种方式使用已有的字段：

        -   从下拉列表中选择知识库已有的字段，添加到该文档的字段列表中。

        -   在 **搜索元数据** 搜索框中搜索你需要的字段，添加到该文档的字段列表中。
    
     ![existing_fields](https://assets-docs.dify.ai/2025/03/5b1876e8bc2c880b3b774c97eba371ab.png)

    -  如需管理知识库已有的字段，可以点击弹窗右下角的 **管理** 按钮，跳转到知识库的管理界面。

    ![manage_metadata](https://assets-docs.dify.ai/2025/03/8dc74a1d2cdd87294e58dbc3d6dd161b.png)


2.  *（可选）* 添加字段后，在字段名右侧的元数据栏中填写字段值。

![values_for_fields](https://assets-docs.dify.ai/2025/03/488107cbea73fd4583e043234fe2fd2e.png)

3.  点击右上角的 **保存** 按钮，保存字段值。

##### 删改文档元数据信息

1.  在文档的元数据编辑模式中，点击右上角的 **编辑** 按钮，进入编辑模式。

![edit_mode](https://assets-docs.dify.ai/2025/03/bb33a0f9c6980300c0f979f8dc0d274d.png)

2.  删改文档元数据信息：
    -  **删改字段值：** 在字段名右侧的字段值框内，删除或修改字段值。

    > 此模式仅支持修改字段值，不支持修改字段名。

    -  **删除字段：** 点击字段值框右侧的删除按钮，删除字段。

    > 此操作仅会删除该文档的该字段与字段值，字段本身依然保留在知识库中。

![edit_metadata](https://assets-docs.dify.ai/2025/03/4c0c4d83d3ad240568f316abfccc9c2c.png)

3.  点击右上角的 **保存** 按钮，保存修改后的字段信息。

## 如何使用元数据功能在知识库中筛选文档？

请参阅 [在应用内集成知识库](https://docs.dify.ai/zh-hans/guides/knowledge-base/integrate-knowledge-within-application) 中的 **使用元数据筛选知识** 章节。

## API 信息

请参阅 [通过 API 维护知识库](https://docs.dify.ai/zh-hans/guides/knowledge-base/knowledge-and-documents-maintenance/maintain-dataset-via-api)。

## FAQ

- **元数据有什么作用？**

    - 提升搜索效率：用户可以根据元数据标签快速筛选和查找相关信息，节省时间并提高工作效率。

    - 增强数据安全性：通过元数据设置访问权限，确保只有授权用户能访问敏感信息，保障数据的安全性。

    - 优化数据管理能力：元数据帮助企业或组织有效分类和存储数据，提高数据的管理和检索能力，增强数据的可用性和一致性。

    - 支持自动化流程：元数据在文档管理、数据分析等场景中可以自动触发任务或操作，简化流程并提高整体效率。

- **知识库元数据管理列表中的元数据字段和某篇文档中的元数据值有什么区别？**

<table style="width: 100%; border-collapse: collapse; background-color: #f8f9ff;">
    <thead>
        <tr>
            <th style="width: 25%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">/</th>
            <th style="width: 25%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">定义</th>
            <th style="width: 25%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">性质</th>
            <th style="width: 50%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">举例</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">元数据管理列表中的元数据字段</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">预定义的字段，用于描述文档的某些属性。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">全局性字段。所有文档都可以使用这些字段。</td>
           <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">作者、文档类型、上传日期。</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">某篇文档中的元数据值</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">每个文档按需标记的针对特定文档的信息。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">文档特定的值。每个文档根据其内容会标记不同的元数据值。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">文档 A 的“作者”字段值为“张三”，文档 B 的“作者”字段值为“李四”。</td>
        </tr>
    </tbody>
</table>

- **“在知识库管理界面删除某条元数据字段”“在编辑元数据弹窗中删除已选文档的某条元数据字段”和“在文档详情界面删除某条元数据字段”有什么区别？**

<table style="width: 100%; border-collapse: collapse; background-color: #fff;">
    <thead>
        <tr style="background-color: #f9fafb;">
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 15%;">操作方式</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 25%;">操作方法</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">示例图</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">影响范围</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">结果</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">在知识库管理界面删除某条元数据字段</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">在知识库管理界面，点击某条元数据字段右侧的删除图标，删除该字段。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">
                <img src="https://assets-docs.dify.ai/2025/03/13367a865d589a29b7c4098526fad5dc.png" alt="knowledge_base_delete" style="max-width: 100%; height: auto;">
            </td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">从知识库管理列表中完全删除该元数据字段及其所有字段值。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">该字段从知识库中移除，所有文档中的该字段及包含的所有字段值也会消失。</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">在编辑元数据弹窗中删除已选文档的某条元数据字段</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">在编辑元数据弹窗中，点击某条元数据字段右侧的删除图标，删除该字段。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">
                <img src="https://assets-docs.dify.ai/2025/03/ed8c9143ba9a8eae6efcb76e309dbec1.png" alt="bulk_delete" style="max-width: 100%; height: auto;">
            </td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">仅删除已选文档的该字段与字段值，字段本身依然保留在知识库管理列表中。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">选中文档中的字段与字段值被移除，但字段仍保留在知识库内，字段值计数会发生数值上的变化。</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">在文档详情界面删除某条元数据字段</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">在文档详情界面中的元数据编辑模式里，点击某条元数据字段右侧的删除图标，删除该字段。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">
                <img src="https://assets-docs.dify.ai/2025/03/19d7fe886dd30a3f3322fa2a87f87203.png" alt="single_delete" style="max-width: 100%; height: auto;">
            </td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">仅删除该文档的该字段与字段值，字段本身依然保留在知识库管理列表中。</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">该文档中的字段与字段值被移除，但字段仍保留在知识库内，字段值计数会发生数值上的变化。</td>
        </tr>
    </tbody>
</table>

- **我可以在知识库管理界面查看我设置的元数据值吗？**

目前，在知识库管理界面，你只能看到每条元数据字段的字段值计数（如“3 values”），无法查看字段值的具体内容。

如果你需要查看字段值的具体内容，可以在单个文档的详情界面中查看。

- **我可以在编辑元数据弹窗中删除单个元数据值吗？**

在 **编辑元数据弹窗** 中，你只能删除 **多个值** 卡片。删除该卡片将清空所有选中文档的该元数据字段的值。

如果你想删除单个元数据值，你需要进入对应文档的详情界面，并参照前文的 **编辑单篇文档的元数据值 > 删改文档元数据信息值** 章节进行操作。