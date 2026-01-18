from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter




class VectorStoreService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        self.vector_store = Chroma(
            collection_name="web_knowledge",
            embedding_function=self.embeddings,
            persist_directory="chroma_db"
        )

    def add_text(self, text: str, metadata: dict):
        chunks = self.text_splitter.split_text(text)

        self.vector_store.add_texts(
            texts=chunks,
            metadatas=[metadata] * len(chunks)
        )

        self.vector_store.persist()

    def search(self, query: str, k: int = 3):
        return self.vector_store.similarity_search(query, k=k)
    
    def retrieve_context(self, query: str, k: int = 2):
        docs = self.vector_store.similarity_search(query, k=k)

        context_text = ""
        sources = set()

        for doc in docs:
            context_text += doc.page_content + "\n\n"
            if "source" in doc.metadata:
                sources.add(doc.metadata["source"])

        return context_text.strip(), list(sources)


