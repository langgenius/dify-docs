---
description: Know more about Dify's billing plans to support expanding your usage.
---

# Billing

## Workspace-based Billing

The Dify platform has "workspaces" and "apps". A workspace can contain multiple apps. Each app has capabilities like prompt orchestration, LLM invocation, knowledge RAG, logging & annotation, and standard API delivery. **We recommend one team or organization use one workspace, because our system bills on a per-workspace basis (calculated from total resource consumption within a workspace)**. For example:

```Plaintext

Workspace 1  
App 1(Prompt, RAG, LLM, Knowledge base, Logging & Annotation, API)
App 2(Prompt, RAG, LLM, Knowledge base, Logging & Annotation, API) 
App 3(Prompt, RAG, LLM, Knowledge base, Logging & Annotation, API)
...
Workspace 2
```

## Plan Quotas and Features

We offer a free plan for all users to test your AI app ideas, including 200 OpenAI model message calls. After using up the free allowance, you need to obtain LLM API keys from different model providers, and add them under **Settings --> Model Providers** to enable normal model capabilities.Upgrading your workspace to a paid plan means unlocking paid resources for that workspace. For example: upgrading to Professional allows creating over 10 apps (up to 50) with up to 200MB total vector storage quota combined across projects in that workspace. Different version quotas and features are as follows:

<table><thead><tr><th width="148">Metric</th><th width="237">Sandbox</th><th>Professional </th><th>Team</th></tr></thead><tbody><tr><td>pricing</td><td>Free</td><td>$59/month</td><td>$159/month</td></tr><tr><td><strong>Model Providers</strong></td><td>OpenAI,Anthropic,Azure OpenAI,Llama2,Hugging Face,Replicate</td><td>OpenAI,Anthropic,Azure OpenAI, Llama2,Hugging Face,Replicate</td><td>OpenAI,Anthropic,Azure OpenAI, Llama2,Hugging Face,Replicate</td></tr><tr><td><strong>Team Members</strong></td><td>1</td><td>3</td><td>Unlimited</td></tr><tr><td><strong>Apps</strong></td><td>10</td><td>50</td><td>Unlimited</td></tr><tr><td><strong>Vector Storage</strong></td><td>10MB</td><td>200MB</td><td>1GB</td></tr><tr><td><strong>Document Processing Priority</strong></td><td>Standard</td><td>Priority</td><td>Priority</td></tr><tr><td><strong>Logo Change</strong></td><td>/</td><td>/</td><td>√</td></tr><tr><td><strong>Fine-Tuning</strong></td><td>/</td><td>√(Coming soon)</td><td>√(Coming soon)</td></tr><tr><td><strong>Logs History</strong></td><td>30 days</td><td>Unlimited</td><td>Unlimited</td></tr></tbody></table>

Check out the [pricing page ](https://dify.ai/pricing)to learn more.

## Monitor Resource Usage

You can view capacity usage details on your workspace's Billing page.

<figure><img src="../.gitbook/assets/usage.png" alt=""><figcaption><p>monitor resource usage</p></figcaption></figure>

## FAQ

1.  What happens if my resource usage exceeds the Free plan before I upgrade to a paid plan?

    > During Dify's Beta stage, excess quotas were provided for free to seed users' workspaces. After Dify's billing system goes live, your existing data will not be lost, but your workspace can no longer process additional text vectorization storage. You will need to upgrade to a suitable plan to continue using Dify.
2.  What if neither the Professional nor Team plans meet my usage needs?

    > If you are a large enterprise requiring more advanced plans, please email us at [business@dify.ai](mailto:business@dify.ai).
3.  Under what circumstances do I need to pay when using the CE version?

    > When using the CE version, please follow our open source license terms. If you need commercial use, such as removing Dify's logo or requiring multiple workspaces, using Dify in a SaaS model, you will need to contact us at [business@dify.ai](mailto:business@dify.ai) for commercial licensing.
