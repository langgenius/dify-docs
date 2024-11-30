# Introduction

## What are Plugins?

The plugin is a developer-friendly extension module that simplifies development with lower entry barriers. It empowers developers with the flexibility to enhance the Dify platform through creative and customizable methods.

Sharing plugins is also made simple and accessible. You can distribute your plugins via the Dify Marketplace, GitHub, or as standalone files, allowing other developers to install and use them efficiently.

Whether you’re integrating new models, adding specialized tools, or extending Dify’s features, the plugin marketplace provides all the resources you need. **We warmly invite developers to contribute to the Dify ecosystem and get profit from it**.

Whether you’re integrating new models, adding specialized tools, or extending Dify’s features, the plugin marketplace offers all the resources you need. **We warmly invite developers to contribute to the Dify ecosystem and benefit from it**.

## Plugin Types

Plugins include these four types:

* **Model**
Integration plugins for various LLMs, including mainstream model providers and services, support configuration and invocation.
* **Tool**
External tools that can be used by Chatflow / Workflow / Agent applications, such as third-party APIs. These are typically functional components and integration tools that help improve application development efficiency.
* **Extension**
Provides endpoint capabilities only. For more details about the developing process, please refer to [here]().
* **Bundle**
A bundle is a combination of multiple plugins. Installing a bundle allows batch installation of pre-selected plugins, eliminating the tedious process of manual individual plugin installation.
For development methods of different plugin types, please refer to Plugin Development.

Plugin Features
Compared to existing tools or models, the plugin system introduces these new features:
* **Enhanced LLM Multimodal Capabilities**
The plugin system enhances LLM's ability to process multimedia content. Developers can use plugins to assist LLM in completing tasks like image processing and video processing, including but not limited to image cropping, background processing, and portrait image processing.
* **Rich Parameter System**
Previously, tool development only supported basic data types like `string`, `number`, `boolean` for parameters and `credential` types. Two new parameter types have been added to simplify plugin integration with LLMs and applications:
   * `app-selector`: For directly selecting and calling a Dify application within plugins
   * `model-selector`: For selecting and using LLMs within plugins to enhance plugin capabilities with AI.
* **Developer-Friendly Debugging**
The plugin system provides comprehensive development and debugging support:
   * Supports mainstream IDEs and debugging tools - just configure some simple environment variables to remotely connect to a Dify instance. Even supports connecting to Dify's SaaS service, where any plugin operations in Dify will be forwarded to your local environment
* **Persistent Data Storage**
To support complex application scenarios, the plugin system provides data persistence capabilities:
   * Plugin-level data storage
      * Workspace-level data sharing
      * Built-in data management mechanisms
These enable plugins to reliably save and manage application data, supporting more complex business scenarios.
* **Convenient Reverse Calling**
The plugin system provides bi-directional interaction capabilities. Through the SDK, plugins can actively call Dify's core functions, including:
   * AI model invocation
   * Tool usage
   * Application access
   * Knowledge base interaction
   * Function node calls (like question classification, parameter extraction, etc.)
This bi-directional calling mechanism gives plugins more powerful integration capabilities.
* **More Freedom in Custom API Interfaces (Endpoint Extensions)**
In addition to Dify's original Service APIs (like Chatbot application API, Workflow application API, etc.), the plugin system adds custom API capabilities. Developers can create new API endpoints based on business requirements to implement custom logic for data processing and request handling.

Dify Plugin Marketplace: A Collaborative Ecosystem
With the launch of the plugin module, we're introducing the **Dify Plugin Marketplace** to better collect and showcase useful plugins, providing rich extension capabilities for your AI application development journey.

Whether you want to integrate new models, add specific tools, or extend Dify's existing functionality, you can find the required resources in the plugin marketplace.

Quick Start: Installing and Using Plugins
This section demonstrates how to quickly install and use plugins, using a "Tool" type plugin as an example.

Finding and Installing Plugins
Visit the "Tools" page to see plugins installed in your current Workspace and system-recommended plugins.

You can search for plugins using tags or the search box. If you can't find a useful tool, click "Plugins" in the top right corner to go to the Marketplace for installation.

Additionally, you can install through these two methods:
Github
Local file upload
For detailed instructions, please refer to Installing Plugins.

Using Plugins
After installation, you can use plugins in Chatflow / Workflow / Agent applications. Some plugins require API authorization after installation before use. For detailed instructions, please click the following documentation links:
Using Plugins in Workflow / Chatflow Applications
Using Tool Plugins in Agents

Developing Plugins
If you're a developer, please refer to Plugin Development. After development, you can import and use the plugin locally.

Publishing Plugins
To publish plugins to the Dify Marketplace, please follow the guidelines to complete plugin information and related documentation. Submit the plugin code to the Github repository - after review, it will be listed in the plugin marketplace.

Besides publishing to official Dify channels, you can also publish to personal Github projects or share as file packages. For detailed instructions, please refer to Publishing Plugins.