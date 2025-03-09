## What is Metadata?

### Overview

Metadata is information that describes your data - essentially “data about data”. Just as a book has a table of contents to help you understand its structure, metadata provides context about your data’s content, origin, purpose, etc., making it easier for you to find and manage information in your knowledge base.

### Core Concepts

-  **Metadata Field:** The container for specific information about a document. Think of it as a labeled box where you store particular details about your content.

-  **Field Name:** The label of a metadata field (e.g., “source”, “language”).

-  **Value:** The information stored in a metadata field (e.g., “official document”, “Japanese”).

-  **Value Count:** The number of unique values contained in a metadata field.

-  **Value Type:** The type of value a field can contain.
    - Dify supports three value types:
        - String: For text-based information
        - Number: For numerical data
        - Time: For dates/timestamps

## How to Manage My Metadata?

### Manage Metadata Fields in the Knowledge Base

You can create, modify, and delete metadata fields in the knowledge base.

> Any changes you make to metadata fields here affect your knowledge base globally.

#### Get Started with the Metadata Panel

##### Access the Metadata Panel

To access the Metadata Panel, go to **Knowledge Base** page and click **Metadata**.

##### Work with the Metadata Panel

-   **View Metadata:** Browse built-in and custom metadata. **Built-in Metadata** is system-generated; **Custom Metadata** is user-defined.

-   **Add Metadata Fields:** Create new metadata fields by clicking **+Add Metadata**.

-   **Edit Metadata Fields:** Modify field names by clicking the edit icon next to each field.

-   **Delete Metadata Fields:** delete unwanted fields by clicking the the delete icon next to each field.

##### Benefits

**Metadata panel** centralizes field management, making it easy to organize and find documents through customizable labels.

##### Built-in vs Custom Metadata

<table border="1" cellspacing="0" cellpadding="10" style="width: 100%; border-collapse: collapse;">
    <tr>
        <th style="width: 15%; text-align: center; background-color: #f5f5f5;">Feature</th>
        <th style="width: 42.5%; text-align: center; background-color: #f5f5f5;">Built-in Metadata</th>
        <th style="width: 42.5%; text-align: center; background-color: #f5f5f5;">Custom Metadata</th>
    </tr>
    <tr>
        <td style="text-align: center;">Location</td>
        <td>Lower section of the Metadata panel</td>
        <td>Upper section of the Metadata panel</td>
    </tr>
    <tr>
        <td style="text-align: center;">Example</td>
        <td><img src="[built-in-metadata-image-url]" style="max-width: 100%;"></td>
        <td><img src="[custom-metadata-image-url]" style="max-width: 100%;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">Activation</td>
        <td>Disabled by default; requires manual activation</td>
        <td>Add as needed</td>
    </tr>
    <tr>
        <td style="text-align: center;">Generation</td>
        <td>System automatically extracts and generates field values</td>
        <td>User-defined and manually added</td>
    </tr>
    <tr>
        <td style="text-align: center;">Editing</td>
        <td>Fields and values cannot be modified once generated</td>
        <td>Fields and values can be edited or deleted</td>
    </tr>
    <tr>
        <td style="text-align: center;">Scope</td>
        <td>Applies to all existing and new documents when enabled</td>
        <td>Stored in metadata list; requires manual assignment to documents</td>
    </tr>
    <tr>
        <td style="text-align: center;">Fields</td>
        <td>
            System-defined fields include:<br>
            • Original filename (string)<br>
            • Uploader (string)<br>
            • Upload date (time)<br>
            • Last update date (time)<br>
            • Source (string)
        </td>
        <td>No default fields; all fields must be manually created</td>
    </tr>
    <tr>
        <td style="text-align: center;">Value Types</td>
        <td colspan="2">
            Three supported value types:<br>
            • String: For text values<br>
            • Number: For numerical values<br>
            • Time: For dates and timestamps
        </td>
    </tr>
    <tr>
        <td style="text-align: center;">Use Cases</td>
        <td>Stores basic document information (filename, uploader, dates)</td>
        <td>Supports business-specific needs (security levels, tags, categories)</td>
    </tr>
</table>

#### Create New Metadata Fields

To create a new metadata field:

1. Click **+Add Metadata** to open the **New Metadata** dialog.

2. Choose the value type:
    - String (for text)
    - Number (for numerical values)
    - Time (for dates/timestamps)

3. Name the field.
> Naming rules: Use lowercase letters, numbers, and underscores only.

4. Click **Save** to apply changes.
> Note: New fields are automatically available across all documents in your knowledge base.

#### Edit Metadata Fields

To edit a metadata field:

1. Click the edit icon next to a field to open the **Rename** dialog.

2. Enter the new name in the **Name** field.
> Note: You can only modify the field name, not the value type.

3. Click **Save** to apply changes.

#### Delete Metadata Fields

To delete a metadata field, click the delete icon next to a field to delete it.
> Note: Deleting a field deletes it and all its values from all documents in your knowledge base.

### Edit Metadata 

#### Bulk Edit Metadata in the Metadata Editor

You can edit metadata in bulk in the knowledge base.

##### Get Started with the Metadata Editor

###### Access the Metadata Editor

To access the Metadata Editor:

1. In the knowledge base, select documents using the checkboxes on the left.

2. Click **Metadata** in the bottom action bar.

###### Work with the Metadata Editor

- **View Metadata:** The editor shows existing metadata in the upper section and new metadata in the lower section.

{% hint style="info" %}
Field status is indicated by:
No marker: Unchanged.
Blue dot: Modified.
Reset option: Appears on hover over the blue dot.
{% endhint %}

- **Edit Values:** Modify values in the field box.

