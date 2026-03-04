from langchain_community.vectorstores import FAISS
from ..embeddings import get_embeddings

embeddings = get_embeddings()

db = FAISS.load_local(
    "vectorstore/faiss_index_flat",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 5})