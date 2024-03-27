import ollama

from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder, OllamaTextEmbedder

from ollama_rag.helpers import CachedInMemoryDocumentStore

class Chat:
    def __init__(self):
        self.history = []
        self.document_store =  CachedInMemoryDocumentStore()

    def get_response(self, message):
        self.history.append({'role': 'user', 'content': message})

        context = self.retrieve_relevant_documents(message)[0].content

        print(f'Context:\n{context}\n')

        system_message = {
            'role': 'system',
            'content': f'''
                You are a research assistant who is really good at answering questions about documents.
                Your tone is professional, your answers are typically 1-3 sentences, and you never use emoji.

                Here is some context that might be helpful to answer the next question:

                {context}
            '''
        }
        messages = [system_message] + self.history

        response = ''
        for chunk in ollama.chat('llama2', messages, stream=True):
            response += chunk['message']['content']
            yield response

        self.history.append({'role': 'assistant', 'content': response})

    def retrieve_relevant_documents(self, message):
        pipeline = Pipeline()

        pipeline.add_component('embedder', OllamaTextEmbedder())
        pipeline.add_component('retriever', InMemoryEmbeddingRetriever(self.document_store, top_k=1))

        pipeline.connect('embedder.embedding', 'retriever.query_embedding')

        return pipeline.run({'embedder': {'text': message}})['retriever']['documents']

    def index_documents(self, documents):
        pipeline = Pipeline()

        if self.document_store.cached:
            return

        pipeline.add_component('converter', PyPDFToDocument())
        pipeline.add_component('cleaner', DocumentCleaner())
        pipeline.add_component('splitter', DocumentSplitter('sentence', split_length=5, split_overlap=1))
        pipeline.add_component('embedder', OllamaDocumentEmbedder())
        pipeline.add_component('writer', DocumentWriter(self.document_store))

        pipeline.connect('converter', 'cleaner')
        pipeline.connect('cleaner', 'splitter')
        pipeline.connect('splitter', 'embedder')
        pipeline.connect('embedder', 'writer')

        pipeline.run({'converter': {'sources': documents}})
