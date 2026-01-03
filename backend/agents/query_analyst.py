from backend.llm import llm

def query_analyst(state):
    prompt = f"""
Rewrite the following query to be precise and searchable.

Query:
{state['query']}
"""
    rewritten_query = llm.invoke(prompt)
    print(f"\n--- REWRITTEN QUERY ---\n{rewritten_query}\n")
    state["rewritten_query"] = rewritten_query
    return {
        **state,
        "rewritten_query": rewritten_query
    }
