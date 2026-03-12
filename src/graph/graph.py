from langgraph.graph import StateGraph, END

from database.neo4j_ops import Neo4jManager
from .state import CourseState
from src.agents.discovery import discovery_agent
from src.agents.deconstructor import deconstructor_agent
from src.agents.librarian import librarian_agent
from src.agents.professor import professor_agent

# 2. Initialize it here
db = Neo4jManager()

def create_graph(llm):
    builder = StateGraph(CourseState)
    
    # Nodes
    builder.add_node("discovery", lambda state: discovery_agent(state, llm, db))
    builder.add_node("deconstructor", lambda state: deconstructor_agent(state, llm))
    builder.add_node("librarian", lambda state: librarian_agent(state, llm))
    builder.add_node("professor", lambda state: professor_agent(state, llm))
    
    # Edges
    builder.set_entry_point("discovery")
    builder.add_conditional_edges(
        "discovery",
        lambda state: "skip" if state.get("exists") else "generate",
        {
            "skip": END,
            "generate": "deconstructor"
        }
    )
    builder.add_edge("deconstructor", "librarian")
    builder.add_edge("librarian", "professor")
    builder.add_edge("professor", END)
    
    return builder.compile()