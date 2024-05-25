# 代码扩展

对于本地部署 Dify 的开发者，如果想实现扩展能力，无需重新写一个 API 服务，可以使用代码扩展，即在 Dify 功能的基础上，以代码形式扩展或增强程序的能力（即插件能力），而不破坏 Dify 原有代码逻辑。它遵循一定的接口或规范，以实现与主程序的兼容和可插拔性。 目前，Dify 开放了两种代码扩展，分别为：

* 新增一种新的外部数据工具类型 [external\_data\_tool.md](external\_data\_tool.md "mention")
* 扩展敏感内容审查策略 [moderation.md](moderation.md "mention")

可在上述功能的基础上，遵循代码层 interface 的规范，来实现横向扩展的目的。如果你愿意将扩展功能贡献给我们的话，非常欢迎给 Dify 提交 PR。

## 前端组件规范定义

代码扩展的前端样式通过 `schema.json` 定义：

* label：自定义类型名称，支持系统语言切换
* form\_schema：表单内容列表
  * type：组件类型
    * select：下拉选项
    * text-input：文本
    * paragraph：段落
  * label：组件名称，支持系统语言切换
  * variable：变量名称
  * required：是否必填
  * default：默认值
  * placeholder：组件提示内容
  * options：组件「select」专有属性，定义下拉内容
    * label：下拉名称，支持系统语言切换
    * value：下拉选项值
  * max\_length：组件「text-input」专有属性，最大长度

### 模版样例

```json
{
    "label": {
        "en-US": "Cloud Service",
        "zh-Hans": "云服务"
    },
    "form_schema": [
        {
            "type": "select",
            "label": {
                "en-US": "Cloud Provider",
                "zh-Hans": "云厂商"
            },
            "variable": "cloud_provider",
            "required": true,
            "options": [
                {
                    "label": {
                        "en-US": "AWS",
                        "zh-Hans": "亚马逊"
                    },
                    "value": "AWS"
                },
                {
                    "label": {
                        "en-US": "Google Cloud",
                        "zh-Hans": "谷歌云"
                    },
                    "value": "GoogleCloud"
                },
                {
                    "label": {
                        "en-US": "Azure Cloud",
                        "zh-Hans": "微软云"
                    },
                    "value": "Azure"
                }
            ],
            "default": "GoogleCloud",
            "placeholder": ""
        },
        {
            "type": "text-input",
            "label": {
                "en-US": "API Endpoint",
                "zh-Hans": "API Endpoint"
            },
            "variable": "api_endpoint",
            "required": true,
            "max_length": 100,
            "default": "",
            "placeholder": "https://api.example.com"
        },
        {
            "type": "paragraph",
            "label": {
                "en-US": "API Key",
                "zh-Hans": "API Key"
            },
            "variable": "api_keys",
            "required": true,
            "default": "",
            "placeholder": "Paste your API key here"
        }
    ]
}
```
