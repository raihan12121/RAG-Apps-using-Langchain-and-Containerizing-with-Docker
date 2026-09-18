from langchain_community.vectorstores import FAISS


class VectorStore:
    """
    FAISS-based vector store for document retrieval.
    """

    def __init__(self, embedding):
        self.embeddings = embedding
        self.store = None

    def build(self, texts: list[str]):
        """
        Build FAISS index from text chunks.
        """
        self.store = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings.model
        )

    def search(self, query: str, k: int = 3) -> list[str]:
        """
        Retrieve top-K relevant chunks.
        """
        if self.store is None:
            raise ValueError("Vector store not initialized")

        docs = self.store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
