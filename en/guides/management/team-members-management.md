# Team Members Management

This guide explains how to manage members within a Dify team. The team member limits for different Dify versions are below.

| Sandbox / Free | Professional | Team      | Community | Enterprise |
| -------------- | ------------ | --------- | --------- | ---------- |
| 1              | 3            | Unlimited | Unlimited | Unlimited  |

### Adding Members

{% hint style="info" %}
Only team owners have permission to invite team members.
{% endhint %}

To add a member, the team owner can click on the avatar in the upper right corner, then select **"Members"** → **"Add"**. Enter the email address and assign member permissions to complete the process.

<figure><img src="../../.gitbook/assets/team-members-management-01.png" alt=""><figcaption><p>Assigning permissions to team members</p></figcaption></figure>

Invited members can complete their registration through either a URL link or an email invitation.

> For Community Edition, enabling email functionality requires the team owner to configure and activate the email service via system [environment variables](https://docs.dify.ai/getting-started/install-self-hosted/environments).

### Member Permissions

Team members are divided into owners, administrators, editors, and members.

* **Owner**
  * Role description: The first member of the team, with the highest level of permissions, responsible for the operation and management of the entire team.
  * Permission overview: Has permissions to manage team members, adjust member permissions, set model providers, create and delete applications, create knowledge bases, set tool libraries, etc.
* **Administrator**
  * Role description: Team administrator, responsible for managing team members and model providers.
  * Permission overview: Cannot adjust member permissions; has permissions to add or remove team members, set model providers, create, edit and delete applications, create knowledge bases, set tool libraries, etc.
* **Editor**
  * Role description: Regular team member, responsible for collaboratively creating and editing applications.
  * Permission overview: Cannot manage team members, set model providers, or set tool libraries; has permissions to create, edit and delete applications, create knowledge bases.
* **Member**
  * Role description: Regular team member, only allowed to view and use applications created within the team.
  * Permission overview: Only has permissions to use applications within the team and use tools.

### Removing Members

{% hint style="info" %}
Only team owners have permission to remove team members.
{% endhint %}

To remove a member, click on the avatar in the upper right corner of the Dify team homepage, navigate to **"Settings"** → **"Members"**, select the member to be removed, and click **"Remove from team"**.

<figure><img src="../../.gitbook/assets/team-members-management-02.png" alt=""><figcaption><p>Removing a member</p></figcaption></figure>

### Frequently Asked Questions

#### 1. How can I transfer team ownership?

Team owners have the highest level of permissions. To maintain the stability of the team structure, team ownership cannot be manually transferred once established.

#### 2. How can I delete a team?

For team data security reasons, team owners cannot delete their teams on their own.

#### 3. How can I delete a team member's account?

Neither team owners nor administrators can delete a team member's account. Account deletion requires the account owner to actively request it, and cannot be performed by others. As an alternative to account deletion, removing a member from the team will revoke that user's access to the team.
