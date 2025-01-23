# Introduction

### **Introduction to Plugins**

Third-party models and tools are vital components that help developers enhance their applications. Although the Dify platform includes multiple tools developed and maintained by Dify teams and community contributors, these existing tools in their current form struggle to comprehensively address the diverse needs of various specialized scenarios. Additionally, developing new tools and integrating them into the Dify platform requires a lengthy process.

A better approach is to cultivate an open ecosystem, enabling every developer to easily create their own tools.

Introducing the all-new Plugins—a more developer-friendly and highly extensible third-party service extension module. The new plugin system breaks free from the limitations of the original framework, offering richer and more powerful extension capabilities. It provides four types of plugins, each tailored to mature scenario-based solutions, giving developers endless creative opportunities to transform Dify applications.

Moreover, the plugin system features more user-friendly distribution options. You can share your plugins through the [Dify Marketplace](publish-plugins/publish-to-dify-marketplace.md), [GitHub](publish-plugins/publish-plugin-on-personal-github-repo.md), or as [local files](publish-plugins/package-and-publish-plugin-file.md), allowing other developers to conveniently install them.

Whether you want to integrate new models or add specific tools to expand the existing functionalities of the Dify platform, you can find the necessary resources in the extensive plugin marketplace. **We hope more developers will join in building the Dify ecosystem and reap its benefits.**

> To experience the plugin's functionality in the Community Edition, please upgrade the version number to v1.0.0.

<figure><img src="https://assets-docs.dify.ai/2025/01/83f9566063db7ae4886f6a139f3f81ff.png" alt=""><figcaption></figcaption></figure>

### **Plugin Types**

Plugins include the following four types:

*   **Models**

    Integration plugins for various AI models, including mainstream service providers and custom models. These plugins support configuration and invocation, focusing on LLM API service requests. For details about model plugin development, please refer to [Quick Start: Model Type Plugins](develop-plugins/model-plugin/).
*   **Tools**

    External tools usable in Chatflow, Workflow, or Agent applications, offering comprehensive toolsets and API implementation capabilities. These plugins enable both calling existing tools and building custom endpoints. For example, when developing a Discord Bot, you can utilize available tools and create custom endpoints for message handling. For more details about tool plugin development, please refer to [Quick Start: Tool Type Plugins](develop-plugins/tool-plugin.md).
*   **Agent Strategy**

    The Agent Strategy plugin defines the reasoning and decision-making logic within an Agent node, including tool selection, invocation, and result processing.
*   **Extensions**

    A lightweight solution for simple scenarios, providing only endpoint capabilities. These plugins enable quick feature extensions through HTTP services, ideal for basic API requesting integrations.

    For more details on developing extension plugins, refer to [Quick Start: Extension Type Plugins](develop-plugins/extension-plugin.md).
*   **Bundle**

    A bundle combines multiple plugins into a single set for batch installation, streamlining the process and eliminating the need for manual installations.

    For more details on developing bundles, refer to Plugin Development: [Bundle Type Plugins](develop-plugins/bundle.md).

### **Plugin Features**

Compared to existing tools or models, the plugin system introduces the following new features:

*   **Enhanced LLM Multimodal Capabilities**

    The plugin system enhances LLM capabilities for processing multimedia content. Developers can leverage plugins to enable tasks such as image processing, video processing, and more, including functionalities like image cropping, background editing, and portrait processing.
*   **Developer-Friendly Debugging Capabilities**

    The plugin system offers robust development and debugging support:

    * Compatible with mainstream IDEs and debugging tools, requiring minimal environment variable configuration for remote connection to a Dify instance.
    * Supports integration with Dify’s SaaS service, forwarding all plugin-related operations performed in Dify directly to your local environment.
*   **Persistent Data Storage**

    To accommodate complex application scenarios, the plugin system offers data persistence storage capabilities:

    * Plugin-level data storage
      * Workspace-level data sharing
      * Built-in data management mechanisms This enables plugins to reliably save and manage application data, supporting more complex business scenarios.
*   **Convenient Reverse Invoking**

    The plugin system provides bi-directional interaction capabilities. Through SDK, plugins can actively call Dify's core functions, including:

    * AI model calls
      * Tool usage
      * Application access
      * Knowledge base interaction
      * Function node calls (such as question classification, parameter extraction, etc.) This bi-directional calling mechanism gives plugins more powerful function integration capabilities.
*   **More Flexability in Custom API Endpoints (Endpoint Extensions)**

    In addition to Dify’s native application APIs (such as the Chatbot and Workflow APIs), the plugin system introduces custom API capabilities. Developers can create new API endpoints tailored to business needs, enabling custom logic for data processing, request handling, and more.

### **Dify Marketplace: A Co-created Ecosystem**

Dify Marketplace is an open ecosystem for developers, offering a rich collection of resources such as models, tools, AI Agents, Extensions, and plugin packages. Through the Marketplace, you can seamlessly integrate third-party services into your existing Dify applications, enhancing their capabilities and contributing to the growth of the Dify ecosystem.

For details on how to publish plugins to the Dify Marketplace, please refer to the following:

{% content-ref url="publish-plugins/publish-to-dify-marketplace.md" %}
[publish-to-dify-marketplace.md](publish-plugins/publish-to-dify-marketplace.md)
{% endcontent-ref %}

### **Quick Start**

If you want to quickly install and use the plugin, please refer to the following documentation:

{% content-ref url="quick-start/install-and-use-plugins.md" %}
[install-and-use-plugins.md](quick-start/install-and-use-plugins.md)
{% endcontent-ref %}

If you want to get started with plugin development, please refer to the following documentation:

{% content-ref url="develop-plugins/" %}
[develop-plugins](develop-plugins/)
{% endcontent-ref %}

### **Publishing Plugins**

If you want to publish your plugin to the [Dify Marketplace](https://marketplace.dify.ai/), please follow the guidelines to complete the plugin information and related documentation. Submit the plugin code to the [GitHub repository](https://github.com/langgenius/dify-official-plugins), and it will be listed in the plugin marketplace after review approval.

{% content-ref url="publish-plugins/publish-to-dify-marketplace.md" %}
[publish-to-dify-marketplace.md](publish-plugins/publish-to-dify-marketplace.md)
{% endcontent-ref %}

Besides publishing to official Dify channels, you can also publish to personal GitHub projects or share as file packages. For detailed instructions, please refer to "Publishing Plugins".

{% content-ref url="publish-plugins/publish-plugin-on-personal-github-repo.md" %}
[publish-plugin-on-personal-github-repo.md](publish-plugins/publish-plugin-on-personal-github-repo.md)
{% endcontent-ref %}

{% content-ref url="publish-plugins/package-and-publish-plugin-file.md" %}
[package-and-publish-plugin-file.md](publish-plugins/package-and-publish-plugin-file.md)
{% endcontent-ref %}





