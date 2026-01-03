from ..vectorstore.retriever import retriever

def clean_citations(citations):
    seen = set()
    cleaned = []

    for c in citations:
        key = (c["source"], c["page"], c["score"])
        if key not in seen:
            seen.add(key)
            cleaned.append(c)

    return cleaned


def researcher(state):
    print("\n Entered Researcher \n")
    # Retrieve documents
    docs_with_scores = retriever.vectorstore.similarity_search_with_score(
    state["rewritten_query"],
    k=5
    )
    citations = []
    for doc,score in docs_with_scores:
        citations.append({
            "source": doc.metadata.get("title", "Unknown"),
            "page": doc.metadata.get("page"),
            "score": score
        })
    


    # Combine retrieved content into grounded context
    context = "\n\n".join(doc.page_content for doc, score in docs_with_scores)
    print("✅ CONTEXT LENGTH:", len(context))

    citations = clean_citations(citations)
    citations = sorted(citations, key=lambda x: x["score"])
    return {
        **state,
        "context": context,
        "citations": citations,
        "documents": docs_with_scores,
    }
