"""
Migration script to fix Weaviate schema incompatibility between 1.19.0 and 1.27.0+
This script:
- Identifies collections with old schema (no vectorConfig)
- Creates new collections with proper vectorConfig including "default" named vector
- Migrates data using cursor-based pagination (efficient for large datasets)
- Uses batch operations for fast inserts
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
import weaviate
from weaviate.classes.config import Configure, VectorDistances
import sys
import time
from typing import List, Dict, Any

# Configuration
WEAVIATE_ENDPOINT = os.getenv("WEAVIATE_ENDPOINT", "http://weaviate:8080")
WEAVIATE_GRPC_ENDPOINT = os.getenv("WEAVIATE_GRPC_ENDPOINT", "grpc://weaviate:50051")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "WVF5YThaHlkYwhGUSmCRgsX3tD5ngdN8pkih")
BATCH_SIZE = 1000
WEAVIATE_HOST = WEAVIATE_ENDPOINT.split("//")[-1].split(":")[0]
WEAVIATE_PORT = int(WEAVIATE_ENDPOINT.split(":")[-1])
WEAVIATE_GRPC_PORT = int(WEAVIATE_GRPC_ENDPOINT.split(":")[-1])


def identify_old_collections(client: weaviate.WeaviateClient) -> List[str]:
    """Identify collections that need migration (those without vectorConfig)"""
    collections_to_migrate = []

    all_collections = client.collections.list_all()
    print(f"Found {len(all_collections)} total collections")

    for collection_name in all_collections.keys():
        # Only check Vector_index collections (Dify knowledge bases)
        if not collection_name.startswith("Vector_index_"):
            continue

        collection = client.collections.get(collection_name)
        config = collection.config.get()

        # Check if this collection has the old schema
        if config.vector_config is None:
            collections_to_migrate.append(collection_name)
            print(f"  - {collection_name}: OLD SCHEMA (needs migration)")
        else:
            print(f"  - {collection_name}: NEW SCHEMA (skip)")

    return collections_to_migrate


def get_collection_schema(
    client: weaviate.WeaviateClient, collection_name: str
) -> Dict[str, Any]:
    """Get the full schema of a collection via REST API"""
    import requests

    response = requests.get(
        f"http://{WEAVIATE_HOST}:{WEAVIATE_PORT}/v1/schema/{collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get schema: {response.text}")


def create_new_collection(
    client: weaviate.WeaviateClient, old_name: str, schema: Dict[str, Any]
) -> str:
    """Create a new collection with updated schema using REST API"""
    import requests

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

    # Copy properties from old schema
    if "properties" in schema:
        new_schema["properties"] = schema["properties"]

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


def migrate_collection_data(
    client: weaviate.WeaviateClient, old_collection_name: str, new_collection_name: str
) -> int:
    """Migrate data from old collection to new collection using cursor-based pagination"""

    old_collection = client.collections.get(old_collection_name)
    new_collection = client.collections.get(new_collection_name)

    total_migrated = 0
    cursor = None

    print(f"Migrating data from {old_collection_name} to {new_collection_name}")

    while True:
        # Fetch batch of objects using cursor-based pagination
        if cursor is None:
            # First batch
            response = old_collection.query.fetch_objects(
                limit=BATCH_SIZE, include_vector=True
            )
        else:
            # Subsequent batches using cursor
            response = old_collection.query.fetch_objects(
                limit=BATCH_SIZE, include_vector=True, after=cursor
            )

        objects = response.objects

        if not objects:
            break

        # Use batch insert for efficiency
        with new_collection.batch.dynamic() as batch:
            for obj in objects:
                # Prepare properties
                properties = obj.properties

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

        total_migrated += len(objects)
        print(f"  Migrated {total_migrated} objects...")

        # Update cursor for next iteration
        if len(objects) < BATCH_SIZE:
            # Last batch
            break
        else:
            # Get the last object's UUID for cursor
            cursor = objects[-1].uuid

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
    """Replace old collection with migrated one by recreating with original name"""
    import requests

    print(f"\nReplacing old collection with migrated data...")

    # Step 1: Delete old collection
    print(f"  Step 1: Deleting old collection...")
    response = requests.delete(
        f"{WEAVIATE_ENDPOINT}/v1/schema/{old_collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    if response.status_code != 200:
        print(f"    Warning: Could not delete old collection: {response.text}")
    else:
        print(f"    Deleted")

    # Step 2: Get schema from migrated collection
    print(f"  Step 2: Getting schema from migrated collection...")
    schema_response = requests.get(
        f"{WEAVIATE_ENDPOINT}/v1/schema/{new_collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    schema = schema_response.json()
    schema["class"] = old_collection_name

    # Step 3: Create collection with original name and new schema
    print(f"  Step 3: Creating collection with original name...")
    create_response = requests.post(
        f"{WEAVIATE_ENDPOINT}/v1/schema",
        json=schema,
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    if create_response.status_code not in [200, 201]:
        raise Exception(f"Failed to create collection: {create_response.text}")
    print(f"    Created")

    # Step 4: Copy data to collection with original name using cursor-based pagination
    print(f"  Step 4: Copying data to original collection name...")
    migrated_collection = client.collections.get(new_collection_name)
    new_collection = client.collections.get(old_collection_name)

    total_copied = 0
    cursor = None

    while True:
        # Fetch batch of objects using cursor-based pagination
        if cursor is None:
            # First batch
            response = migrated_collection.query.fetch_objects(
                include_vector=True, limit=BATCH_SIZE
            )
        else:
            # Subsequent batches using cursor
            response = migrated_collection.query.fetch_objects(
                include_vector=True, limit=BATCH_SIZE, after=cursor
            )

        objects = response.objects

        if not objects:
            break

        # Use batch insert for efficiency
        with new_collection.batch.dynamic() as batch:
            for obj in objects:
                batch.add_object(
                    properties=obj.properties, vector=obj.vector, uuid=obj.uuid
                )

        total_copied += len(objects)
        print(f"    Copied {total_copied} objects...")

        # Update cursor for next iteration
        if len(objects) < BATCH_SIZE:
            break
        else:
            cursor = objects[-1].uuid

    print(f"    Total copied: {total_copied} objects")

    # Step 5: Delete the temporary migrated collection
    print(f"  Step 5: Cleaning up temporary migrated collection...")
    response = requests.delete(
        f"{WEAVIATE_ENDPOINT}/v1/schema/{new_collection_name}",
        headers={"Authorization": f"Bearer {WEAVIATE_API_KEY}"},
    )
    if response.status_code == 200:
        print(f"    Cleaned up")

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
