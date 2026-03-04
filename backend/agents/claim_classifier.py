import re

FORWARD_WORDS = [
    "aim", "aims", "aiming",
    "target", "targets",
    "expect", "expects",
    "plan", "plans",
    "intend", "intends",
    "working to",
    "seek", "seeks",
    "designed to"
]

def claim_classifier(state):
    claim = state["query"].lower()

    if any(word in claim for word in FORWARD_WORDS):
        claim_type = "forward-looking"

    elif re.search(r"\d+%", claim):
        claim_type = "quantitative"

    else:
        claim_type = "general"

    return {
        **state,
        "claim_type": claim_type
    }