{% hint style="info" %}
Single values show directly in the field box.
Multiple values show as a “Multiple Values” card. If you delete all values, the box will show “Empty”.
{% endhint %}

- **Add Fields:** Click **+Add Metadata** to **create new fields**, **add existing fields ** and **manage all fields**.

- **Delete Fields:** Click the delete icon to delete a field from selected documents.

- **Apply Changes:** Choose whether to apply changes to all selected documents.

##### Bulk Add Metadata

To add metadata in bulk:

1. Click **+Add Metadata** in the editor to:
    - Create new fields via **+New Metadata**.
    > New fields are automatically added to the knowledge base.
    - Add existing fields from the dropdown or from the search box.
    - Access the Metadata Panel via **Manage**.

2. (Optional) Enter values for new fields.
> The date picker is for time-type fields

3. Click **Save** to apply changes.

##### Bulk Update Metadata

To update metadata in bulk:

1. In the editor:
    - **Add Values:** Type directly in the field boxes.
    - **Reset Values:** Click the blue dot that appears on hover.
    - **Delete Values:** Clear the field or delete the **Multiple Value** card.
    - **Delete fields:** Click the delete icon (fields appear struck through and grayed out).
    > Note: This only deletes the field from this document, not from your knowledge base.

2. Click **Save** to apply changes.

##### Set Update Scope

Use **Apply to All Documents** to control changes:

- Unchecked (Default): Updates only documents that already have the field.

- Checked: Adds or updates fields across all selected documents.

#### Edit Metadata on the Document Detail Page

You can edit a single document’s metadata on its detail page.

##### Access Metadata Edit Mode

To edit a single document’s metadata:

1. Open the document to view the right sidebar:
    - Metadata overview (top)
    - Custom fields (middle, editable)
    - System fields (bottom, read-only)

2. Click **Start labeling** to begin.

##### Add Metadata

To add a single document’s metadata fields and values:

1. Click **+Add Metadata** to:
    - Create new fields via **+New Metadata**.
    > New fields are automatically added to the knowledge base.
    - Add existing fields from the dropdown or from the search box.
    - Access the Metadata Panel via **Manage**.

2. (Optional) Enter values for new fields.

3. Click **Save** to apply changes.

##### Edit Metadata

To update a single document’s metadata fields and values:

1. Click **Edit** in the top right to begin.

2. Edit metadata:
    - **Update Values:** Type directly in value fields or delete it.
    > Note: You can only modify the value, not the value name.
    - **Delete Fields:** Click the delete icon.
    > Note: This only deletes the field from this document, not from your knowledge base.

3. Click **Save** to apply changes.

## How to Filter Documents with Metadata?

For filtering documents with metadata, see “Metadata Filtering” in [Integrate Knowledge Base within Application](https://docs.dify.ai/guides/knowledge-base/integrate-knowledge-within-application).

## API Documentation

See [Maintaining Dataset via API](https://docs.dify.ai/guides/knowledge-base/knowledge-and-documents-maintenance/maintain-dataset-via-api).

## FAQ

- **What can I do with metadata?**

    - Find information faster with smart filtering.

    - Control access to sensitive content.

    - Organize data more effectively.

    - Automate workflows based on metadata rules.

- **Fields vs Values: What is the difference?**

<table style="width: 100%; border-collapse: collapse; background-color: #f8f9ff;">
    <thead>
        <tr>
            <th style="width: 25%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">Concept</th>
            <th style="width: 25%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">Definition</th>
            <th style="width: 25%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">Characteristics</th>
            <th style="width: 50%; padding: 12px; border: 1px solid #e5e7eb; background-color: #f9fafb;">Examples</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Metadata Fields in the Metadata Panel</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">System-defined attributes that describe document properties</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Global fields accessible across all documents in the knowledge base</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Author, Type, Date, etc.</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Metadata Value on a document’s detail page</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Custom metadata tagged according to individual document requirements</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">Unique metadata values assigned based on document content and context</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: top;">The “Author” field in Document A is set to “Mary” value, while in Document B it is set to “John” value.</td>
        </tr>
    </tbody>
</table>

- **How do different delete options work?**

<table style="width: 100%; border-collapse: collapse; background-color: #fff;">
    <thead>
        <tr style="background-color: #f9fafb;">
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 15%;">Action</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 25%;">Steps</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Image</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Impact</th>
            <th style="padding: 12px; border: 1px solid #e5e7eb; width: 20%;">Outcome</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Delete field in the Metadata Panel</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">In the Metadata Panel, click delete icon next to field</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">
                <img src="[Image1URL]" alt="Knowledge Base Delete" style="max-width: 100%; height: auto;">
            </td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Global - affects all documents</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Field and all values permanently deleted from the knowledge base</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Delete field in the Metadata Editor</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">In the Metadata Editor, click delete icon next to field</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">
                <img src="[Image2URL]" alt="Bulk Delete" style="max-width: 100%; height: auto;">
            </td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Selected documents only</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Field deleted from selected documents; remains in the knowledge base</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Delete field on the document detail page</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">In the Edit Mode, click delete icon next to field</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">
                <img src="[Image3URL]" alt="Single Delete" style="max-width: 100%; height: auto;">
            </td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Current document only</td>
            <td style="padding: 12px; border: 1px solid #e5e7eb; vertical-align: middle;">Field deleted from current document; remains in the knowledge base</td>
        </tr>
    </tbody>
</table>

- **Can I see values in the Metadata Panel?**

The management panel only shows value counts (e.g., "24 values"). Please check the document detail page to see specific values.

- **Can I delete a specific value in the Metadata Editor?**

No - bulk edit only deletes all values at once. Please go to the document detail page to delete specific values.