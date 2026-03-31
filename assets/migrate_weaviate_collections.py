"""
Migration script to fix Weaviate schema incompatibility between 1.19.0 and 1.27.0+
This script:
- Identifies collections with old schema (no vectorConfig)
- Creates new collections with proper vectorConfig including "default" named vector
- Migrates data using Weaviate iterator (recommended for reading all objects)
- Uses fixed-size batch operations for reliable inserts
- Preserves all object properties and vectors
Note:
- This is a community-edited version of the draft of the script presented by the Dify Team.
- This script is not officially supported by the Dify Team.
- The original source for this script can be found at https://github.com/langgenius/dify/issues/27291#issuecomment-3501003678.
- The changes made in this script are:
  - Retrieve Weaviate connection info from environment variables to make this script run in the Worker container.
  - Switch to cursor-based pagination in "replace_old_collection", since the migration could fail with large collections.
  - Fix an issue where both the old and new collections remained without being deleted after migrating an empty collection.
"""

import os
import requests
import weaviate
from weaviate.classes.config import Configure, VectorDistances
import sys
import time
from typing import List, Dict, Any

# =============================================================================
# Connection Configuration
# =============================================================================
# This script reads Weaviate connection info from environment variables,
# making it suitable for running inside the Dify Worker container where
# these variables are already set.
#
# If running outside the container (e.g. locally with kubectl port-forward),
# set the environment variables before running:
#
#   export WEAVIATE_ENDPOINT="http://localhost:18080"
#   export WEAVIATE_GRPC_ENDPOINT="grpc://localhost:50051"
#   export WEAVIATE_API_KEY="your-api-key"
#   python migrate_weaviate_collections.py
#
# Or override the defaults directly below:
#
# WEAVIATE_ENDPOINT format:   http://<host>:<port>   (REST API endpoint)
# WEAVIATE_GRPC_ENDPOINT format: grpc://<host>:<port>  (gRPC endpoint)
# WEAVIATE_API_KEY: The API key configured in your Weaviate instance
# =============================================================================
WEAVIATE_ENDPOINT = os.getenv("WEAVIATE_ENDPOINT", "http://weaviate:8080")
WEAVIATE_GRPC_ENDPOINT = os.getenv("WEAVIATE_GRPC_ENDPOINT", "grpc://weaviate:50051")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "WVF5YThaHlkYwhGUSmCRgsX3tD5ngdN8pkih")
BATCH_SIZE = 1000

# Derived values — parsed from the endpoints above.
# These are used by the Weaviate Python client (connect_to_local) and REST calls.
WEAVIATE_HOST = WEAVIATE_ENDPOINT.split("//")[-1].split(":")[0]
WEAVIATE_PORT = int(WEAVIATE_ENDPOINT.split(":")[-1])
WEAVIATE_GRPC_PORT = int(WEAVIATE_GRPC_ENDPOINT.split(":")[-1])


def check_properties_need_migration(schema: Dict[str, Any]) -> bool:
    """
    Check if collection properties need migration:
    - document_id or doc_id has uuid type (should be text)
    - chunk_index has moduleConfig (should not have it)
    """
    properties = schema.get("properties", [])
    for prop in properties:
        prop_name = prop.get("name", "")

        # Check if document_id or doc_id is uuid type
        if prop_name in ["document_id", "doc_id"]:
            if prop.get("dataType") == ["uuid"]:
                return True

        # Check if chunk_index has moduleConfig
        if prop_name == "chunk_index":
            if "moduleConfig" in prop:
                return True

    return False


def identify_old_collections(client: weaviate.WeaviateClient) -> List[str]:
    """Identify collections that need migration (those without vectorConfig OR with wrong property types)"""
    collections_to_migrate = []

    all_collections = client.collections.list_all()
    print(f"Found {len(all_collections)} total collections")

    for collection_name in all_collections.keys():
        # Only check Vector_index collections (Dify knowledge bases)
        if not collection_name.startswith("Vector_index_"):
            continue

        collection = client.collections.get(collection_name)
        config = collection.config.get()

        # Check if this collection has the old schema (no vectorConfig)
        if config.vector_config is None:
            collections_to_migrate.append(collection_name)
            print(f"  - {collection_name}: OLD SCHEMA - no vectorConfig (needs migration)")
            continue

        # Also check if properties need migration (uuid -> text conversion)
        try:
            response = requests.get(
                f"{WEAVIATE_ENDPOINT}/v1/schema/{collection_name}",
                headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
            )

            if response.status_code == 200:
                schema = response.json()
                if check_properties_need_migration(schema):
                    collections_to_migrate.append(collection_name)
                    print(f"  - {collection_name}: PROPERTY TYPE MISMATCH (needs migration)")
                    continue
        except Exception as e:
            print(f"  - {collection_name}: Error checking schema: {e}")

        print(f"  - {collection_name}: OK (skip)")

    return collections_to_migrate


