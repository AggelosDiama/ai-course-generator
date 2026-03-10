from langgraph.graph import StateGraph, END
from .state import CourseState  # Import from the new state.py
from .deconstructor import deconstructor_agent
from .librarian import librarian_agent
from .professor import professor_agent

def create_graph(llm):
    builder = StateGraph(CourseState)
    
    # Nodes
    builder.add_node("deconstructor", lambda state: deconstructor_agent(state, llm))
    builder.add_node("librarian", lambda state: librarian_agent(state, llm))
    builder.add_node("professor", lambda state: professor_agent(state, llm))
    
    # Edges
    builder.set_entry_point("deconstructor")
    builder.add_edge("deconstructor", "librarian")
    builder.add_edge("librarian", "professor")
    builder.add_edge("professor", END)
    
    return builder.compile()