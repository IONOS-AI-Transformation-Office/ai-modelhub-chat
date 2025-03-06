import argparse

from aimodelhub.vectordb import create_collection, add_files_to_collection, delete_collection, query_collection, persist_id
from aimodelhub.models import get_models, print_models
from paths import MAX_PAGES


def prepare_collection(collection_name, input_path):
    """
    Prepares the collection by creating it and uploading all documents in the input path.
    Args:
        collection_name (str): The name of the collection to create.
        input_path (str): The input path with all documents to upload.
    Returns:
        str: The ID of the collection. This ID will be used to query the collection.
    """
    collection_description = f"This is a demo collection called {collection_name}"
    collection_id = create_collection(collection_name, collection_description)

    if collection_id:
        add_files_to_collection(collection_id, input_path, MAX_PAGES)

    return collection_id


def query(collection_id, query_string):
    """
    Query the collection.
    Args:
        collection_id (str): Collection ID of the collection to query.
        query_string (str): The user query to be answered using the data uploaded to the collection.
    """
    if collection_id:
        generated_text = query_collection(collection_id, query_string)

        if generated_text:
            print("Query Result:")
            print(generated_text)


def next_steps():
    """
    Display the supported models to be used alternatively
    """
    print("Not satisfied with the results? Use another model from our list:")

    models = get_models()
    print_models(models)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an image based on input text and specified orientation.")
    parser.add_argument('--collection_name', type=str, default='Test collection', help="Name of the collection to persist data.")
    parser.add_argument('--input_path', type=str, default='input', help="Path to search for documents to upload to document collection")
    
    args = parser.parse_args()

    collection_id = prepare_collection(collection_name=args.collection_name, input_path=args.input_path)
    persist_id(collection_id=collection_id)

    next_steps()
