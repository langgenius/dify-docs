# Integrating Langfuse

### 1. What is Langfuse

Langfuse is an open-source LLM engineering platform that helps teams collaborate on debugging, analyzing, and iterating their applications.

{% hint style="info" %}
Introduction to Langfuse: [https://langfuse.com/](https://langfuse.com/)
{% endhint %}

***

### 2. How to Configure Langfuse

1. Register and log in to Langfuse on the [official website](https://langfuse.com/)
2. Create a project in Langfuse. After logging in, click **New** on the homepage to create your own project. The **project** will be used to associate with **applications** in Dify for data monitoring.

<figure><img src="../../../.gitbook/assets/image (249).png" alt=""><figcaption><p>Create a project in Langfuse</p></figcaption></figure>

Edit a name for the project.

<figure><img src="../../../.gitbook/assets/image (251).png" alt=""><figcaption><p>Create a project in Langfuse</p></figcaption></figure>

3. Create project API credentials. In the left sidebar of the project, click **Settings** to open the settings.

<figure><img src="../../../.gitbook/assets/image (253).png" alt=""><figcaption><p>Create project API credentials</p></figcaption></figure>

In Settings, click **Create API Keys** to create project API credentials.

<figure><img src="../../../.gitbook/assets/image (252).png" alt=""><figcaption><p>Create project API credentials</p></figcaption></figure>

Copy and save the **Secret Key**, **Public Key**, and **Host**.

<figure><img src="../../../.gitbook/assets/image (254).png" alt=""><figcaption><p>Get API Key configuration</p></figcaption></figure>

4. Configure Langfuse in Dify. Open the application you need to monitor, open **Monitoring** in the side menu, and select **Configure** on the page.

<figure><img src="../../../.gitbook/assets/image (255).png" alt=""><figcaption><p>Configure Langfuse</p></figcaption></figure>

After clicking configure, paste the **Secret Key, Public Key, Host** created in Langfuse into the configuration and save.

<figure><img src="../../../.gitbook/assets/image (256).png" alt=""><figcaption><p>Configure Langfuse</p></figcaption></figure>

Once successfully saved, you can view the status on the current page. If it shows as started, it is being monitored.

<figure><img src="../../../.gitbook/assets/image (257).png" alt=""><figcaption><p>View configuration status</p></figcaption></figure>

***

### 3. Viewing Monitoring Data in Langfuse

After configuration, debugging or production data of the application in Dify can be viewed in Langfuse.

<figure><img src="../../../.gitbook/assets/image (259).png" alt=""><figcaption><p>Debugging applications in Dify</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (258).png" alt=""><figcaption><p>Viewing application data in Langfuse</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image.png" alt=""><figcaption><p>Viewing application data in Langfuse</p></figcaption></figure>