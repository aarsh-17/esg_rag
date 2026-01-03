from typing import Dict
from ..llm import llm   # adjust import if needed

def reasoner(state):
  
    context = state.get("context", "")
    question = state.get("rewritten_query", "")


    prompt = f"""
You must answer ONLY using the provided context.
You are NOT allowed to use outside knowledge.

If the answer is not explicitly stated in the context,
respond exactly with:
"Information not found in the provided documents."

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt)

    state["answer"] = answer
    state["done"] = True
    return {
        **state,
        "answer": answer,
        "done": True
    }
