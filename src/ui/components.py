from nicegui import app, ui
from langchain_openai import ChatOpenAI
from datetime import datetime

from config import (
    CHAT_BOT_IMAGE, CHAT_BOT_NAME, CHAT_HEADER_TITLE, CHAT_HEADER_COLOR,
    CHAT_FOOTER_PLACEHOLDER, CHAT_FOOTER_COLOR, CHAT_USER_IMAGE, CHAT_USER_NAME,
    IONOS_API_TOKEN, LLM_NAME, LLM_BASE_URL, 
)
from ui.history import append_to_history, get_history, get_llm_prompt


def show_header():
    """
    Display header of the chat window with the name of the bot.
    """
    with (
        ui.header(elevated=True).style(f'background-color: {CHAT_HEADER_COLOR}'), 
        ui.column().classes('w-full max-w-3xl mx-auto')
    ):
        with ui.row().classes('w-full no-wrap items-center'):
            (
                ui.label(CHAT_HEADER_TITLE)
                  .style('color: #ffffff; font-size: 150%; font-weight: 300')
            )


def show_footer():
    """
    Display the footer of the chat window with the input element for messages.
    """
    with (
        ui.footer().style(f'background-color: {CHAT_FOOTER_COLOR}'), 
        ui.column().classes('w-full max-w-3xl mx-auto my-6')
    ):
        with ui.row().classes('w-full no-wrap items-center'):
            (
                ui.input(placeholder=CHAT_FOOTER_PLACEHOLDER)
                  .on('keydown.enter', lambda event: post_message(event.sender))
                  .props("rounded outlined input-class=mx-3 size=100")
            )


@ui.refreshable
def show_chat():
    """
    Display all chat messages and scroll to the end of the chat window.
    """
    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        for entry in get_history():
            if entry['role'] in ['system', 'user']:
                display_message(entry)     
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')


def display_message(message: dict):
    """
    Takes a message from the chat history and displays it in the chat window.
    Args:
        massage (dict): The content of the message.
    """
    ui.chat_message(message['content'],
        name=get_sender(message['role']),
        sent=message['sent'],
        stamp=get_time_delta(message['time']) if 'time' in message else '',
        avatar=get_avatar(message['role'])
    ).style('size: 12; width: 100%').classes('justify-center')


def get_time_delta(time_string):
    """
    Calculates the number of seconds / minutes that passed, since the 
    point in time represented by the time_string.
    Args:
        time_string (str): A point in time represented as string in format "%Y-%m-%dT%H:%M:%S".
    Returns:
        str: The seconds / minutes passes since the time_string in format ".. sec ago".
    """
    time = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S")
    time_delta = (datetime.now()-time).total_seconds()
    if time_delta < 60:
        return f"{time_delta:1.0f} sec ago"
    else:
        minutes = ((datetime.now()-time).total_seconds() // 60)
        return f"{minutes:1.0f} min ago"
        

def get_sender(sender_string):
    """
    Derives a human readable string from the OpenAI sender strings
    Args:
        sender_string (str): The OpenAI sender string to convert.
    Returns:
        str: 'IONOS powered AI' if sender is 'system' and 'you' if sender is 'user'.
    """    
    if sender_string == 'system':
        return CHAT_BOT_NAME
    if sender_string == 'user':
        return CHAT_USER_NAME


def get_avatar(sender_string):
    """
    Derives a avatar image links from the OpenAI sender strings.
    Args:
        sender_string (str): The OpenAI sender string to convert.
    Returns:
        str: Bot if sender is 'system' and face if sender is 'user'.
    """
    if sender_string == 'system':
        return CHAT_BOT_IMAGE
    if sender_string == 'user':
        return CHAT_USER_IMAGE


async def post_message(query_field):
    """
    Invoked after the user clicks 'enter' in the input field. Adds
    the typed message to the message history, generates the LLM 
    answer and displays everything in the chat window.
    Args:
        query_field (ui.input): Field capturing the user input.
    """
    query = query_field.value
    query_field.value = ''
    show_user_message(query)
    show_bot_message()

    llm = ChatOpenAI(
        model_name=LLM_NAME, 
        streaming=True, 
        base_url=LLM_BASE_URL, 
        openai_api_key=IONOS_API_TOKEN
    )
    async for chunk in llm.astream(get_llm_prompt(query)):
        get_history()[-1]['content'] += chunk.content
        show_chat.refresh()


def show_user_message(query):
    """
    Formats a query entered by the user and adds it to the history list.
    Args:
        query (str): Message entered by the user.
    """
    append_to_history({
        'role': 'user', 
        'content': query, 
        'sent': True, 
        'time': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")
    })
    show_chat.refresh()


def show_bot_message():
    """
    Adds an empty message to the history list.
    """
    append_to_history({'role': 'system', 'content': '', 'sent': False})
    show_chat.refresh()
