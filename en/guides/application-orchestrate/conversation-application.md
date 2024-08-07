# Conversation Assistant

Conversation applications use a one-question-one-answer mode to have a continuous conversation with the user.
<!-- TODO CN IMG -->
### Applicable scenarios

Conversation applications can be used in fields such as customer service, online education, healthcare, financial services, etc. These applications can help organizations improve work efficiency, reduce labor costs, and provide a better user experience.

### How to compose

Conversation applications supports: prompts, variables, context, opening remarks, and suggestions for the next question.

Here, we use a interviewer application as an example to introduce the way to compose a conversation applications.

#### Step 1 Create an application

Click the "Create Application" button on the homepage to create an application. Fill in the application name, and select **"Chat App"** as the application type.

<figure><img src="../../../img/chat-app.png" alt=""><figcaption><p>Create Application</p></figcaption></figure>

#### Step 2: Compose the Application

After the application is successfully created, it will automatically redirect to the application overview page. Click on the button on the left menu: **"Orchestrate"** to compose the application.

<figure><img src="../../../img/compose-the-app.png" alt=""><figcaption></figcaption></figure>

**2.1 Fill in Prompts**

Prompt phrases are used to guide AI in providing professional responses, making the replies more precise. You can utilize the built-in prompt generator to craft suitable prompts. Prompts support the insertion of form variables, such as `{{input}}`. The values in the prompt variables will be replaced with the values filled in by the user.

Example:

1. Enter the interview scenario command.
2. The prompt will automatically generate on the right side content box.
3. You can insert custom variables within the prompt to tailor it to specific needs or details.

For a better experience, we will add an opening dialogue: `"Hello, {{name}}. I'm your interviewer, Bob. Are you ready?"`

To add the opening dialogue, click the "Add Feature" button in the upper left corner, and enable the "Conversation remarkers" feature:

<figure><img src="../../../img/conversation-remarkers.png" alt=""><figcaption></figcaption></figure>

And then edit the opening remarks:

![](../../../img/conversation-options.png)

**2.2 Adding Context**

If an application wants to generate content based on private contextual conversations, it can use our [knowledge](../knowledge-base/) feature. Click the "Add" button in the context to add a knowledge base.

![](../../../img/context.png)

**2.3 Debugging**

Enter user inputs on the right side and check the respond content.

![](../../../img/debug.png)

If the results are not satisfactory, you can adjust the prompts and model parameters. Click on the model name in the upper right corner to set the parameters of the model:

![](../../../img/adjust-model-parameters.png)

**Debugging with multiple models:**

If debugging with a single model feels inefficient, you can utilize the **Debug as Multiple Models** feature to batch-test the models’ response effectiveness.

![](../../../img/multiple-models.png)

Supports adding up to 4 LLMs at the same time.

![](../../../img/multiple-models-2.png)

> ⚠️ When using the multi-model debugging feature, if only some large models are visible, it is because other large models’ keys have not been added yet. You can manually add multiple models’ keys in [“Add New Provider”](https://docs.dify.ai/guides/model-configuration/new-provider).

**2.4 Publish App**

After debugging your application, click the **"Publish"** button in the top right corner to create a standalone AI application. In addition to experiencing the application via a public URL, you can also perform secondary development based on APIs, embed it into websites, and more. For details, please refer to [Publishing](https://docs.dify.ai/guides/application-publishing).

If you want to customize the application that you share, you can Fork our open source [WebApp template](https://github.com/langgenius/webapp-conversation). Based on the template, you can modify the application to meet your specific needs and style requirements.
