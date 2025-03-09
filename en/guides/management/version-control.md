
This article explains how to manage versions in Dify’s Chatflow and Workflow.

## Overview

Version Control Panel allows you to track changes, publish updates, and restore previous versions of your applications. 

## Key Concepts

- **Current Draft:** Your working version where you make changes.

- **Published Version:** Any version released to production.

- **Latest Version:** The current production version.

- **Previous Version:** Any older published version.

- **Restore:** Return to any earlier version of your application.

## Features

- **View all versions:** Access and review details of all published versions.

- **Find specific versions:** Use filters to locate a specific version.

- **Publish new versions:** Release new application versions with custom names and release notes.

- **Edit published versions:** Edit the title and release notes of a published version.

- **Delete historical versions:** Remove outdated versions to keep the list organized.

- **Restore published versions:** Load a historical version into drafts for modifications.

## How to View All Versions

To view all versions:

1. Click the history icon to enter the Version Control Panel.

2. View versions in chronological order with titles, release notes, publish dates, and publishers.

3. *(Optional)* Click **Load More** to view more historical versions.

## How to Find a Specific Version

**- To find versions you published:**

1. Click the filter icon to open the filter dialog

2. Choose between:
- **All:** Shows versions published by you and other users
- **Only yours:** Shows only versions you published

**- To find named versions:**

Toggle **Only show named versions** to display only versions with custom names and hide unnamed versions

## How to Publish a New Version

To publish a new version:

1. Click **Publish > Publish Update**.

2. *(Optional)* In the **Name This Version** dialog:
- Enter a version title
- Enter the release notes
Or skip these fields to use the default name (“Untitled Version”) and blank information

3. Click **Publish** to release the current version. The newly published version will be marked as `Latest` in the panel.

## How to Edit a Published Version

To edit a published version:

1. In the Version Control Panel, find the version you want to edit.

2. Click the menu icon.

3. Choose either:
- **Name this version** for versions with default names.
- **Edit version info** for versions with custom names.

## How to Delete a Historical Version

To delete a historical version:

1. Locate the published version you want to delete.

2. Click the action menu and select **Delete**.

3. Confirm **Delete**.

{% hint style="warning" %}
-   The **Current Draft** cannot be deleted
-   The **Latest Version** (marked as “Latest”) cannot be deleted
{% endhint %}

## How to Restore a Published Version

To restore a published version:

1. Find the historical version you want to restore.

2. Click the menu icon and select **Restore**.

3. Confirm **Restore**. The system will load the selected version into your current draft.

## Version Control Workflow

Here is how versions work through a typical workflow:

> Note: Matching colors indicate identical version content.

### Phase 1: Initial Draft

-   System creates a **Draft** (Version A).

### Phase 2: First Release

-   Version A is published, becoming the **Latest Version**.
-   System creates a new **Draft** (Version B).

### Phase 3: Second Release

-   Version B is published, becoming the **Latest Version**.
-   Version A becomes a **Historical Version**.
-   System creates a new **Draft** (Version C).

### Phase 4: Restore

-   Version A is rolled back to **Draft**, replacing Version C.
-   Version B remains the **Latest Version**.

### Phase 5: Publishing a Restored Version

-   Rolled back Version A is published, becoming the **Latest Version**.
-   Previous Versions A and B become **Historical Version**.
-   System creates a new **Draft** (Version D).

### Complete Workflow Demo

## FAQ

**What are the different version types?**

<table style="width: 100%; border-collapse: collapse; background-color: #fff;">
    <thead>
        <tr style="background-color: #f9fafb;">
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 15%;">Type</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 25%;">Description</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Access</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Deletion</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Rollback</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Draft</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Current work in progress</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Requires publishing to go live</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Not accessible online</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Not deletable</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Latest Release</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Current live version</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Requires new draft for updates</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Live and accessible</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Can be restored</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Historical Release</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Previous published versions</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Can restore to draft</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Stored in history only</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Can be restored</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Published</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Includes both latest and historical releases</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;"></td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;"></td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;"></td>
        </tr>
    </tbody>
</table>

**What happens to my current draft when restoring a historical version?**

When restoring a historical version, that version‘s content becomes your new draft. Your current draft will be lost, so please review changes carefully before proceeding.

**Which apps support version management?**

Version management is currently available for **Chatflow** and **Workflow** applications only. It is not yet supported for **Chatbot**, **Text Generator**, or **Agents**.