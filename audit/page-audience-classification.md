# Page Audience Classification

Total pages audited: 163
- Cloud-only: 2 pages
- Self-Hosted-only: 14 pages
- Both (duplicate-and-tailor): 33 pages
- Both (snippet-shareable): 114 pages
- Ambiguous (needs writer review): 0 pages

## Cloud-only

Pages whose content only applies to Dify Cloud customers.

- `en/use-dify/workspace/subscription-management.mdx` — frontmatter `tag: "CLOUD"`; entire page is subscription plan comparison and billing management, irrelevant to self-hosted
- `en/use-dify/knowledge/knowledge-request-rate-limit.mdx` — frontmatter `tag: "CLOUD"`; rate limits are subscription-tier-specific and only enforced on Cloud

## Self-Hosted-only

Pages whose content only applies to self-hosted (CE/EE) customers.

All 12 files under `en/self-host/` are self-hosted-only by definition:

- `en/self-host/advanced-deployments/local-source-code.mdx` — local source code deployment
- `en/self-host/advanced-deployments/start-the-frontend-docker-container.mdx` — docker container management
- `en/self-host/configuration/environments.mdx` — environment variable reference (excluded from translation pipeline)
- `en/self-host/platform-guides/bt-panel.mdx` — BT Panel deployment guide
- `en/self-host/platform-guides/dify-premium.mdx` — AWS AMI self-hosted offering; references Cloud only to distinguish it as an alternative
- `en/self-host/quick-start/docker-compose.mdx` — Docker Compose deployment
- `en/self-host/quick-start/faqs.mdx` — self-hosted deployment FAQs
- `en/self-host/troubleshooting/common-issues.mdx` — self-hosted troubleshooting
- `en/self-host/troubleshooting/docker-issues.mdx` — Docker-specific troubleshooting
- `en/self-host/troubleshooting/integrations.mdx` — self-hosted integration troubleshooting
- `en/self-host/troubleshooting/storage-and-migration.mdx` — self-hosted storage and migration
- `en/self-host/troubleshooting/weaviate-v4-migration.mdx` — Weaviate v4 migration for self-hosted

Plus 2 pages in other sections that are self-hosted-only:

- `en/use-dify/publish/webapp/web-app-access.mdx` — frontmatter `tag: "ENTERPRISE"`; entire page describes EE access control tiers (All Members, Specific Members, Authenticated External Users, Public), unavailable on Cloud
- `en/develop-plugin/publishing/standards/third-party-signature-verification.mdx` — explicit Warning: "feature is available only in the Dify Community Edition; not currently supported on Dify Cloud Edition"

## Both (duplicate-and-tailor)

Pages that need a Cloud copy and a Self-Hosted copy with audience-specific phrasing.

### Getting Started

- `en/use-dify/getting-started/introduction.mdx` — intro card links to both "Dify Cloud" signup and "Self Host" docker-compose; Cloud version should omit the self-host card and vice versa
- `en/use-dify/getting-started/quick-start.mdx` — tutorial steps explicitly target Dify Cloud (cloud.dify.ai signup, Sandbox plan credits); self-hosted version would need a different "Before You Start" section

### Build

- `en/use-dify/build/additional-features.mdx` — self-hosted env var block (`UPLOAD_FILE_SIZE_LIMIT`) embedded in Cloud-neutral feature description
- `en/use-dify/build/agent.mdx` — same self-hosted file-size env var pattern
- `en/use-dify/build/chatbot.mdx` — same self-hosted file-size env var pattern
- `en/use-dify/build/text-generator.mdx` — same self-hosted file-size env var pattern
- `en/use-dify/build/workflow-collaboration.mdx` — collaboration is disabled by default on self-hosted and requires an env var to enable; Cloud version should omit that block

### Knowledge

