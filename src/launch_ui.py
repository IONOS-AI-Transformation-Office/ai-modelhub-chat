from nicegui import ui

from paths import STORAGE_SECRET
from ui.components import show_header, show_footer, show_chat, init_history

@ui.page('/')
def show():
    """
    Show chat in browser.
    """
    ui.page_title("AI Model Hub - Testbot")
    show_header()
    show_footer()
    show_chat()
    

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(storage_secret=STORAGE_SECRET)