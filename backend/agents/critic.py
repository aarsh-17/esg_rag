from ..llm import llm

def critic(state):
    verdict = state.get("verdict", "")
    context = state.get("context", "")
    claim = state.get("query", "")
    confidence = state.get("confidence", 0.0)

    prompt = f"""
You are evaluating potential greenwashing.

Determine whether the CONTEXT provides substantive evidence that meaningfully supports the CLAIM.

Substantive evidence means:
- Concrete actions with measurable impact
- Specific outcomes, results, or data
- Clear elaboration beyond generic intention language

If the context only repeats intention, ambition, or vague commitments without measurable support, respond NO.

Respond only YES or NO.

CLAIM:
{claim}

CONTEXT:
{context}
"""

    response = llm.invoke(prompt).strip().upper()

    grounded = response == "YES"
    print(f"Critic response: {response} (grounded: {grounded})")

    # Adjust confidence
    if grounded:
        confidence = round(confidence + 0.4, 3)
    else:
        confidence = round(confidence * 0.5, 3)

    return {
        **state,
        "grounded": grounded,
        "confidence": confidence
    }