- `en/use-dify/knowledge/create-knowledge/chunking-and-cleaning-text.mdx` — one chunking feature marked "Available for self-hosted deployments only"
- `en/use-dify/knowledge/create-knowledge/import-text-data/readme.mdx` — Cloud paid-plan batch-upload limit alongside self-hosted env vars for the same limits; both audiences present but with different phrasing
- `en/use-dify/knowledge/create-knowledge/import-text-data/sync-from-notion.mdx` — has a dedicated section "Integration Configuration Method for Community Edition Notion" (internal vs public integration difference); Cloud version handles this transparently
- `en/use-dify/knowledge/create-knowledge/setting-indexing-methods.mdx` — Q&A indexing mode explicitly "available for self-hosted deployments only"
- `en/use-dify/knowledge/knowledge-pipeline/knowledge-pipeline-orchestration.mdx` — self-hosted env vars for limits + one feature block marked "Available for self-hosted deployments only"
- `en/use-dify/knowledge/knowledge-pipeline/publish-knowledge-pipeline.mdx` — Sandbox plan restriction on publishing knowledge pipelines
- `en/use-dify/knowledge/manage-knowledge/maintain-knowledge-documents.mdx` — Cloud auto-disables idle documents on subscription schedule (Sandbox 7 days, Pro/Team 30 days); Generate Summary is self-hosted-only; Add Chunks is Cloud paid feature; self-hosted env var for image attachment limit

### Monitor

- `en/use-dify/monitor/logs.mdx` — log retention period varies by Cloud subscription (Sandbox 30 days); self-hosted has different retention behavior
- `en/use-dify/monitor/integrations/integrate-aliyun.mdx` — version prerequisite note "Dify Cloud or Community Edition version must be ≥ v1.6.0"; version constraints apply differently per deployment
- `en/use-dify/monitor/integrations/integrate-weave.mdx` — frontmatter description "Dify Cloud | Community version ≥ v1.3.1"; version constraint framing differs per deployment

### Nodes

- `en/use-dify/nodes/code.mdx` — self-hosted installations must manually start the sandbox service for code execution; Cloud handles this transparently
- `en/use-dify/nodes/knowledge-retrieval.mdx` — Cloud rate limits (subscription-plan-specific) plus self-hosted env var for image attachment size
- `en/use-dify/nodes/trigger/overview.mdx` — Sandbox plan 2-trigger limit and Cloud execution quotas; self-hosted has no such quotas
- `en/use-dify/nodes/trigger/plugin-trigger.mdx` — Cloud has pre-configured OAuth clients for popular plugins; self-hosted requires manual OAuth app creation + TRIGGER_URL env var
- `en/use-dify/nodes/trigger/webhook-trigger.mdx` — self-hosted TRIGGER_URL env var for customizing the webhook base prefix

### Publish

- `en/use-dify/publish/publish-to-marketplace.mdx` — confirms app compatibility against "Dify Cloud or the latest Community Edition"; marketplace listing is universal but testing instructions differ
- `en/use-dify/publish/webapp/web-app-settings.mdx` — references Enterprise access control feature and distinguishes "Dify Community" (public by default) from the Enterprise feature

### Workspace

- `en/use-dify/workspace/app-management.mdx` — DSL version compatibility note distinguishes "SaaS users" from "Community users"
- `en/use-dify/workspace/model-providers.mdx` — System Providers (Dify-managed, subscription-billed) are Cloud-only; self-hosted has only custom providers
- `en/use-dify/workspace/personal-account-management.mdx` — login method table explicitly splits by edition (Community: email+password; Cloud: GitHub, Google, email verification code)
- `en/use-dify/workspace/plugins.mdx` — has an "Enterprise Only" callout for one plugin capability
- `en/use-dify/workspace/readme.mdx` — workspace creation section explicitly describes Cloud (auto-created on first login) vs Community Edition (created during installation) differently
- `en/use-dify/workspace/team-members-management.mdx` — team size limits table explicitly splits Free/Professional/Team (Cloud) from Community/Enterprise (self-hosted unlimited)

### Tutorials

- `en/use-dify/tutorials/customer-service-bot.mdx` — image alt text references both "Community Edition and SaaS Version"; content is generic enough but framing is audience-aware
- `en/use-dify/tutorials/twitter-chatflow.mdx` — offers Cloud signup as an alternative to local deployment; self-hosted version would restructure the opening

### Develop Plugin

- `en/develop-plugin/dev-guides-and-walkthroughs/tool-oauth.mdx` — Cloud pre-configures OAuth clients for popular tools; self-hosted requires manual OAuth app creation and domain configuration; substantively different setup paths

