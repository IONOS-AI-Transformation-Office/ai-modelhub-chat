import os

# A private key to secure the session cookie
# IMPORTANT: replace this, when using this project
STORAGE_SECRET = 'REPLACE ME!'

# Load the API Token from environment variables
IONOS_API_TOKEN = os.environ.get('IONOS_API_TOKEN')

# Generate the HEADERS using the API Token
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {IONOS_API_TOKEN}',
}

# The maximum number of pages to extract from a PDF when filling the vector db.
MAX_PAGES = 10

# Data backend to be used. Chose from 'chromadb' and 'pgvector'
DATA_BACKEND = 'pgvector'
# Embedding model to be used when writing embeddings to the vector db.
EMBEDDING_MODEL = 'BAAI/bge-m3'
# Size of chunks in which to devide the documents when loading them to the vector db.
CHUNK_SIZE = 1000
# Number of tokens for which the chunks overlap when loading them to the vector db.
CHUNK_OVERLAP = 50

# Name of the large language model to be used when generating answers.
LLM_NAME = 'meta-llama/Meta-Llama-3.1-8B-Instruct'
# Base url of the OpenAI endpoint to be used when applying the Large Language Model
LLM_BASE_URL = 'https://openai.inference.de-txl.ionos.com/v1'

# Instructions how the chat should behave when answering queries. Notice,
# that these instructions can be used to enforce answering in certain 
# languages or limiting the answert to a certain set of topics.
CHAT_INSTRUCTIONS = """
    You are helpful assistant who always answers in German.
    You only answer question concering the Magnificent Hoster.
    If you get any other questions politly answer that you cannot help.
"""
# Initial question to be shown in the chat to welcome the user.
CHAT_INITIAL_QUESTION = "Hallo! Wie kann ich dir helfen?"

# Caption on top of the chat window
CHAT_HEADER_TITLE = 'My first chat powered by IONOS AI Model Hub'
# Background color of the title bar of the chat.
CHAT_HEADER_COLOR = '#061A3E'

# Placeholder to be shown in the input area before the user entered the first query.
CHAT_FOOTER_PLACEHOLDER = 'start typing...'
# Background color of the footer.
CHAT_FOOTER_COLOR = '#FFFFFF'