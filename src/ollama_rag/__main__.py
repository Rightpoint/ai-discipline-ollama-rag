import sys
import gradio
from pathlib import Path

from ollama_rag.chat import Chat

def main():
    chat = Chat()
    chat.index_documents([Path(__file__).parent.parent.parent / 'documents' / 'Searle (1980) - The Chinese Room.pdf'])

    def get_response(message, _):
        for chunk in chat.get_response(message):
            yield chunk
    
    gradio.ChatInterface(get_response).launch()

sys.exit(main())