## Both (snippet-shareable)

Pages whose content is universally identical and can live as a snippet imported by both products.

### Getting Started

- `en/use-dify/getting-started/key-concepts.mdx` — pure conceptual glossary, no audience markers

### Build

- `en/use-dify/build/goto-anything.mdx` — UI navigation feature, no audience markers
- `en/use-dify/build/mcp.mdx` — MCP protocol feature, no audience markers
- `en/use-dify/build/orchestrate-node.mdx` — workflow canvas concepts, no audience markers
- `en/use-dify/build/predefined-error-handling-logic.mdx` — error handling spec, no audience markers
- `en/use-dify/build/shortcut-key.mdx` — keyboard shortcuts reference, no audience markers
- `en/use-dify/build/version-control.mdx` — version control feature, no audience markers
- `en/use-dify/build/workflow-chatflow.mdx` — workflow vs chatflow comparison, no audience markers

### Debug

- `en/use-dify/debug/error-type.mdx` — error type reference, no audience markers
- `en/use-dify/debug/history-and-logs.mdx` — debug history feature, no audience markers
- `en/use-dify/debug/step-run.mdx` — step-run debugging feature, no audience markers
- `en/use-dify/debug/variable-inspect.mdx` — variable inspector feature, no audience markers

### Knowledge

- `en/use-dify/knowledge/connect-external-knowledge-base.mdx` — external knowledge base connection, no audience markers
- `en/use-dify/knowledge/create-knowledge/introduction.mdx` — knowledge creation overview, no audience markers
- `en/use-dify/knowledge/create-knowledge/import-text-data/sync-from-website.mdx` — website sync, no audience markers
- `en/use-dify/knowledge/external-knowledge-api.mdx` — external knowledge API reference, no audience markers
- `en/use-dify/knowledge/integrate-knowledge-within-application.mdx` — integration guide, no audience markers
- `en/use-dify/knowledge/knowledge-pipeline/authorize-data-source.mdx` — data source authorization, no audience markers
- `en/use-dify/knowledge/knowledge-pipeline/create-knowledge-pipeline.mdx` — pipeline creation, no audience markers
- `en/use-dify/knowledge/knowledge-pipeline/manage-knowledge-base.mdx` — knowledge base management, no audience markers
- `en/use-dify/knowledge/knowledge-pipeline/readme.mdx` — knowledge pipeline overview, no audience markers
- `en/use-dify/knowledge/knowledge-pipeline/upload-files.mdx` — file upload, no audience markers
- `en/use-dify/knowledge/manage-knowledge/introduction.mdx` — knowledge management overview, no audience markers
- `en/use-dify/knowledge/manage-knowledge/maintain-dataset-via-api.mdx` — API-based dataset maintenance, no audience markers
- `en/use-dify/knowledge/metadata.mdx` — metadata feature, no audience markers
- `en/use-dify/knowledge/readme.mdx` — knowledge section overview, no audience markers
- `en/use-dify/knowledge/test-retrieval.mdx` — retrieval testing, no audience markers

### Monitor

- `en/use-dify/monitor/analysis.mdx` — dashboard metrics, no audience markers
- `en/use-dify/monitor/annotation-reply.mdx` — annotation system; "Enterprise Standards" is a use-case heading label, not a product gate
- `en/use-dify/monitor/integrations/integrate-arize.mdx` — Arize integration, no audience markers
- `en/use-dify/monitor/integrations/integrate-langfuse.mdx` — Langfuse integration, no audience markers
- `en/use-dify/monitor/integrations/integrate-langsmith.mdx` — LangSmith integration, no audience markers
- `en/use-dify/monitor/integrations/integrate-opik.mdx` — Opik integration, no audience markers
- `en/use-dify/monitor/integrations/integrate-phoenix.mdx` — Phoenix integration, no audience markers

### Nodes

