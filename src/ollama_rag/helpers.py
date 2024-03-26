from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.document_stores.types import DuplicatePolicy
from typing import Dict, List, Literal
from pathlib import Path
import json


class CachedInMemoryDocumentStore(InMemoryDocumentStore):
    def __init__(self, bm25_tokenization_regex: str = r"(?u)\b\w\w+\b", bm25_algorithm: Literal['BM25Okapi'] | Literal['BM25L'] | Literal['BM25Plus'] = "BM25L", bm25_parameters: Dict | None = None, embedding_similarity_function: Literal['dot_product'] | Literal['cosine'] = "dot_product"):
        super().__init__(bm25_tokenization_regex, bm25_algorithm, bm25_parameters, embedding_similarity_function)

        self.cache_path = Path(__file__).parent.parent.parent / '.document_store_cache'
        self.cached = False
        self._load_cache()

    def write_documents(self, documents: List[Document], policy: DuplicatePolicy = DuplicatePolicy.NONE) -> int:
        documents = super().write_documents(documents, policy)
        self._write_cache()
        return documents

    def _load_cache(self):
        if self.cache_path.exists():
            with open(self.cache_path, 'r') as cache:
                documents = [Document.from_dict(document) for document in json.load(cache)]
            self.write_documents(documents)
            self.cached = True
    
    def _write_cache(self):
        with open(self.cache_path, 'w') as cache:
            documents = [document.to_dict() for document in self.storage.values()]
            json.dump(documents, cache)
        self.cached = True
