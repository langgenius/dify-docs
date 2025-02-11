# Initialize Development Tools

Before start to develop Dify plugins please prepare the following prerequisites:

* Dify plugin scaffolding tool
* Python environment, version ≥ 3.12

### **1. Installing the Dify Plugin Development Scaffolding Tool**

> The Dify plugin development scaffolding tool, also known as `dify-plugin-daemon`, can be regarded as a plugin development SDK.

Visit the [Dify plugin GitHub page](https://github.com/langgenius/dify-plugin-daemon/releases) and select and download the version suitable for your operating system.

Using **macOS with M-series chips** as an example: Download the `dify-plugin-darwin-arm64` file from the project address mentioned above. Then, in the terminal, navigate to the file's location and grant it execution permissions:

```
chmod +x dify-plugin-darwin-arm64
```

Run the following command to verify successful installation.

```
./dify-plugin-darwin-arm64 version
```

> If the system shows an "Apple cannot verify" error, go to **Settings → Privacy & Security → Security**, and click the "Open Anyway" button.

After running the command, the installation is successful, if the terminal returns version information like `v0.0.1-beta.15`.

{% hint style="info" %}
**Tips:**

If you want to use the `dify` command globally in your system to run the scaffolding tool, it's recommended to rename the binary file to `dify` and copy it to the `/usr/local/bin` system path.

After configuration, entering the `dify version` command in the terminal will output the version number.

<img src="https://assets-docs.dify.ai/2025/01/74e57a57c1ae1cc70f4a45084cbbb37e.png" alt="" data-size="original">
{% endhint %}

### **2. Initialize Python Environment**

For detailed instructions, please refer to the [Python installation](https://pythontest.com/python/installing-python-3-11/) tutorial, or ask the LLM for complete installation instructions.

### 3. **Develop plugins**

Please refer to the following content for examples of different types of plugin development.

{% content-ref url="tool-plugin.md" %}
[tool-plugin.md](tool-plugin.md)
{% endcontent-ref %}

{% content-ref url="model-plugin/" %}
[model-plugin](model-plugin/)
{% endcontent-ref %}

{% content-ref url="agent-strategy.md" %}
[agent-strategy.md](agent-strategy.md)
{% endcontent-ref %}

{% content-ref url="extension-plugin.md" %}
[extension.md](extension-plugin.md)
{% endcontent-ref %}

{% content-ref url="bundle.md" %}
[bundle.md](bundle.md)
{% endcontent-ref %}