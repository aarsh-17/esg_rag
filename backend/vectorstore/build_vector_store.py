import json
import faiss
import numpy as np
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from backend.embeddings import get_embeddings
from backend.vectorstore.load_data import load_documents
from backend.vectorstore.chunk_data import chunk_documents


def build_vectorstore():
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"\nTotal chunks: {len(chunks)}")

    # Save chunks preview
    export_data = []
    for chunk in chunks:
        export_data.append({
            "chunk_id": chunk.metadata.get("chunk_id"),
            "page": chunk.metadata.get("page"),
            "source": chunk.metadata.get("source"),
            "text": chunk.page_content
        })

    export_path = Path("vectorstore/chunks_preview.json")
    export_path.parent.mkdir(parents=True, exist_ok=True)

    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"Saved chunk preview JSON to {export_path}")

    # ---------------------------
    # Build Flat Cosine Index
    # ---------------------------

    embeddings = get_embeddings()

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    # Already normalized via encode_kwargs
    vectors = np.array(embeddings.embed_documents(texts)).astype("float32")
    dimension = vectors.shape[1]

    # Flat Inner Product (Cosine)
    index = faiss.IndexFlatIP(dimension)

    index.add(vectors)

    print("Metric type:", index.metric_type)  # 0 = inner product

    docstore = InMemoryDocstore(
        {str(i): chunks[i] for i in range(len(chunks))}
    )
    index_to_docstore_id = {i: str(i) for i in range(len(chunks))}

    db = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=docstore,
        index_to_docstore_id=index_to_docstore_id
    )

    db.save_local("vectorstore/faiss_index_flat")

    print("Flat cosine vector store built successfully.")


if __name__ == "__main__":
    build_vectorstore()