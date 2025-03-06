import requests
import os
import base64

from paths import HEADERS, CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL, DATA_BACKEND
from aimodelhub.documents import extract_text


def create_collection(collection_name, collection_description):
    """
    Creates a collection in IONOS AI Model Hub.
    Args:
        collection_name (str): The name of the collection.
        collection_description (str): A description of the collection.
    Returns:
        str: The ID of the created collection.
    """
    endpoint = "https://inference.de-txl.ionos.com/collections"
    # Define the payload for creating a collection
    body = {
        "type": "collection",
        "properties": {
            "name": collection_name,
            "description": collection_description,
            "chunking": {
                "enabled": True,
                "strategy": {
                    "config": {
                        "chunk_overlap": CHUNK_OVERLAP, 
                        "chunk_size": CHUNK_SIZE
                    }
                }
            },
            "embedding": {
                "model": EMBEDDING_MODEL
            },
            "engine": {
                "db_type": DATA_BACKEND
            }
        }
    }

    # Send the request to create the collection
    response = requests.post(endpoint, headers=HEADERS, json=body)

    # Check for errors
    if response.status_code != 201:
        print(f"Error creating collection: {response.status_code} - {response.text}")
        return None

    # Get the collection ID from the response
    collection_id = response.json()["id"]
    print("Collection ID:", collection_id)
    return collection_id


def add_files_to_collection(collection_id, folder_path, max_pages=None):
    """
    Adds files from a folder to the specified collection.
    Args:
        collection_id (str): The ID of the collection.
        folder_path (str): The path to the folder containing the files.
        max_pages (int, optional): The maximum number of pages to extract from PDFs. Defaults to None.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(f"Processing: {filename}")
            text = extract_text(file_path, max_pages)
            if text:
                add_document_to_collection(collection_id, filename, text)


def add_document_to_collection(collection_id, file_name, text):
    """
    Adds a single document to the collection.
    Args:
        collection_id (str): The ID of the collection.
        file_name (str): The name of the file (used for the document name).
        text (str): The extracted text content of the file.
    """
    endpoint = f"https://inference.de-txl.ionos.com/collections/{collection_id}/documents"
    # Define the payload
    body = {
        "type": "collection",
        "items": [
            {
                "type": "document",
                "properties": {
                    "name": file_name,
                    "contentType": "text/plain",
                    "content": base64.b64encode(text.encode("utf-8")).decode("utf-8")
                }
            }
        ]
    }
    # Send the request to add the document
    response = requests.put(endpoint, headers=HEADERS, json=body)

    if response.status_code == 200:
        print(f"Document '{file_name}' added to collection.")
    else:
        print(f"Error adding document '{file_name}': {response.status_code} - {response.text}")


def retrieve_documents(collection_id, query_string, num_documents=3):
    """
    Retrieves documents from the specified collection which are semantically most similar to the
    query string.
    Args: 
        collection_id (str): The ID of the collection to query.
        query_string (str): The natural language query.
        num_documents (int, optional): The number of documents to retrieve.
    Returns:
        list: The results from the document collection.
    """
    endpoint = f"https://inference.de-txl.ionos.com/collections/{collection_id}/query"
    body = {"query": query_string, "limit": num_documents }
    relevant_documents = requests.post(endpoint, json=body, headers=HEADERS)

    return [
        {
            'file_name': entry['document']['properties']['name'],
            'content': base64.b64decode(entry['document']['properties']['content']).decode()
        } for entry in relevant_documents.json()['properties']['matches']
    ]


def query_collection(collection_id, query_string, model_name="meta-llama/Llama-3.3-70B-Instruct", max_length=300, temperature=0.01):
    """
    Queries the collection and generates a response using a large language model.
    Args:
        collection_id (str): The ID of the collection to query.
        query_string (str): The natural language query.
        model_name (str, optional): The model name of the language generation model.
        max_length (int, optional): The maximum length of the generated response. Defaults to 300.
        temperature (float, optional): Controls the randomness of the model's output. Defaults to 0.01.
    Returns:
        dict: The response from the model, including the generated text.
    """
    endpoint = "https://openai.inference.de-txl.ionos.com/v1/chat/completions"
    relevant_docs = retrieve_documents(collection_id=collection_id, query_string=query_string)
    print(f"The most relevant content is in files: {[entry['file_name'] for entry in relevant_docs]}")
    prompt = [
        {"role": "system", "content": """
            Please use the information specified as context to answer the question.
            Formulate you answer in one sentence and be an honest AI. Answer in a list
            of five bullet points each starting with a year and the milestone in about 20 words.
         """},
        {"role": "system", "content": "; ".join([entry['content'] for entry in relevant_docs])},
        {"role": "user", "content": query_string}
    ]
    body = {
        "model": model_name,
        "messages": prompt,
    }
    response = requests.post(endpoint, json=body, headers=HEADERS)

    if response.status_code == 200:
        results = response.json()['choices'][0]['message']['content']
        return results
    else:
        print(f"Error querying collection: {response.status_code} - {response.text}")
        return None


def delete_collection(collection_id):
    """
    Deletes the collection specified.
    Args:
        collection_id (str): The ID of the collection to delete.
    """
    response = requests.delete(
        f"https://inference.de-txl.ionos.com/collections/{collection_id}", 
        headers=HEADERS
    )

    if response.status_code == 204:
        print(f"Deleted collection: {collection_id}")
    elif response.status_code == 404:
        print(f"Collection to delete did not exist: {collection_id}")
    else:
        print(f"Error deleting collection: {response.status_code} - {response.text}")


def persist_id(collection_id, filename="data/collection_id.txt"):
    """
    Persists the collection_id in a file so that it can be accessed from the frontend
    Args:
        collection_id (str): The ID of the collection to persist.
        filename (str, optional): The file in which the collection ID is persisted.
    """
    file = open(filename, "w")
    file.write(collection_id)
    file.close()


def retrieve_id(filename="data/collection_id.txt"):
    """
    Retrieve the collection_id from a file it has be persisted to
    Args:
        filename (str, optional): The file in which the collection ID is persisted.
    Returns:
        str: Collection ID persisted in file.
    """
    if os.path.isfile(filename):
        file = open(filename, "r")
        return file.read()
    
    print(f"The file holding the collection ID ({filename}) does not exist.")


def delete_persisted_id(filename="data/collection_id.txt"):
    """
    Delete the file in which the collection ID is persisted.
    Args:
        filename (str, optional): The file in which the collection ID is persisted.
    """
    if os.path.isfile(filename):
        os.remove(filename)
