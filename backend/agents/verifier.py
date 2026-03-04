from ..llm import llm

SIMILARITY_THRESHOLD = 0.35

def verifier(state):
    context = state.get("context", "")
    claim = state.get("query", "")
    similarity = state.get("top_similarity", 0.0)
    claim_type = state.get("claim_type", "general")

    # 1️⃣ Similarity gate
    if similarity < SIMILARITY_THRESHOLD:
        return {
            **state,
            "verdict": "UNSUPPORTED",
            "confidence": round(similarity, 3),
            "done": True
        }

    # 2️⃣ Type-aware instruction
    type_instruction = ""

    if claim_type == "quantitative":
        type_instruction = """
- The claim includes numbers or percentages.
- Verify that the SAME numerical value and time reference appear in the context.
- If numbers do not match exactly, mark UNSUPPORTED.
"""

    elif claim_type == "forward-looking":
        type_instruction = """
- The claim is forward-looking.
- Distinguish between:
    * Achieved results (past tense)
    * Ongoing effort (working to, reducing)
    * Design intent (designed to, expected to)
- If the context only contains vague marketing language, mark MARKETING_LANGUAGE.
"""

    prompt = f"""
You are a strict ESG claim verification agent.

Evaluate whether the CLAIM is supported by the CONTEXT.

You are NOT allowed to use outside knowledge.

Return ONLY one of the following labels:

SUPPORTED
PARTIALLY_SUPPORTED
UNSUPPORTED
MARKETING_LANGUAGE

Definitions:

SUPPORTED:
Explicit factual or numerical confirmation.

PARTIALLY_SUPPORTED:
Related but incomplete confirmation.

UNSUPPORTED:
No direct evidence supports the claim.

MARKETING_LANGUAGE:
Vague, aspirational, or non-measurable.

{type_instruction}

CLAIM:
{claim}

CONTEXT:
{context}
"""

    verdict = llm.invoke(prompt).strip().upper()

    # 3️⃣ Confidence scaling
    confidence = 0.6 * similarity

    if verdict == "SUPPORTED":
        confidence += 0.4
    elif verdict == "PARTIALLY_SUPPORTED":
        confidence += 0.2

    print(f"Verifier verdict: {verdict} (similarity: {similarity}, confidence: {confidence})")

    return {
        **state,
        "verdict": verdict,
        "confidence": round(confidence, 3),
        "done": True
    }