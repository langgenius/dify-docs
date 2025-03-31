# Tools

{% hint style="warning" %}
"Tools" has been fully upgraded to the "Plugins". Please refer to the [documentation](https://docs.dify.ai/plugins/introduction) for detailed information.
{% endhint %}

### Tool Definition

Tools can extend the capabilities of LLMs (Language Learning Models), such as performing web searches, scientific calculations, or generating images, thereby enhancing the LLM's ability to connect with the external world. Dify provides two types of tools: **First-party Tools** and **Custom Tools**.

You can directly use the first-party built-in tools provided by the Dify ecosystem, or easily import custom API tools (currently supporting OpenAPI / Swagger and OpenAI Plugin specifications).

#### Functions of Tools:

1. Tools allow users to create more powerful AI applications on Dify. For example, you can arrange suitable tools for an intelligent assistant application (Agent) that can complete complex tasks through task reasoning, step-by-step breakdown, and tool invocation.
2. They facilitate connecting your application with other systems or services and interacting with the external environment, such as code execution or access to proprietary information sources.

### How to Configure First-party Tools

<figure><img src="../../.gitbook/assets/first-party-tools.png" alt=""><figcaption><p>First-party Tools List</p></figcaption></figure>

Dify currently supports:

<table><thead><tr><th width="154">Tool</th><th>Description</th></tr></thead><tbody><tr><td>Google Search</td><td>Tool for performing Google SERP searches and extracting snippets and web pages. The input should be a search query.</td></tr><tr><td>Wikipedia</td><td>Tool for performing Wikipedia searches and extracting snippets and web pages.</td></tr><tr><td>DALL-E Drawing</td><td>Tool for generating high-quality images through natural language input.</td></tr><tr><td>Web Scraping</td><td>Tool for scraping web data.</td></tr><tr><td>WolframAlpha</td><td>A powerful computational knowledge engine that provides standardized answers based on questions and has strong mathematical computation capabilities.</td></tr><tr><td>Chart Generation</td><td>Tool for generating visual charts, allowing you to create bar charts, line charts, pie charts, and other types of charts.</td></tr><tr><td>Current Time</td><td>Tool for querying the current time.</td></tr><tr><td>Yahoo Finance</td><td>Tool for obtaining and organizing the latest financial information, such as news and stock quotes.</td></tr><tr><td>Stable Diffusion</td><td>A tool for generating images that can be deployed locally using stable-diffusion-webui.</td></tr><tr><td>Vectorizer</td><td>Tool for quickly and easily converting PNG and JPG images to SVG vector graphics.</td></tr><tr><td>YouTube</td><td>Tool for retrieving statistics of YouTube channel videos.</td></tr></tbody></table>

{% hint style="info" %}
We welcome you to contribute your developed tools to Dify. For detailed methods on how to contribute, please refer to the [Dify Development Contribution Documentation](https://github.com/langgenius/dify/blob/main/CONTRIBUTING.md). Your support is invaluable to us.
{% endhint %}

#### First-party Tool Authorization

If you need to use the first-party built-in tools provided by the Dify ecosystem, you need to configure the corresponding credentials before using them.

<figure><img src="../../.gitbook/assets/configure-first-party-tool-api.png" alt=""><figcaption><p>Configure First-party Tool Credentials</p></figcaption></figure>

Once the credentials are successfully verified, the tool will display an "Authorized" status. After configuring the credentials, all members in the workspace can use this tool when arranging applications.

### How to Create Custom Tools

You can import custom API tools in the "Tools - Custom Tools" section, currently supporting OpenAPI / Swagger and ChatGPT Plugin specifications. You can directly paste the OpenAPI schema content or import it from a URL. For the OpenAPI / Swagger specification, you can refer to the [official documentation](https://swagger.io/specification/).

Currently, tools support two authentication methods: No Authentication and API Key.

<figure><img src="../../.gitbook/assets/en-tools-create-customized-tools-1.png" alt=""><figcaption><p>Create Custom Tools</p></figcaption></figure>

After importing the schema content, the system will automatically parse the parameters in the file, and you can preview the specific parameters, methods, and paths of the tool. You can also test the tool parameters here.

<figure><img src="../../.gitbook/assets/en-tools-create-customized-tools-2.png" alt=""><figcaption><p>Custom Tool Parameter Testing</p></figcaption></figure>

Once the custom tool is created, all members in the workspace can use this tool when arranging applications in the "Studio."

<figure><img src="../../.gitbook/assets/en-tools-create-customized-tools-3.png" alt=""><figcaption><p>Custom Tool Added</p></figcaption></figure>

#### Cloudflare Workers

You can also use [dify-tools-worker](https://github.com/crazywoola/dify-tools-worker) to quickly deploy custom tools. This tool provides:

* Routes that can be imported into Dify `https://difytoolsworker.yourname.workers.dev/doc`, offering an OpenAPI-compatible interface documentation.
* API implementation code that can be directly deployed to Cloudflare Workers.

### How to Use Tools in Applications

Currently, you can use the configured tools when creating **intelligent assistant applications** in the "Studio."

<figure><img src="../../.gitbook/assets/use-tools-in-app.png" alt=""><figcaption><p>Add Tools When Creating Intelligent Assistant Applications</p></figcaption></figure>

For example, after adding tools in a financial analysis application, the intelligent assistant will autonomously invoke tools when needed to query financial report data, analyze the data, and complete the conversation with the user.

<figure><img src="../../.gitbook/assets/ai-using-tools-during-conversation.png" alt=""><figcaption><p>Intelligent Assistant Using Tools to Answer Questions During Conversation</p></figcaption></figure>
