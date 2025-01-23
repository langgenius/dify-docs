# Publish to Dify Marketplace

**Dify Marketplace** is dedicated to providing more powerful and flexible functionality extensions for global Dify platform users. Your contributions will further enrich this platform's possibilities.

Whether you're a developer submitting a plugin for the first time or an experienced contributor, we hope to provide clear publishing processes and best practice recommendations through this guide, helping your plugin be successfully published and bring value to the community.

We look forward to building a more open and innovative plugin ecosystem with you!

### **Plugin Review Process**

The plugin publishing process refers to developers submitting Pull Requests (PRs) to the Dify Marketplace repository on Github. After review and approval, the new plugin code will be merged and automatically published to Dify Marketplace.

Here is the general plugin review process:

<figure><img src="https://assets-docs.dify.ai/2024/12/fdaf16a2017d290bd5b045344f78660c.png" alt=""><figcaption></figcaption></figure>

### **Developer Responsibilities**

#### **Before Submitting a Pull Request (PR)**

1. **Ensure Plugin Functionality and Complete Documentation**

* Verify that the plugin functions properly
* Provide comprehensive **README files** including:
  * Setup instructions and usage guides
  * Any code, APIs, credentials, or other information users need to connect the plugin to services
* Ensure collected user information is only used for service connection and plugin improvement

2. **Validate Plugin's Contribution Value**

* Ensure the plugin provides unique value to Dify users
* Plugin should introduce functionality or services not yet available in Dify or other plugins
* Follow community standards:
  * Non-violent content, respecting global user base
  * Compliant with integrated service policies

**How to Check for Similar Plugins?**

* Avoid submitting plugins with functionality that duplicates existing plugins or PRs, unless the new plugin has:
  * New features
  * Performance improvements
* **How to determine if a plugin is unique enough:**
  * If the plugin only makes minor adjustments to existing functionality (like adding language parameters), consider extending the existing plugin
  * If the plugin implements significant functional changes (like optimizing batch processing or improving error handling), it can be submitted as a new plugin
  * Not sure? Include a brief explanation in your PR about why a new plugin is needed
* **How to Check for Similar Plugins?**
  * Avoid submitting functionality that duplicates existing plugins or PRs, unless the new plugin offers:
    * New features
    * Performance improvements
  * **How to determine if a plugin is unique:**
    * If the plugin only makes minor adjustments to existing functionality (like adding language parameters), consider extending the existing plugin
    * If the plugin implements significant functional changes (like optimizing batch processing or improving error handling), it can be submitted as a new plugin
    * Not sure? Include a brief explanation in your PR describing why a new plugin is needed

**Example:**

Taking the Google search plugin as an example, it accepts a single input query and outputs a list of Google search results using the Google Search API.

If you provide a new Google search plugin with similar underlying implementation but minor input adjustments (e.g., adding new language parameters), we recommend extending the existing plugin.

On the other hand, if you've implemented the plugin with optimized batch search and error handling capabilities in a new way, it can be reviewed as a separate plugin.

***

**During Pull Request (PR) Review**

Actively respond to reviewers' questions and feedback:

* PR comments unresolved for **14 days** will be marked as stale (can be reopened)
* PR comments unresolved for **30 days** will be closed (cannot be reopened, need to create new PR)

***

**After Pull Request (PR) Approval**

**1. Ongoing Maintenance**

* Handle user-reported issues and feature requests
* Migrate plugins when major API changes occur:
  * Dify will provide advance notice of changes and migration instructions
  * Dify engineers can provide migration support

**2. Marketplace Public Beta Testing Phase Limitations**

* Avoid introducing breaking changes to existing plugins

***

**Review Process**

**1. Review Order**

* PRs are processed on a **first-come-first-served** basis. Reviews will begin within 1 week. If delayed, reviewers will notify PR authors via comments.

**2. Review Focus**

* Check if plugin names, descriptions, and setup instructions are clear and instructive
* Verify if the plugin's Manifest file meets format specifications and contains valid author contact information

**3. Plugin Functionality and Relevance**

* Test plugins according to provided setup instructions
* Ensure the plugin's purpose is reasonable within the Dify ecosystem

Dify.ai reserves the right to accept or reject plugin submissions.

***

**Frequently Asked Questions**

1. **How to determine if a plugin is unique?**

Example: A Google search plugin that only adds language parameters should probably be submitted as an extension to an existing plugin. However, if the plugin implements significant functional improvements (like optimized batch processing or error handling), it can be submitted as a new plugin.

2. **What if my PR is marked as stale or closed?**

Stale PRs can be reopened after addressing feedback. Closed PRs (over 30 days) require creating a new PR.

3. **Can plugins be updated during the Beta testing phase?**

Yes, but breaking changes should be avoided.

