import argparse

from aimodelhub.vectordb import retrieve_id, delete_collection, delete_persisted_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deletes a collection of the user.")
    parser.add_argument('--collection_id', type=str, default=None, help="ID of the collection to delete.")
    
    args = parser.parse_args()

    if args.collection_id is None:
        collection_id = retrieve_id()
    else:
        collection_id = args.collection_id

    delete_collection(collection_id=collection_id)
    delete_persisted_id()