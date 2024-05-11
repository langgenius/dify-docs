# Moderation

In our interactions with AI applications, we often have stringent requirements in terms of content security, user experience, and legal regulations. At this point, we need the "Sensitive Word Review" feature to create a better interactive environment for end-users. On the prompt orchestration page, click "Add Function" and locate the "Content Review" toolbox at the bottom:

<figure><img src="../.gitbook/assets/content_moderation.png" alt=""><figcaption><p>Content moderation</p></figcaption></figure>

## Call the OpenAI Moderation API

OpenAI, along with most companies providing LLMs, includes content moderation features in their models to ensure that outputs do not contain controversial content, such as violence, sexual content, and illegal activities. Additionally, OpenAI has made this content moderation capability available, which you can refer to at [https://platform.openai.com/docs/guides/moderation/overview](https://platform.openai.com/docs/guides/moderation/overview).

Now you can also directly call the OpenAI Moderation API on Dify; you can review either input or output content simply by entering the corresponding "preset reply."

<figure><img src="../.gitbook/assets/moderation2.png" alt=""><figcaption><p>OpenAI Moderation</p></figcaption></figure>

## Keywords

Developers can customize the sensitive words they need to review, such as using "kill" as a keyword to perform an audit action when users input. The preset reply content should be "The content is violating usage policies." It can be anticipated that when a user inputs a text snippet containing "kill" at the terminal, it will trigger the sensitive word review tool and return the preset reply content.

<figure><img src="../.gitbook/assets/moderation3.png" alt=""><figcaption><p>Keywords</p></figcaption></figure>

## Moderation Extension

Different enterprises often have their own mechanisms for sensitive word moderation. When developing their own AI applications, such as an internal knowledge base ChatBot, enterprises need to moderate the query content input by employees for sensitive words. For this purpose, developers can write an API extension based on their enterprise's internal sensitive word moderation mechanisms, specifically referring to [moderation-extension.md](extension/api\_based\_extension/moderation-extension.md "mention"), which can then be called on Dify to achieve a high degree of customization and privacy protection for sensitive word review.

<figure><img src="../.gitbook/assets/moderation4.png" alt=""><figcaption><p>Moderation Extension</p></figcaption></figure>
