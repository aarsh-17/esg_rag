from typing import TypedDict, List
from langchain_core.documents import Document
from langgraph.graph import StateGraph

from .agents.query_analyst import query_analyst
from .agents.researcher import researcher
from .agents.reasoner import reasoner
from .agents.critic import critic
from .agents.supervisor import supervisor

class AgentState(TypedDict):
    query: str
    rewritten_query: str
    context: str
    answer: str
    documents: List[Document]
    doc_score: float
    grounded: bool
    done: bool
    citations: list

graph = StateGraph(AgentState)

graph.add_node("query_analyst", query_analyst)
graph.add_node("researcher", researcher)
graph.add_node("reasoner", reasoner)
graph.add_node("critic", critic)

graph.set_entry_point("query_analyst")

graph.add_edge("query_analyst", "researcher")
graph.add_edge("researcher", "reasoner")
graph.add_edge("reasoner", "critic")

graph.add_edge("critic", "__end__")

app = graph.compile()
