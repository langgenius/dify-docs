---
description: >-
  This document primarily introduces how to scrape data from a web page, parse
  it into Markdown, and import it into the Dify knowledge base.
---

# Sync Data from Website

Dify knowledge base supports crawling content from public web pages using third-party tools such as [Jina Reader](https://jina.ai/reader/) and [Firecrawl](https://www.firecrawl.dev/), parsing it into Markdown content, and importing it into the knowledge base.

{% hint style="info" %}
​[Firecrawl](https://www.firecrawl.dev/) and [Jina Reader](https://jina.ai/reader/) are both open-source web parsing tools that can convert web pages into clean Markdown format text that is easy for LLMs to recognize, while providing easy-to-use API services.Comment
{% endhint %}

The following sections will introduce the usage methods for Firecrawl and Jina Reader respectively.

### Firecrawl <a href="#how-to-configure" id="how-to-configure"></a>

#### **1. Configure Firecrawl API credentials**

Click on the avatar in the upper right corner, then go to the **DataSource** page, and click the **Configure** button next to Firecrawl.

<figure><img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FRncMhlfeYTrpujwzDIqw%2Fuploads%2FQ2CvvgqQXmsUMXZR4u8N%2Fimage.png?alt=media&#x26;token=f7273557-94f7-4250-adfe-8d2e11f6a307" alt=""><figcaption><p>Configuring Firecrawl Credentials</p></figcaption></figure>

Log in to the [Firecrawl website](https://www.firecrawl.dev/) to complete registration, get your API Key, and then enter and save it in Dify.

<figure><img src="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FRncMhlfeYTrpujwzDIqw%2Fuploads%2FtAwcLoAYT1A2v12pfJC3%2Fimage.png?alt=media&#x26;token=3b5b784f-2808-431f-8595-2638d038c190" alt=""><figcaption><p>Get the API Key and save it in Dify</p></figcaption></figure>

#### 2. Scrape target webpage

On the knowledge base creation page, select **Sync from website**, choose Firecrawl as the provider, and enter the target URL to be crawled.

<figure><img src="../../.gitbook/assets/image (102).png" alt=""><figcaption><p>Web scraping configuration</p></figcaption></figure>

The configuration options include: Whether to crawl sub-pages, Page crawling limit, Page scraping max depth, Excluded paths, Include only paths, and Content extraction scope. After completing the configuration, click **Run** to preview the parsed pages.

<figure><img src="../../.gitbook/assets/image (103).png" alt=""><figcaption><p>Execute scraping</p></figcaption></figure>

#### 3. Review import results

After importing the parsed text from the webpage, it is stored in the knowledge base documents. View the import results and click **Add URL** to continue importing new web pages.

<figure><img src="../../.gitbook/assets/image (104).png" alt=""><figcaption><p>Importing parsed web text into the knowledge base</p></figcaption></figure>

***

### Jina Reader

#### 1. Configuring Jina Reader Credentials&#x20;

Click on the avatar in the upper right corner, then go to the **DataSource** page, and click the **Configure** button next to Jina Reader.

<figure><img src="../../.gitbook/assets/image (105).png" alt=""><figcaption><p>Configuring Jina Reader</p></figcaption></figure>

Log in to the [Jina Reader website](https://jina.ai/reader/), complete registration, obtain the API Key, then fill it in and save.

<figure><img src="../../.gitbook/assets/image (106).png" alt=""><figcaption><p>Fill in Jina configuration</p></figcaption></figure>

#### 2. Using Jina Reader to Crawl Web Content&#x20;

On the knowledge base creation page, select Sync from website, choose Jina Reader as the provider, and enter the target URL to be crawled.

<figure><img src="../../.gitbook/assets/image (107).png" alt=""><figcaption><p>Web Crawling Configuration </p></figcaption></figure>

Configuration options include: whether to crawl subpages, maximum number of pages to crawl, and whether to use sitemap for crawling. After completing the configuration, click the **Run** button to preview the page links to be crawled.

<figure><img src="../../.gitbook/assets/image (109).png" alt=""><figcaption><p>Executing the Crawl</p></figcaption></figure>

Import the parsed text from web pages and store it in the knowledge base documents, then view the import results. To continue adding web pages, click the Add URL button on the right to import new web pages.

<figure><img src="../../.gitbook/assets/image (110).png" alt=""><figcaption><p>Importing parsed web text into the knowledge base</p></figcaption></figure>

After crawling is complete, the content from the web pages will be incorporated into the knowledge base.