- `en/use-dify/nodes/agent.mdx` — Agent node spec, no audience markers
- `en/use-dify/nodes/answer.mdx` — Answer node spec, no audience markers
- `en/use-dify/nodes/doc-extractor.mdx` — document extractor node, no audience markers
- `en/use-dify/nodes/http-request.mdx` — HTTP request node, no audience markers
- `en/use-dify/nodes/human-input.mdx` — Human Input node, no audience markers
- `en/use-dify/nodes/ifelse.mdx` — if/else node, no audience markers
- `en/use-dify/nodes/iteration.mdx` — iteration node, no audience markers
- `en/use-dify/nodes/list-operator.mdx` — list operator node, no audience markers
- `en/use-dify/nodes/llm.mdx` — LLM node spec, no audience markers
- `en/use-dify/nodes/loop.mdx` — loop node spec, no audience markers
- `en/use-dify/nodes/output.mdx` — output node, no audience markers
- `en/use-dify/nodes/parameter-extractor.mdx` — parameter extractor node, no audience markers
- `en/use-dify/nodes/question-classifier.mdx` — question classifier node, no audience markers
- `en/use-dify/nodes/template.mdx` — template node; mentions `subscription` only inside a Jinja2 template example snippet, not as a product gate
- `en/use-dify/nodes/tools.mdx` — tools node, no audience markers
- `en/use-dify/nodes/trigger/schedule-trigger.mdx` — schedule trigger spec, no audience markers
- `en/use-dify/nodes/user-input.mdx` — user input node, no audience markers
- `en/use-dify/nodes/variable-aggregator.mdx` — variable aggregator node, no audience markers
- `en/use-dify/nodes/variable-assigner.mdx` — variable assigner node, no audience markers

### Publish

- `en/use-dify/publish/developing-with-apis.mdx` — API publishing guide, no audience markers
- `en/use-dify/publish/publish-mcp.mdx` — MCP publishing, no audience markers
- `en/use-dify/publish/README.mdx` — publish section overview, no audience markers
- `en/use-dify/publish/webapp/chatflow-webapp.mdx` — chatflow web app, no audience markers
- `en/use-dify/publish/webapp/embedding-in-websites.mdx` — website embedding, no audience markers
- `en/use-dify/publish/webapp/workflow-webapp.mdx` — workflow web app, no audience markers

### Workspace

- `en/use-dify/workspace/api-extension/api-extension.mdx` — API extension feature, no audience markers
- `en/use-dify/workspace/api-extension/cloudflare-worker.mdx` — Cloudflare Worker integration, no audience markers
- `en/use-dify/workspace/api-extension/external-data-tool-api-extension.mdx` — external data tool extension, no audience markers
- `en/use-dify/workspace/api-extension/moderation-api-extension.mdx` — moderation extension, no audience markers
- `en/use-dify/workspace/tools.mdx` — tools management, no audience markers

### Tutorials

