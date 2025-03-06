# Integrate Open Source Models from Hugging Face

Dify supports Text-Generation and Embeddings. Below are the corresponding Hugging Face model types:

* Text-Generation：[text-generation](https://huggingface.co/models?pipeline\_tag=text-generation\&sort=trending)，[text2text-generation](https://huggingface.co/models?pipeline\_tag=text2text-generation\&sort=trending)
* Embeddings：[feature-extraction](https://huggingface.co/models?pipeline\_tag=feature-extraction\&sort=trending)

The specific steps are as follows:

1. You need a Hugging Face account ([registered address](https://huggingface.co/join)).
2. Set the API key of Hugging Face ([obtain address](https://huggingface.co/settings/tokens)).
3. Select a model to enter the [Hugging Face model list page](https://huggingface.co/models?pipeline\_tag=text-generation\&sort=trending).

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/dafa87c38d57e81d4b9e71e221b8a42d.webp" alt=""><figcaption></figcaption></figure>

Dify supports accessing models on Hugging Face in two ways:

1. Hosted Inference API. This method uses the model officially deployed by Hugging Face. No fee is required. But the downside is that only a small number of models support this approach.
2. Inference Endpoint. This method uses resources such as AWS accessed by the Hugging Face to deploy the model and requires payment.

### Models that access the Hosted Inference API

#### 1 Select a model

Hosted inference API is supported only when there is an area containing Hosted inference API on the right side of the model details page. As shown in the figure below:

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/2dab3b4e18ba2142888bb3164d891787.webp" alt=""><figcaption></figcaption></figure>

On the model details page, you can get the name of the model.

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/79678881bbf8773154bc72288e9921dd.webp" alt=""><figcaption></figcaption></figure>

#### 2 Using access models in Dify

Select Hosted Inference API for Endpoint Type in `Settings > Model Provider > Hugging Face > Model Type`. As shown below:

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/90075a56ed15d952a3ac04d8cd678882.webp" alt=""><figcaption></figcaption></figure>

API Token is the API Key set at the beginning of the article. The model name is the model name obtained in the previous step.

### Method 2: Inference Endpoint

#### 1 Select the model to deploy

Inference Endpoint is only supported for models with the Inference Endpoints option under the Deploy button on the right side of the model details page. As shown below:

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/ddd118e18fc0b57323b757d6605bcf65.webp" alt=""><figcaption></figcaption></figure>

#### 2 Deployment model

Click the Deploy button for the model and select the Inference Endpoint option. If you have not bound a bank card before, you will need to bind the card. Just follow the process. After binding the card, the following interface will appear: modify the configuration according to the requirements, and click Create Endpoint in the lower left corner to create an Inference Endpoint.

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/9dd475f2a873a4f14bcd6b5b178314da.webp" alt=""><figcaption></figcaption></figure>

After the model is deployed, you can see the Endpoint URL.

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/98dccb0e2519e1f0c6183c03dc5306b3.webp" alt=""><figcaption></figcaption></figure>

#### 3 Using access models in Dify

Select Inference Endpoints for Endpoint Type in `Settings > Model Provider > Hugging face > Model Type`. As shown below:

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/afe36ac5b91357687cae775c7d79bfe7.webp" alt=""><figcaption></figcaption></figure>

The API Token is the API Key set at the beginning of the article. `The name of the Text-Generation model can be arbitrary, but the name of the Embeddings model needs to be consistent with Hugging Face.` The Endpoint URL is the Endpoint URL obtained after the successful deployment of the model in the previous step.

<figure><img src="https://assets-docs.dify.ai/img/en/models-integration/d50aa4a34851bd159140034d42a6c5b8.webp" alt=""><figcaption></figcaption></figure>

> Note: The "User name / Organization Name" for Embeddings needs to be filled in according to your deployment method on Hugging Face's [Inference Endpoints](https://huggingface.co/docs/inference-endpoints/guides/access), with either the ''[User name](https://huggingface.co/settings/account)'' or the "[Organization Name](https://ui.endpoints.huggingface.co/)".
