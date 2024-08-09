# External Data Tool

## Feature Introduction

Previously, the [.](./ "mention") feature allowed developers to directly upload various formats of long texts and structured data to build datasets, enabling AI applications to engage in conversations based on the latest context provided by the user.

With this update, the **External Data Tool** empowers developers to use their own search capabilities or internal knowledge bases as external data for the LLM's context. This is achieved by extending the API to retrieve and embed external data into prompts. Compared to uploading datasets to the cloud, using the **External Data Tool** offers significant advantages in ensuring private data security, customizing searches, and accessing real-time data.

## Implementation Details

When an end-user makes a request to the dialogue system, the platform's backend will trigger the external data tool (i.e., call its own API). It will query external information related to the user's question, such as employee profiles or real-time records, and return relevant parts via the API. The platform's backend will assemble the returned results into text and inject it into the prompt as context to provide more personalized and user-need-aligned responses.

## Operating Instructions

1. Before using the external data tool, you need to prepare an API and an API Key for authentication. Please read [External Data Tool](https://docs.dify.ai/guides/extension/api-based-extension/external-data-tool)
2. Dify provides centralized API management. After adding the API extension configuration in the settings interface, it can be used directly in various applications on Dify.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/api_based.png" alt=""><figcaption><p>API-based Extension</p></figcaption></figure>

3. For example, to "query the weather," enter the name, API endpoint, and API Key in the "Add API-based Extension" dialog box. After saving, we can call the API.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/weather inquiry.png" alt=""><figcaption><p>Weather Inquiry</p></figcaption></figure>

4. On the prompt orchestration page, click the "+ Add" button next to "Tools." In the opened "Add Tool" dialog box, fill in the name and variable name (the variable name will be referenced in the prompt, please fill in English), and select the API-based extension added in step 2.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/api_based_extension1.png" alt=""><figcaption><p>External_data_tool</p></figcaption></figure>

5. In this way, we can assemble the queried external data into the prompt. For example, to query today's weather in London, you can add the `location` variable, input "London," combine it with the external data tool's extension variable name `weather_data`, and the debug output will be as follows:

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/Weather_search_tool.jpeg" alt=""><figcaption><p>Weather_search_tool</p></figcaption></figure>

In the dialogue logs, we can also see the real-time data returned by the API:

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/log.jpeg" alt="" width="335"><figcaption><p>Prompt Log</p></figcaption></figure>