def get_collection_schema(
    client: weaviate.WeaviateClient, collection_name: str
) -> Dict[str, Any]:
    """Get the full schema of a collection via REST API"""
    response = requests.get(
        f"http://{WEAVIATE_HOST}:{WEAVIATE_PORT}/v1/schema/{collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get schema: {response.text}")


def transform_properties(properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transform properties to match the new schema format:
    - document_id: uuid -> text, indexFilterable=true, indexSearchable=true, tokenization="word"
    - doc_id: uuid -> text, indexFilterable=true, indexSearchable=true, tokenization="word"
    - chunk_index: remove moduleConfig, ensure indexFilterable=true, indexSearchable=false
    """
    transformed = []

    for prop in properties:
        new_prop = prop.copy()
        prop_name = prop.get("name", "")

        # Convert document_id and doc_id from uuid to text
        if prop_name in ["document_id", "doc_id"]:
            if prop.get("dataType") == ["uuid"]:
                print(f"    Converting {prop_name}: uuid -> text (with text search enabled)")
                new_prop["dataType"] = ["text"]
                new_prop["indexFilterable"] = True
                new_prop["indexRangeFilters"] = False
                new_prop["indexSearchable"] = True
                new_prop["tokenization"] = "word"

                # Remove auto-schema description
                if "description" in new_prop:
                    del new_prop["description"]

        # Fix chunk_index: remove moduleConfig, ensure proper index settings
        if prop_name == "chunk_index":
            if "moduleConfig" in new_prop:
                print(f"    Removing moduleConfig from {prop_name}")
                del new_prop["moduleConfig"]

            # Ensure correct index settings
            new_prop["indexFilterable"] = True
            new_prop["indexRangeFilters"] = False
            new_prop["indexSearchable"] = False

        # Remove moduleConfig from any other properties if present
        elif "moduleConfig" in new_prop:
            print(f"    Removing moduleConfig from {prop_name}")
            del new_prop["moduleConfig"]

        transformed.append(new_prop)

    return transformed


def create_new_collection(
    client: weaviate.WeaviateClient, old_name: str, schema: Dict[str, Any]
) -> str:
    """Create a new collection with updated schema using REST API"""
    # Generate new collection name
    new_name = f"{old_name}_migrated"

    print(f"Creating new collection: {new_name}")

    # Build new schema with proper vectorConfig
    # Note: When using vectorConfig (named vectors), we don't set class-level vectorizer
    new_schema = {
        "class": new_name,
        # This is the key: define vectorConfig with "default" named vector
        # Do NOT set class-level vectorizer when using vectorConfig
        "vectorConfig": {
            "default": {
                "vectorizer": {"none": {}},
                "vectorIndexType": "hnsw",
                "vectorIndexConfig": {
                    "distance": "cosine",
                    "ef": -1,
                    "efConstruction": 128,
                    "maxConnections": 32,
                },
            }
        },
        "properties": [],
    }

    # Copy and transform properties from old schema
    if "properties" in schema:
        print("  Transforming properties...")
        new_schema["properties"] = transform_properties(schema["properties"])

    # Create collection via REST API
    response = requests.post(
        f"{WEAVIATE_ENDPOINT}/v1/schema",
        json=new_schema,
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create collection: {response.text}")

    print(f"  Created new collection: {new_name}")
    return new_name


def transform_property_values(properties: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform property values during migration:
    - Convert UUID objects to strings for document_id and doc_id
    """
    from uuid import UUID

    transformed = {}

    for key, value in properties.items():
        # Convert UUID to string for document_id and doc_id
        if key in ["document_id", "doc_id"] and value is not None:
            if isinstance(value, UUID):
                transformed[key] = str(value)
            else:
                transformed[key] = str(value) if value else value
        else:
            transformed[key] = value

    return transformed


def migrate_collection_data(
    client: weaviate.WeaviateClient, old_collection_name: str, new_collection_name: str
) -> int:
    """Migrate data from old collection to new collection using iterator + fixed-size batch"""
    old_collection = client.collections.get(old_collection_name)
    new_collection = client.collections.get(new_collection_name)

    total_migrated = 0

    print(f"Migrating data from {old_collection_name} to {new_collection_name}")

    # Use fixed-size batch to avoid overwhelming the server during migration
    with new_collection.batch.fixed_size(batch_size=BATCH_SIZE) as batch:
        # Use iterator (recommended by Weaviate) instead of manual cursor pagination
        for obj in old_collection.iterator(include_vector=True):
            # Prepare and transform properties (uuid -> text conversion)
            properties = transform_property_values(obj.properties)

            # Add object with vector
            batch.add_object(
                properties=properties,
                vector=(
                    obj.vector["default"]
                    if isinstance(obj.vector, dict)
                    else obj.vector
                ),
                uuid=obj.uuid,
            )

            total_migrated += 1
            if total_migrated % BATCH_SIZE == 0:
                print(f"  Migrated {total_migrated} objects...")

    print(f"  Total migrated: {total_migrated} objects")
    return total_migrated


def verify_migration(
    client: weaviate.WeaviateClient, old_collection_name: str, new_collection_name: str
):
    """Verify that the migration was successful"""

    old_collection = client.collections.get(old_collection_name)
    new_collection = client.collections.get(new_collection_name)

    # Count objects in both collections
    old_count_response = old_collection.query.fetch_objects(limit=1)
    new_count_response = new_collection.query.fetch_objects(limit=1)

    # Get aggregation for accurate counts
    old_agg = old_collection.aggregate.over_all(total_count=True)
    new_agg = new_collection.aggregate.over_all(total_count=True)

    old_count = old_agg.total_count
    new_count = new_agg.total_count

    print(f"\nVerification:")
    print(f"  Old collection ({old_collection_name}): {old_count} objects")
    print(f"  New collection ({new_collection_name}): {new_count} objects")

    if old_count == new_count:
        print(f"  Status: SUCCESS - Counts match!")
        return True
    else:
        print(f"  Status: WARNING - Counts don't match!")
        return False


def replace_old_collection(
    client: weaviate.WeaviateClient, old_collection_name: str, new_collection_name: str
):
    """
    Replace old collection with migrated one by recreating with original name.

    Safety: The old collection is only deleted AFTER the new one is fully created,
    populated, and verified. If any step fails, both collections are preserved so
    no data is lost. The user can re-run the script or recover manually.
    """
    print(f"\nReplacing old collection with migrated data...")

    # Step 1: Get schema from migrated collection
    print(f"  Step 1: Getting schema from migrated collection...")
    schema_response = requests.get(
        f"{WEAVIATE_ENDPOINT}/v1/schema/{new_collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    if schema_response.status_code != 200:
        raise Exception(
            f"Failed to get migrated collection schema: {schema_response.text}"
        )
    schema = schema_response.json()

    # Step 2: Delete old collection to free the name
    # This is required because Weaviate does not support rename.
    # The migrated collection still holds a full copy of the data.
    print(f"  Step 2: Deleting old collection (migrated copy is safe)...")
    response = requests.delete(
        f"{WEAVIATE_ENDPOINT}/v1/schema/{old_collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    if response.status_code != 200:
        print(f"    Warning: Could not delete old collection: {response.text}")
    else:
        print(f"    Deleted")

    # Step 3: Create collection with original name and new schema
    print(f"  Step 3: Creating collection with original name...")
    schema["class"] = old_collection_name
    create_response = requests.post(
        f"{WEAVIATE_ENDPOINT}/v1/schema",
        json=schema,
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    if create_response.status_code not in [200, 201]:
        print(f"    FAILED to create collection: {create_response.text}")
        print(f"    DATA IS SAFE in: {new_collection_name}")
        print(f"    You can retry or recover manually.")
        raise Exception(f"Failed to create collection: {create_response.text}")
    print(f"    Created")

    # Step 4: Copy data from migrated collection to the newly created one
    print(f"  Step 4: Copying data to original collection name...")
    migrated_collection = client.collections.get(new_collection_name)
    new_collection = client.collections.get(old_collection_name)

    total_copied = 0

    try:
        # Use fixed-size batch to avoid overwhelming the server during migration
        with new_collection.batch.fixed_size(batch_size=BATCH_SIZE) as batch:
            # Use iterator (recommended by Weaviate) instead of manual cursor pagination
            for obj in migrated_collection.iterator(include_vector=True):
                batch.add_object(
                    properties=obj.properties, vector=obj.vector, uuid=obj.uuid
                )

                total_copied += 1
                if total_copied % BATCH_SIZE == 0:
                    print(f"    Copied {total_copied} objects...")
    except Exception as e:
        print(f"    COPY INTERRUPTED after {total_copied} objects: {e}")
        print(f"    DATA IS SAFE in: {new_collection_name}")
        print(f"    You can re-run this script to retry.")
        raise

    print(f"    Total copied: {total_copied} objects")

    # Step 5: Verify copy before cleaning up
    print(f"  Step 5: Verifying copy...")
    migrated_agg = migrated_collection.aggregate.over_all(total_count=True)
    new_agg = new_collection.aggregate.over_all(total_count=True)

    if migrated_agg.total_count != new_agg.total_count:
        print(
            f"    WARNING: Count mismatch! "
            f"Migrated: {migrated_agg.total_count}, New: {new_agg.total_count}"
        )
        print(f"    Keeping {new_collection_name} as backup for safety.")
        print(
            f"\n  PARTIAL SUCCESS: {old_collection_name} created with {new_agg.total_count} objects, "
            f"but {new_collection_name} retained due to count mismatch."
        )
        return False

    print(f"    Verified: {new_agg.total_count} objects match.")

    # Step 6: Only now delete the migrated collection — everything is confirmed safe
    print(f"  Step 6: Cleaning up temporary migrated collection...")
    response = requests.delete(
        f"{WEAVIATE_ENDPOINT}/v1/schema/{new_collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    if response.status_code == 200:
        print(f"    Cleaned up")
    else:
        print(
            f"    Warning: Could not delete {new_collection_name}: {response.text}"
        )
        print(f"    You can delete it manually later.")

    print(
        f"\n  SUCCESS! {old_collection_name} now has the new schema with {total_copied} objects"
    )
    return True


def migrate_all_collections():
    """Main migration function"""

    print("=" * 80)
    print("Weaviate Collection Migration Script")
    print("Migrating from Weaviate 1.19.0 schema to 1.27.0+ schema")
    print("=" * 80)
    print()

    client = weaviate.connect_to_local(
        host=WEAVIATE_HOST,
        port=WEAVIATE_PORT,
        grpc_port=WEAVIATE_GRPC_PORT,
        auth_credentials=weaviate.auth.AuthApiKey(WEAVIATE_API_KEY),
    )

    try:
        # Step 1: Identify collections that need migration
        print("Step 1: Identifying collections that need migration...")
        collections_to_migrate = identify_old_collections(client)

        if not collections_to_migrate:
            print("\nNo collections need migration. All collections are up to date!")
            return

        print(f"\nFound {len(collections_to_migrate)} collections to migrate:")
        for col in collections_to_migrate:
            print(f"  - {col}")

        # Confirm before proceeding
        print("\nThis script will:")
        print("1. Create new collections with updated schema")
        print("2. Copy all data using efficient batch operations")
        print("3. Verify the migration")
        print("4. Optionally rename collections to activate the new ones")
        print()

        # Step 2: Migrate each collection
        for collection_name in collections_to_migrate:
            print("\n" + "=" * 80)
            print(f"Migrating: {collection_name}")
            print("=" * 80)

            try:
                # Get old schema
                schema = get_collection_schema(client, collection_name)

                # Create new collection
                new_collection_name = create_new_collection(
                    client, collection_name, schema
                )

                # Migrate data
                migrated_count = migrate_collection_data(
                    client, collection_name, new_collection_name
                )

                # Verify migration
                success = verify_migration(client, collection_name, new_collection_name)

                if success:
                    print(f"\nMigration successful for {collection_name}!")
                    print(f"New collection: {new_collection_name}")

                    # Automatically replace old collection with migrated one
                    try:
                        replace_old_collection(
                            client, collection_name, new_collection_name
                        )
                    except Exception as e:
                        print(
                            f"\nWarning: Could not automatically replace collection: {e}"
                        )
                        print(f"\nTo activate manually:")
                        print(f"1. Delete the old collection: {collection_name}")
                        print(f"2. Rename {new_collection_name} to {collection_name}")

            except Exception as e:
                print(f"\nError migrating {collection_name}: {e}")
                print(f"Skipping this collection and continuing...")
                continue

        print("\n" + "=" * 80)
        print("Migration Complete!")
        print("=" * 80)
        print("\nSummary:")
        print(f"  Collections migrated: {len(collections_to_migrate)}")

    finally:
        client.close()


if __name__ == "__main__":
    try:
        migrate_all_collections()
    except KeyboardInterrupt:
        print("\n\nMigration interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
