# Version Control

This article explains how to manage versions in Dify’s Chatflow and Workflow.

## Overview

**Version Control Panel** allows you to track changes, publish updates, and restore previous versions of your applications. 

## Key Concepts

- **Current Draft**: Your working version where you make changes.

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/38296a597c0ca31b5fb70be2234f2363.png" width="400" alt="Current draft">
</p>

- **Published Version**: Any version released to production.

- **Latest Version**: The current production version.

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/e4c06a0817c30cf9e8893487c889cb02.png" width="350" alt="Latest version">
</p>

- **Previous Version**: Any older published version.

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/4cd05033b93d84b53496f3d02e88601f.png" width="200" alt="Previous version">
</p>

- **Restore**: Return to any earlier version of your application.

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/607a69b5355886b9ae8d23a08e818e35.jpg" width="200" alt="Restore feature">
</p>

## Features

- **View all versions**: Access and review details of all published versions.

- **Find specific versions**: Use filters to find a specific version.

- **Publish new versions**: Release new application versions with custom names and release notes.

- **Edit published versions**: Edit the title and release notes of a published version.

- **Delete previous versions**: Remove outdated versions to keep the list organized.

- **Restore published versions**: Load a published version into drafts for modifications.

## How to View All Versions

To view all versions:

1. Click the history icon to enter the Version Control Panel.

![View all versions](https://assets-docs.dify.ai/2025/03/eed667bbc9498425342c09039054cf98.png)

2. View versions in chronological order with titles, release notes, publish dates, and publishers.

3. *(Optional)* Click **Load More** to view more historical versions.

![Load more](https://assets-docs.dify.ai/2025/03/df9aeb06128f11089dc2294f0338e2ca.png)

## How to Find a Specific Version

**To find versions you published**:

1. Click the filter icon to open the filter dialog.

2. Choose between:

- **All**: Shows versions published by you and other users
- **Only yours**: Shows only versions you published

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/0bf8fef8858671a8fef160f49dd83dad.jpg" width="200" alt="All or only yours">
</p>

**To find named versions**:

Toggle **Only show named versions** to display only the versions with custom names.

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/2473121caa2e25ad1a76ee42a4127fb4.jpg" width="200" alt="Only show named versions">
</p>

## How to Publish a New Version

To publish a new version:

1. Click **Publish > Publish Update** to release the current version.

![Publish new version](https://assets-docs.dify.ai/2025/03/26f3f324ab4ecb965708d553ddd78d97.png)

2. The newly published version will be marked as `Latest` in the panel.

![Latest version marked](https://assets-docs.dify.ai/2025/03/67e95de17577bc272addad6c33f8ea59.png)

## How to Edit a Published Version

To edit a published version:

1. In the Version Control Panel, find the version you want to edit.

2. Click its action menu icon.

3. Choose either:
- **Name this version** for versions with default names.

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/ac149f63da6611d7080d305dd3fad65c.jpg" width="200" alt="Name this version">
</p>

- **Edit version info** for versions with custom names.

<p align="center">
    <img src="https://assets-docs.dify.ai/2025/03/1d840edf979132a9bbf1e065f95e663c.jpg" width="200" alt="Edit version info">
</p>

4. Confirm **Publish**.

![Edit version info](https://assets-docs.dify.ai/2025/03/838e5a12aa277bada6c2a4a214450fa5.jpg)

## How to Delete a Previous Version

To delete a Previous version:

1. Find the published version you want to delete.

2. Click the action menu icon and select **Delete**.

<p align="center">
  <img src="https://assets-docs.dify.ai/2025/03/25ad1999fc9f6f44fcac04526ac5563a.jpg" width="200" alt="Delete version">
</p>

3. Confirm **Delete**.

![Delete Version Confirmed](https://assets-docs.dify.ai/2025/03/9326fd0463d024aac1907c83a37fe13b.jpg)

{% hint style="warning" %}
-   The **Current Draft** cannot be deleted
-   The **Latest Version** (marked as “Latest”) cannot be deleted
{% endhint %}

## How to Restore a Published Version

To restore a published version:

1. Find the published version you want to restore.

2. Click its action menu icon and select **Restore**.

<p align="center">
  <img src="https://assets-docs.dify.ai/2025/03/c96b714accc29df8e46e711782a7a6a9.jpg" width="200" alt="Restore version">
</p>

3. Confirm **Restore**. The system will load the selected version into your current draft.

![Restore version confirmed](https://assets-docs.dify.ai/2025/03/f3a6e13f2e910f5c7917f52fe77bdfca.jpg)

## Version Control Workflow

Here is how versions work through a typical workflow:

> Note: Matching colors indicate identical version content.

### Phase 1: Initial Draft

-   System creates a **Draft** (Version A).

![Phase 1](https://assets-docs.dify.ai/2025/03/35ece9d5d5d4d8c46a3fb5ceae4d0c15.jpeg)

### Phase 2: First Release

-   Version A is published, becoming the **Latest Version**.
-   System creates a new **Draft** (Version B).

![Phase 2](https://assets-docs.dify.ai/2025/03/3d1f66cdeb08710f01462a6b0f3ed0a8.jpeg)

### Phase 3: Second Release

-   Version B is published, becoming the **Latest Version**.
-   Version A becomes a **Previous Version**.
-   System creates a new **Draft** (Version C).

![Phase 3](https://assets-docs.dify.ai/2025/03/92ffbf88a3cbeeeeab47c1bd8b4f7198.jpeg)

### Phase 4: Restore

-   Version A is restored to **Draft**, replacing Version C.
-   Version B remains the **Latest Version**.

![Phase 4](https://assets-docs.dify.ai/2025/03/541f1891416af90dab5b51bfec833249.jpeg)

### Phase 5: Publish a Restored Version

-   Restored Version A is published, becoming the **Latest Version**.
-   Previous Versions A and B become **Previous Versions**.
-   System creates a new **Draft** (Version D).

![Phase 5](https://assets-docs.dify.ai/2025/03/3572a4f2edef166c3f14e4ec4e68b297.jpeg)

### Complete Workflow Demo

![Workflow](https://assets-docs.dify.ai/2025/03/dc7c15a4dfafb72ce7fffea294d5b5e5.gif)

## FAQ

- **What are the different version types?**

<table style="width: 100%; border-collapse: collapse; background-color: #fff;">
    <thead>
        <tr style="background-color: #f9fafb;">
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 15%;">Type</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 25%;">Description</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Access</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Deletion</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Restoration</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Current Draft</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Current work in progress</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Requires publishing to go live</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Not accessible online</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Not deletable</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Latest Version</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Current live version</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Requires new draft for updates</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Live and accessible</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Can be restored</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Previous Version</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Previous published versions</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Can restore to draft</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Stored in history only</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Can be restored</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Published Version</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Includes both latest and previous versions</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">/</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">/</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">/</td>
        </tr>
    </tbody>
</table>

- **What happens to my current draft when restoring a previous version?**

When restoring a previous version, that version’s content becomes your new draft. Your current draft will be lost, so please review changes carefully before proceeding.

- **Which apps support version control?**

Version control is currently available for **Chatflow** and **Workflow** applications only. It is not yet supported for **Chatbot**, **Text Generator**, or **Agents**.
