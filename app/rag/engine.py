import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.core.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL_NAME,
    GROQ_MODEL_NAME,
    PDF_PATH,
    TOP_K,
)
from app.rag.chunker import LangchainTextChunker
from app.rag.embeddings import EmbeddingModel
from app.rag.loader import PDFLoader
from app.rag.vectorstore import VectorStore


class RAGEngine:
    """
    Singleton-style RAG Engine.
    """

    def __init__(self):
        self.vector_store = None
        self.llm = None
        self._initialize()

    def _initialize(self):
        load_dotenv(override=True)

        text = PDFLoader(PDF_PATH).load()
        chunks = LangchainTextChunker(CHUNK_SIZE, CHUNK_OVERLAP).chunk(text)

        embeddings = EmbeddingModel(EMBEDDING_MODEL_NAME)
        self.vector_store = VectorStore(embeddings)
        self.vector_store.build(chunks)

        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.llm = ChatGroq(model=GROQ_MODEL_NAME, api_key=api_key)

    def generate_answer(self, question: str) -> str:
        """
        Generate an answer using the vector store with a grounded prompt.
        """
        if self.llm is None:
            load_dotenv(override=True)
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY is not set. Please add your Groq API key to the .env file.")
            self.llm = ChatGroq(model=GROQ_MODEL_NAME, api_key=api_key)

        contexts = self.vector_store.search(query=question, k=TOP_K)
        combined_texts = "\n\n".join(contexts)

        prompt = f"""You are a helpful assistant. Use only the information provided in the context below to answer the question.
If the answer is not present in the context, respond with "I don't know".

Context:
{combined_texts}

Question: {question}

Answer:"""

        response = self.llm.invoke(prompt)
        return response.content
