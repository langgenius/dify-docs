# Integrating AWS Bedrock Models (DeepSeek)

## Overview

[AWS Bedrock Marketplace](https://aws.amazon.com/bedrock/marketplace/) is a comprehensive LLM deployment platform that enables developers to discover, evaluate, and utilize over 100 emerging foundational models (FMs) with ease. 

This document explains how to deploy the DeepSeek model on the Bedrock Marketplace and integrate it with the Dify platform, facilitating the rapid development of AI applications powered by DeepSeek.

## Prerequisites

- An AWS account with access to [Bedrock](https://aws.amazon.com/bedrock/).
- A [Dify.AI account](https://cloud.dify.ai/).

## Deployment Procedure

### 1. Deploy the DeepSeek Model

**1.1** In the **Bedrock Marketplace**, search for **DeepSeek** and select any version of the **DeepSeek R1** model or its distilled variant.

![](https://assets-docs.dify.ai/2025/02/9c6e17fc0cf262b2005013bf122251d1.png)

**1.2** Navigate to the model details page, click **"Deploy"**, and complete the required configuration as prompted to execute a one-click deployment.

> **Note:** Different model versions may require different compute instance configurations, which can affect the associated costs.

![](https://assets-docs.dify.ai/2025/02/613497e3473d9b6eaa7cb5611decee0c.png)

**1.3** After deployment, review the automatically generated **Endpoint** on the **Marketplace Deployments** page. This parameter, which is identical to the SageMaker Endpoint, will be used for subsequent integration with the Dify platform.

![View Endpoint](https://assets-docs.dify.ai/2025/02/82a1d6406662b83386b86ec511ab20be.png)

### 2. Connect the DeepSeek Model with the Dify Platform

**2.1** Log in to the **Dify** management dashboard and navigate to the **Settings** page.

**2.2** In the **Model Provider** section, locate **SageMaker** and click the **"Add Model"** button at the bottom-right corner of the SageMaker card to access the configuration interface.

![Add Model](https://assets-docs.dify.ai/2025/02/864fc8476c47b460b67f14152cbbf360.png)

**2.3** On the SageMaker configuration page, complete the following fields:

- **Model Type**: Select **LLM**.
- **Model Name**: Enter a custom name for the model.
- **sagemaker endpoint**: Input the **Endpoint** parameter obtained from the AWS Bedrock Marketplace. This parameter can be found on the **Endpoint** page.

Refer to the **Marketplace Deployments** page for the auto-generated **Endpoint**:

![](https://assets-docs.dify.ai/2025/02/1feaa8d5054933f42da25a8f655b5a9e.png)

### 3. Execute the Model

**For Chatflow / Workflow Applications:**

After completing the configuration, test the DeepSeek model within the Dify platform. Click on **"Create Blank App"** on the left-hand side of the Dify homepage, select either a **Chatflow** or **Workflow** application, and add an LLM node.

Refer to the screenshot below to verify that the model is generating responses correctly in the application preview.

![Model Running](https://assets-docs.dify.ai/2025/02/e7fb06888101662ecb970401fdba63b5.png)

In addition to testing with the Chatflow / Workflow app, you can also create Chatbot app for testing.

## FAQ

### 1. **Endpoint Parameter Not Visible After Deployment**

Ensure that the compute instance is configured correctly and that AWS permissions are properly set. If the issue persists, consider redeploying the model or contacting AWS customer support.

### 2. **How to Validate the Model in Dify**

After configuring the model within Dify, invoke it via the provided interface to verify that the input data is processed correctly and that the output matches expectations.