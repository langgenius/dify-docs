# Sync from Notion

Dify knowledge supports importing from Notion and setting up **Sync** so that data is automatically synced to Dify after updates in Notion.

### Authorization verification

1. When creating a knowledge base, select the data source, click **Sync from Notion--Go to connect**, and complete the authorization verification according to the prompt.
2. You can also: click **Settings--Data Sources--Add a Data Source**, click Notion Source **Connect** to complete authorization verification.

<figure><img src="../../.gitbook/assets/notion-connect.png" alt=""><figcaption><p>Connect Notion</p></figcaption></figure>

### Import Notion data

After completing authorization verification, go to the knowledge creation page, click **Sync from Notion**, and select the required authorization page to import.

### Segmentation and cleaning

Next, select your **segmentation settings** and **indexing method**, **save and process**. Wait for Dify to process this data, usually this step requires token consumption in LLM providers. Dify not only supports importing ordinary page types but also summarizes and saves the page attributes under the database type.

_**Note: Images and files are not currently supported for import. Table data will be converted to text.**_

### Sync Notion data

If your Notion content has been modified, you can click Sync directly on the Dify knowledge document list page to sync the data with one click(Please note that each time you click, the current content will be synchronized). This step requires token consumption.

<figure><img src="../../.gitbook/assets/sync-notion-data.png" alt=""><figcaption><p>Sync Notion data</p></figcaption></figure>

### (Community Edition) Notion Integration Configuration Guide

Notion integration is divided into two ways: **internal integration** and **public integration** . It can be configured in Dify on demand.

For the specific differences between the two integration methods, please refer to the [official doc of Notion](https://developers.notion.com/docs/authorization).

#### 1. **Use internal integration**

Create an integration in your [integration's settings](https://www.notion.so/my-integrations) page. By default, all integrations start with an internal integration; internal integrations will be associated with a workspace of your choice, so you need to be the workspace owner to create an integration.

**Specific operation steps:**

Click the " **New integration** " button, the type is Internal by default (cannot be modified), select the associated space, enter the name and upload the logo, and click "**Submit**" to create the integration successfully.

<figure><img src="../../.gitbook/assets/image (4) (1) (1).png" alt=""><figcaption></figcaption></figure>

Once the integration is created, you can update its settings as needed under the **Capabilities** tab and click the "**Show**" button under **Secrets** and then copy the Secrets.

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Copy it and back to the Dify source code , in the **.env** file configuration related environment variables, environment variables as follows:

**NOTION\_INTEGRATION\_TYPE** = internal or **NOTION\_INTEGRATION\_TYPE** = public

**NOTION\_INTERNAL\_SECRET**=you-internal-secret

#### 2. **Use public integration**

**You need to upgrade the internal integration to public integration** , navigate to the integrated Distribution page, and toggle the switch to expose the integration.

To toggle the switch to public settings, you need to **fill in additional information in the Organization Information** form below, including your company name, website, and Retargeting URL, and click the "Submit" button.

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

After your integration has been successfully made public in your [integration’s settings page](https://www.notion.so/my-integrations), you will be able to access the integration’s secrets in the Secrets tab.

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Back to the Dify source code , in the **.env** file configuration related environment variables , environment variables as follows:

**NOTION\_INTEGRATION\_TYPE**=public

**NOTION\_CLIENT\_SECRET**=you-client-secret

**NOTION\_CLIENT\_ID**=you-client-id

Once configured, you will be able to utilize Notion data import and sync functions in the knowledge section.
