# ========================================
# LANGGRAPH WORKFLOW BUILDER AND AGENT COORDINATION
# ========================================

from typing import Optional
from langgraph.graph import Graph, END

# Import our modular components
from .state import ResearchState
from .research import research_node

def research_graph(state: Optional[ResearchState] = None):
    """
    Build and compile a research workflow graph using LangGraph.
    
    This function creates a simple but powerful research workflow that:
    Step 1: Create a new LangGraph workflow instance
    Step 2: Create a state-aware research node wrapper
    Step 3: Add the research node to the workflow
    Step 4: Configure workflow entry and exit points
    Step 5: Compile the workflow for execution
    
    Args:
        state: Optional ResearchState instance for progress tracking throughout workflow
    
    Returns:
        A compiled LangGraph that can be executed with input messages
    """
    # Step 1: Create a new LangGraph workflow instance
    workflow = Graph()
    
    # Step 2: Create a wrapper function that includes state management
    # This allows us to pass the state to the research node while maintaining
    # LangGraph's expected function signature (messages only)
    def research_node_with_state(messages):
        return research_node(messages, state)
    
    # Step 3: Add the research node to the workflow
    # The node will handle the complete research process:
    # - Web searching with progress tracking
    # - Report generation with state updates
    # - Error handling and logging
    workflow.add_node("research", research_node_with_state)
    
    # Step 4: Configure workflow entry and exit points
    workflow.set_entry_point("research")     # Start workflow at research node
    workflow.add_edge("research", END)       # End workflow after research completes
    
    # Step 5: Compile the workflow for execution
    # Compilation validates the graph structure and creates an executable workflow
    return workflow.compile()