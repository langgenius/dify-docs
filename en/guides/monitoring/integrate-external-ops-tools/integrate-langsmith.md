# Integrating LangSmith

### 1. What is LangSmith

LangSmith is a platform for building production-grade LLM applications. It is used for developing, collaborating, testing, deploying, and monitoring LLM applications.

{% hint style="info" %}
Introduction to LangSmith: [https://www.langchain.com/langsmith](https://www.langchain.com/langsmith)
{% endhint %}

***

### 2. How to Configure LangSmith

1. Register and log in to LangSmith on the [official website](https://www.langchain.com/langsmith)
2. Create a project in LangSmith. After logging in, click **New Project** on the homepage to create your own project. The **project** will be used to associate with **applications** in Dify for data monitoring.

<figure><img src="../../../.gitbook/assets/image (3).png" alt=""><figcaption><p>Create a project in LangSmith</p></figcaption></figure>

Once created, you can view all created projects in the Projects section.

<figure><img src="../../../.gitbook/assets/image (7).png" alt=""><figcaption><p>View created projects in LangSmith</p></figcaption></figure>

3. Create project credentials. Find the project settings **Settings** in the left sidebar.

<figure><img src="../../../.gitbook/assets/image (8).png" alt=""><figcaption><p>Project settings</p></figcaption></figure>

Click **Create API Key** to create project credentials.

<figure><img src="../../../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>Create a project API Key</p></figcaption></figure>

Select **Personal Access Token** for subsequent API authentication.

<figure><img src="../../../.gitbook/assets/image (5).png" alt=""><figcaption><p>Create an API Key</p></figcaption></figure>

Copy and save the created API key.

<figure><img src="../../../.gitbook/assets/image (9).png" alt=""><figcaption><p>Copy API Key</p></figcaption></figure>

4. Configure LangSmith in the Dify application. Open the application you need to monitor, open **Monitoring** in the side menu, and select **Configure** on the page.

<figure><img src="../../../.gitbook/assets/image (11).png" alt=""><figcaption><p>Configure LangSmith</p></figcaption></figure>

After clicking configure, paste the **API Key** and **project name** created in LangSmith into the configuration and save.

<figure><img src="../../../.gitbook/assets/image (12).png" alt=""><figcaption><p>Configure LangSmith</p></figcaption></figure>

{% hint style="info" %}
The configured project name needs to match the project set in LangSmith. If the project names do not match, LangSmith will automatically create a new project during data synchronization.
{% endhint %}

Once successfully saved, you can view the monitoring status on the current page.

<figure><img src="../../../.gitbook/assets/image (15).png" alt=""><figcaption><p>View configuration status</p></figcaption></figure>

### 3. Viewing Monitoring Data in LangSmith

After configuration, debugging or production data of the application in Dify can be viewed in LangSmith.

<figure><img src="../../../.gitbook/assets/image (17).png" alt=""><figcaption><p>Debugging applications in Dify</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (2).png" alt=""><figcaption><p>Viewing application data in LangSmith</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (18).png" alt=""><figcaption><p>Viewing application data in LangSmith</p></figcaption></figure>