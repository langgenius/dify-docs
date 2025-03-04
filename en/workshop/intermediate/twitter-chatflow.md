---
cover: ../../.gitbook/assets/%E7%94%BB%E6%9D%BF_1.png
coverY: 0
---

# Generating analysis of Twitter account using Chatflow Agent

## Introduction

In Dify, you can use some crawler tools, such as Jina, which can convert web pages into markdown format that LLMs can read.

Recently, [wordware.ai](https://www.wordware.ai/) has brought to our attention that we can use crawlers to scrape social media for LLM analysis, creating more interesting applications.

However, knowing that X (formerly Twitter) stopped providing free API access on February 2, 2023, and has since upgraded its anti-crawling measures. Tools like Jina are unable to access X's content directly.

> Starting February 9, we will no longer support free access to the Twitter API, both v2 and v1.1. A paid basic tier will be available instead 🧵
>
> — Developers (@XDevelopers) [February 2, 2023](https://twitter.com/XDevelopers/status/1621026986784337922?ref\_src=twsrc%5Etfw)

Fortunately, Dify also has an HTTP tool, which allows us to call external crawling tools by sending HTTP requests. Let's get started!

## **Prerequisites**

### Register Crawlbase

Crawlbase is an all-in-one data crawling and scraping platform designed for businesses and developers.

Moreover, using Crawlbase Scraper allows you to scrape data from social platforms like X, Facebook and Instagram.

Click to register: [crawlbase.com](https://crawlbase.com)

### Deploy Dify locally

Dify is an open-source LLM app development platform. You can choose cloud service or deploy it locally using docker compose.

In this article, If you don’t want to deploy it locally, register a free Dify Cloud sandbox account here: [https://cloud.dify.ai/signin](https://cloud.dify.ai/signin).

{% hint style="info" %}
Dify Cloud Sandbox users get 200 free credits, equivalent to 200 GPT-3.5 messages or 20 GPT-4 messages. 
{% endhint %}

The following are brief tutorials on how to deploy Dify:

#### Clone Dify

```bash
git clone https://github.com/langgenius/dify.git
```

#### **Start Dify**

```bash
cd dify/docker
cp .env.example .env
docker compose up -d
```

### Configure LLM Providers

Configure Model Provider in account setting:

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/19e05ce9a7929c53aab8cf003273ad23.webp" alt=""><figcaption></figcaption></figure>

## Create a chatflow

Now, let's get started on the chatflow.

Click on `Create from Blank` to start:

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/aa528b783dece180036e783f6bf653c9.webp" alt=""><figcaption></figcaption></figure>

The initialized chatflow should be like:

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/05d50d65ec1afbdda6512c92a558bca0.webp" alt=""><figcaption></figcaption></figure>

## Add nodes to chatflow

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/7e199ed86b86c24cca8903737e0d208d.webp" alt=""><figcaption><p>The final chatflow looks like this</p></figcaption></figure>

### Start node

In start node, we can add some system variables at the beginning of a chat. In this article, we need a Twitter user’s ID as a string variable. Let’s name it `id` .

Click on Start node and add a new variable:

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/72b447ae1577155940b76fb3c2d7f45b.webp" alt=""><figcaption></figcaption></figure>

### Code node

According to [Crawlbase docs](https://crawlbase.com/docs/crawling-api/scrapers/#twitter-profile), the variable `url` (this will be used in the following node) should be `https://twitter.com/` + `user id` , such as `https://twitter.com/elonmusk` for Elon Musk.

To convert the user ID into a complete URL, we can use the following Python code to integrate the prefix `https://twitter.com/` with the user ID:

```python
def main(id: str) -> dict:
    return {
        "url": "https://twitter.com/"+id,
    }
```

Add a code node and select python, and set input and output variable names:

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/4094f8ec4b9d2987a6ccc8a8ad64076a.webp" alt=""><figcaption></figcaption></figure>

### HTTP request node

Based on the [Crawlbase docs](https://crawlbase.com/docs/crawling-api/scrapers/#twitter-profile), to scrape a Twitter user’s profile in http format, we need to complete HTTP request node in the following format:

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/7607140220496c77e0cb84bb65871383.webp" alt=""><figcaption></figcaption></figure>

Importantly, it is best not to directly enter the token value as plain text for security reasons, as this is not a good practice. Actually, in the latest version of Dify, we can set token values in **`Environment Variables`**. Click `env` - `Add Variable` to set the token value, so plain text will not appear in the node.

Check [https://crawlbase.com/dashboard/account/docs](https://crawlbase.com/dashboard/account/docs) for your crawlbase API Key.

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/c9fd5578db8952438a5b31b4ed47e603.webp" alt=""><figcaption></figcaption></figure>

By typing `/` , you can easily insert the API Key as a variable.

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/90e9b7f78989d62daabe0c4f68445099.webp" alt=""><figcaption></figcaption></figure>

Tap the start button of this node to check whether it works correctly:

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/15d737eca4cceaf55fbb4da8e5adba3c.webp" alt=""><figcaption></figcaption></figure>

### LLM node

Now, we can use LLM to analyze the result scraped by crawlbase and execute our command.

The value `context` should be `body` from HTTP Request node.

The following is a sample system prompt.

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/f41daaa1d86651cd33552920730ba8b3.webp" alt=""><figcaption></figcaption></figure>

## Test run

Click `Preview` to start a test run and input twitter user id in `id`

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/8bd435ac17949825813fc2239b39fe4f.webp" alt=""><figcaption></figcaption></figure>

For example, I want to analyze Elon Musk's tweets and write a tweet about global warming in his tone.

<figure><img src="https://assets-docs.dify.ai//img/en/intermediate/34b19b1bb72c99acf84f550ef4e2a9bf.webp" alt=""><figcaption></figcaption></figure>

Does this sound like Elon? lol

Click `Publish` in the upper right corner and add it in your website.

Have fun!

## Lastly…

### Other X(Twitter) Crawlers

In this article, I’ve introduced crawlbase. It should be the cheapest Twitter crawler service available, but sometimes it cannot correctly scrape the content of user tweets.

The Twitter crawler service used by [wordware.ai](http://wordware.ai) mentioned earlier is **Tweet Scraper V2**, but the subscription for the hosted platform **apify** is $49 per month.

## Links

* [X@dify\_ai](https://x.com/dify\_ai)
* Dify’s repo on GitHub:[https://github.com/langgenius/dify](https://github.com/langgenius/dify)
