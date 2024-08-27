---
description: >-
  This document primarily introduces how to scrape data from a web page, parse
  it into Markdown, and import it into the Dify knowledge base.
---

# Sync Data from Website

Dify's knowledge base supports web scraping and parsing into Markdown for import through integration with Firecrawl.

{% hint style="info" %}
[Firecrawl](https://www.firecrawl.dev/) is an open-source web parsing tool that converts web pages into clean Markdown format text that LLMs easily recognize. It also provides an easy-to-use API service.&#x20;
{% endhint %}

### How to Configure

#### 1. Configure Firecrawl API credentials

First, you need to configure Firecrawl credentials in the **Data Source** section of the **Settings** page.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/sync-from-website/image (6).png" alt=""><figcaption><p>Configuring Firecrawl Credentials</p></figcaption></figure>

Log in to the [Firecrawl website](https://www.firecrawl.dev/) to complete registration, get your API Key, and then enter and save it in Dify.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/sync-from-website/image (7).png" alt=""><figcaption><p>Get the API Key and save it in Dify</p></figcaption></figure>

#### 2. Scrape target webpage

On the knowledge base creation page, select **Sync from website** and enter the URL to be scraped.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/sync-from-website/image (1).png" alt=""><figcaption><p>Web scraping configuration</p></figcaption></figure>

The configuration options include: Whether to crawl sub-pages, Page crawling limit, Page scraping max depth, Excluded paths, Include only paths, and Content extraction scope. After completing the configuration, click **Run** to preview the parsed pages.

<figure><img src="/en/.gitbook/assets/guides/knowledge-base/sync-from-website/image (2).png" alt=""><figcaption><p>Execute scraping</p></figcaption></figure>

#### 3. Review import results

After importing the parsed text from the webpage, it is stored in the knowledge base documents. View the import results and click **Add URL** to continue importing new web pages.

<figure><img src="../../../jp/.gitbook/assets/image (5).png" alt=""><figcaption><p>Importing parsed web text into the knowledge base</p></figcaption></figure>

