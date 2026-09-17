from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingModel:

    """
    Wrapper around sententransformer embeddings
    """

    def __init__(self):
        self.model=HuggingFaceEmbeddings(
            model_name=model_name
        )
    
    def embed_documents(self,texts):
        return self.model.embed_documents(texts)


    def embed_query(self, query: str):
        return self.model.embed_query(query)
        