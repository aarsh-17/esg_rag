from typing import TypedDict, List
from langchain_core.documents import Document
from langgraph.graph import StateGraph

from .agents.query_analyst import query_analyst
from .agents.researcher import researcher
from .agents.verifier import verifier
from .agents.critic import critic
from .agents.claim_classifier import claim_classifier




class AgentState(TypedDict):
    query: str
    context: str
    documents: List[Document]
    citations: list
    verdict: str
    grounded: bool
    done: bool
    top_similarity: float
    confidence: float
    claim_type: str


graph = StateGraph(AgentState)

graph.add_node("query_analyst", query_analyst)
graph.add_node("researcher", researcher)
graph.add_node("verifier", verifier)
graph.add_node("critic", critic)
graph.add_node("claim_classifier", claim_classifier)

graph.set_entry_point("query_analyst")

graph.add_edge("query_analyst", "claim_classifier")
graph.add_edge("claim_classifier", "researcher")
graph.add_edge("researcher", "verifier")
graph.add_edge("verifier", "critic")
graph.add_edge("critic", "__end__")

app = graph.compile()