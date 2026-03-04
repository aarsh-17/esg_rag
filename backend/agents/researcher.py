from ..vectorstore.retriever import retriever

BGE_PREFIX = "Represent this sentence for searching relevant passages: "

def clean_citations(citations):
    seen = set()
    cleaned = []

    for c in citations:
        key = (c["source"], c["page"], c["chunk_id"])
        if key not in seen:
            seen.add(key)
            cleaned.append(c)

    return cleaned


def researcher(state):
    query = BGE_PREFIX + state["query"]

    docs_with_scores = retriever.vectorstore.similarity_search_with_score(
        query,
        k=5
    )

    if not docs_with_scores:
        return {
            **state,
            "context": "",
            "documents": [],
            "citations": [],
            "top_3_chunks": [],
            "top_similarity": 0.0
        }

    # Top similarity score
    top_similarity = float(docs_with_scores[0][1])

    # First 3 chunk texts
    top_3_chunks = [
        {
            "chunk_id": doc.metadata.get("chunk_id"),
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "text": doc.page_content,
            "score": float(score)
        }
        for doc, score in docs_with_scores[:3]
    ]

    citations = [
        {
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "score": float(score)
        }
        for doc, score in docs_with_scores
    ]

    citations = clean_citations(citations)

    context = "\n\n".join(doc.page_content for doc, _ in docs_with_scores)

    return {
        **state,
        "context": context,
        "documents": [doc for doc, _ in docs_with_scores],
        "citations": citations,
        "top_3_chunks": top_3_chunks,
        "top_similarity": top_similarity
    }