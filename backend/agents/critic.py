import backend.llm as llm
def critic(state):
    context = state.get("context", "")
    answer = state.get("answer", "")

    if not context.strip():
        # No context = cannot verify grounding
        state["grounded"] = False
        return {**state, "grounded": False}

    prompt = f"""
Does the ANSWER rely strictly on the CONTEXT below?

Respond only YES or NO.

CONTEXT:
{context}

ANSWER:
{answer}
"""

    verdict = "yes" if answer.lower() in context.lower() else "no"
   

    return {
        **state,
        "grounded": verdict == "yes"
    }

