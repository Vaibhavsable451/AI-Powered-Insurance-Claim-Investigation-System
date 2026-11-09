class EvidenceIndex:
    """Optional in-memory FAISS index for semantic evidence lookup."""
    def __init__(self):
        self.vectorstore = None

    def build(self, text: str) -> bool:
        try:
            from langchain_community.vectorstores import FAISS
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_core.documents import Document
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            chunks = [text[i:i+900] for i in range(0, len(text), 750)]
            docs = [Document(page_content=c, metadata={"chunk": i}) for i, c in enumerate(chunks)]
            self.vectorstore = FAISS.from_documents(docs, embeddings)
            return True
        except Exception:
            self.vectorstore = None
            return False

    def search(self, query: str, k: int = 3):
        if self.vectorstore is None:
            return []
        return self.vectorstore.similarity_search(query, k=k)
