from nicegui import app
from config import CHAT_INSTRUCTIONS, CHAT_INITIAL_QUESTION
from aimodelhub.vectordb import retrieve_documents, retrieve_id

def get_history():
    """
    Complete chat history in the current chat.
    Returns:
        str: Chat history.
    """
    if 'history' not in app.storage.client:
        init_history()

    return app.storage.client['history']


def init_history():
    """
    Initialises / resets the history of the chat.

    Namely, it replaces the chat history with the instructions to the LLM and the
    question to be initially displayed to the user.
    """
    app.storage.client['history'] = [ 
        {'role': 'developer', 'content': CHAT_INSTRUCTIONS, 'sent': False},
        {'role': 'system', 'content': CHAT_INITIAL_QUESTION, 'sent': False}  
    ]


def append_to_history(message):
    """
    Appends a new message to the chat history list.
    Args:
        message (dict): message to append.
    """
    history = get_history()
    history.append(message)
    app.storage.client['history'] = history


def get_llm_prompt(query):
    """
    Takes a query as input, searches for all relevant documents in the vector database
    and appends it to the chat history. The result is returned as prompt for the LLM.
    Args:
        query (str): Query the user entered into the chat window.
    Returns:
        list: Prompt to be used as the input of the LLM.
    """
    relevant_docs = retrieve_documents(collection_id=retrieve_id(), query_string=query)
    print(f"The most relevant content is in files: {[entry['file_name'] for entry in relevant_docs]}")
    prompt = [
        {"role": "system", "content": "; ".join([entry['content'] for entry in relevant_docs])},
    ]
    prompt.extend(get_history())

    return prompt