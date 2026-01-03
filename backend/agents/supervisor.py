def supervisor(state):
    if state.get("done"):
        return "end"

    return "query_analyst"