- `en/use-dify/tutorials/article-reader.mdx` — article reader tutorial, no audience markers
- `en/use-dify/tutorials/build-ai-image-generation-app.mdx` — image generation tutorial, no audience markers
- `en/use-dify/tutorials/simple-chatbot.mdx` — simple chatbot tutorial, no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-01.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-02.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-03.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-04.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-05.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-06.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-07.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-08.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-09.mdx` — no audience markers
- `en/use-dify/tutorials/workflow-101/lesson-10.mdx` — no audience markers

### Develop Plugin (all 37 remaining pages are snippet-shareable)

- `en/develop-plugin/dev-guides-and-walkthroughs/agent-strategy-plugin.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/cheatsheet.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/creating-new-model-provider.mdx` — no audience markers (billing reference is a Jinja2 code example)
- `en/develop-plugin/dev-guides-and-walkthroughs/datasource-plugin.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/develop-a-slack-bot-plugin.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/develop-flomo-plugin.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/develop-md-exporter.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/develop-multimodal-data-processing-tool.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/endpoint.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/trigger-plugin.mdx` — billing mention is a subscription-tier Jinja2 example in plugin code, not a product gate
- `en/develop-plugin/features-and-specs/advanced-development/bundle.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/advanced-development/customizable-model.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/advanced-development/reverse-invocation-app.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/advanced-development/reverse-invocation-model.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/advanced-development/reverse-invocation-node.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/advanced-development/reverse-invocation-tool.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/advanced-development/reverse-invocation.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/plugin-types/general-specifications.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/plugin-types/model-designing-rules.mdx` — billing mention is in a Jinja2 template example
- `en/develop-plugin/features-and-specs/plugin-types/model-schema.mdx` — rate-limit mention is a schema field description, not a product gate
- `en/develop-plugin/features-and-specs/plugin-types/multilingual-readme.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/plugin-types/persistent-storage-kv.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/plugin-types/plugin-info-by-manifest.mdx` — no audience markers
- `en/develop-plugin/features-and-specs/plugin-types/plugin-logging.mdx` — CE version requirement is a minimum version note applicable to all deployments; not a product gate
- `en/develop-plugin/features-and-specs/plugin-types/remote-debug-a-plugin.mdx` — cloud.dify.ai URL is the example endpoint; self-hosted users substitute their own URL; content is universal
- `en/develop-plugin/features-and-specs/plugin-types/tool.mdx` — no audience markers
- `en/develop-plugin/getting-started/cli.mdx` — no audience markers
- `en/develop-plugin/getting-started/getting-started-dify-plugin.mdx` — "Community & Contributions" is a card title for the community forum, not a product gate
- `en/develop-plugin/publishing/faq/faq.mdx` — no audience markers
- `en/develop-plugin/publishing/marketplace-listing/plugin-auto-publish-pr.mdx` — marketplace workflow, no audience markers
- `en/develop-plugin/publishing/marketplace-listing/release-by-file.mdx` — file-based release, no audience markers
- `en/develop-plugin/publishing/marketplace-listing/release-overview.mdx` — all three publishing methods apply regardless of deployment
- `en/develop-plugin/publishing/marketplace-listing/release-to-dify-marketplace.mdx` — marketplace submission, no audience markers
- `en/develop-plugin/publishing/marketplace-listing/release-to-individual-github-repo.mdx` — GitHub publishing, no audience markers
- `en/develop-plugin/publishing/standards/contributor-covenant-code-of-conduct.mdx` — billing mention is a hypothetical scenario in a Jinja2 code example; code of conduct applies universally
- `en/develop-plugin/publishing/standards/privacy-protection-guidelines.mdx` — no audience markers
- `en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin.mdx` — cloud.dify.ai URL is the example debug endpoint; self-hosted users substitute their own instance URL; content is universal

## Ambiguous (needs writer review)

No pages were placed in ambiguous. Every page could be classified with reasonable confidence using the heuristics. Borderline calls are noted inline in the duplicate-and-tailor section where the audience signal is weak.

Judgment calls worth flagging for writer review during migration:

- **integrate-aliyun.mdx and integrate-weave.mdx** — classified duplicate-and-tailor because of version prerequisite framing, but the substantive content is identical; could migrate as snippets with a version note in the wrapper.
- **tutorials/customer-service-bot.mdx** — audience signal is a single image alt text; content is otherwise universal; could be treated as snippet-shareable after removing the alt text reference.
- **tutorials/twitter-chatflow.mdx** — the Cloud signup mention is an aside; the tutorial itself works on both deployments; same borderline logic applies.
- **remote-debug-a-plugin.mdx and tool-plugin.mdx** — classified snippet-shareable because cloud.dify.ai is just the example URL; self-hosted users substitute their own instance URL; the instruction is universal.

## Notes for migration

- The Build section (`build/agent.mdx`, `chatbot.mdx`, `text-generator.mdx`, `additional-features.mdx`) follows an identical pattern: one self-hosted env var block appended to otherwise universal content. These four can share a snippet for the common body and use product-specific wrappers for the env var block, rather than fully duplicating every page.
- The Workspace section is the most Cloud-skewed area outside `self-host/`. The subscription/plan model, system model providers, and login methods are meaningfully different between Cloud and self-hosted; expect the most editorial work here.
- All 37 Develop Plugin pages minus `third-party-signature-verification.mdx` and `tool-oauth.mdx` are snippet-shareable. This section requires very little per-product work.
- Six monitoring integration pages (Langfuse, LangSmith, Arize, Opik, Phoenix, Weave minus the version-note ones) are snippet-shareable. The integration setup process is identical across deployments.
- Trigger nodes (`trigger/overview.mdx`, `trigger/plugin-trigger.mdx`, `trigger/webhook-trigger.mdx`) all carry self-hosted env var or quota differences and need duplicating; `trigger/schedule-trigger.mdx` does not and is snippet-shareable.
