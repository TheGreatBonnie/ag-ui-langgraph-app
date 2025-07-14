# ========================================
# RESEARCH NODE FUNCTIONALITY
# ========================================

import openai
from typing import Optional, List
from langchain_core.messages import AIMessage

# Import our modular components
from .state import ResearchState
from .search import search_node
from .report import report_node

def research_node(messages, state: Optional[ResearchState] = None):
    """
    LangGraph node function that orchestrates the complete research workflow.
    
    Step 1: Extract the user query from the message chain
    Step 2: Set processing state to active
    Step 3: Perform web search with state tracking
    Step 4: Generate detailed report from search results
    Step 5: Generate AI response message based on research findings
    
    Args:
        messages: List of conversation messages (LangChain message objects)
        state: Optional ResearchState instance for progress tracking
        
    Returns:
        List containing AIMessage with the agent's final response
    """
    # Step 1: Extract the research query from the last message
    last = messages[-1]      # Get the most recent message
    query = last.content     # Extract the text content (user's query)
    
    # Step 2: Set processing state to indicate workflow is active
    if state:
        state.set_in_progress(True)
    
    # Step 3: Perform web search with integrated state management
    search_results = search_node(query, state)
    
    # Step 4: Generate comprehensive report from search results
    report = report_node(search_results, state)
    
    # Step 5: Generate AI response based on the research findings
    try:
        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful research assistant. Based on the research query and findings, 
                    generate a brief, conversational response (2-3 sentences) that:
                    1. Acknowledges completing the research
                    2. Highlights 1-2 key insights or findings
                    3. Indicates the detailed report is available
                    
                    Keep it natural and engaging, not templated."""
                },
                {
                    "role": "user", 
                    "content": f"Query: {query}\n\nReport summary: {report[:500]}..."
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        final_message = completion.choices[0].message.content
        
    except Exception as e:
        # Fallback to a simple message if AI generation fails
        print(f"[DEBUG] Error generating AI response: {e}")
        final_message = f"I've completed your research on '{query}'. You can find the detailed analysis in the report above."
    
    return [AIMessage(content=final_message)]