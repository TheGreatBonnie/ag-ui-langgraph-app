# ========================================
# WEB SEARCH FUNCTIONALITY
# ========================================

import os
import requests
from typing import Optional, Dict, Any

# Import the ResearchState from our state module
from .state import ResearchState

def search_node(query: str, state: Optional[ResearchState] = None):
    """
    Perform web search using Serper API and track progress via state management.
    
    Step 1: Log search initiation and update state
    Step 2: Set up API credentials and request parameters
    Step 3: Make API call to Serper search service
    Step 4: Parse and structure the search results
    Step 5: Handle error cases (no results found)
    Step 6: Process and format successful results
    Step 7: Update state with discovered sources
    Step 8: Return structured search results
    
    Args:
        query: The search query string
        state: Optional ResearchState instance for progress tracking
        
    Returns:
        Structured search results or error message string
    """
    # Step 1: Log search initiation and update progress state
    print(f"[DEBUG] Searching for: {query}")
    
    if state:
        # Update state to show we're in the searching phase
        state.update_phase("gathering_information", "searching", 0.2)
    
    # Step 2: Set up API credentials and request configuration
    api_key = os.environ["SERPER_API_KEY"]              # Get API key from environment
    url = "https://google.serper.dev/search"            # Serper API endpoint
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = {"q": query}                              # Search query payload
    
    # Step 3: Make the API call to Serper search service
    response = requests.post(url, headers=headers, json=payload)
    results = response.json()
    
    # Step 4: Extract different types of search results from response
    organic_results = results.get("organic", [])           # Main search results
    knowledge_graph = results.get("knowledgeGraph", {})   # Knowledge panel data
    related_searches = results.get("relatedSearches", []) # Related query suggestions
    people_also_ask = results.get("peopleAlsoAsk", [])    # FAQ-style results
    
    # Step 5: Handle case where no search results were found
    if not organic_results:
        print(f"[DEBUG] Full Serper response: {results}")
        print("[DEBUG] No search results found.")
        return "No relevant research results were found on the topic."
    
    # Step 6: Log successful results and prepare structured data
    print(f"[DEBUG] Serper results: {len(organic_results)} organic results found")
    
    # Compile all results into a structured format for further processing
    compiled_results = {
        "organic": organic_results[:5],  # Limit to top 5 organic results
        "knowledgeGraph": knowledge_graph if knowledge_graph else None,
        "relatedSearches": related_searches[:3] if related_searches else None,
        "peopleAlsoAsk": people_also_ask[:3] if people_also_ask else None
    }
    
    # Step 7: Update state with discovered sources if state management is active
    if state and organic_results:
        # Transform search results into source objects for state tracking
        sources = [
            {
                "title": result.get("title", "No title"),
                "url": result.get("link", result.get("url", "")),
                "snippet": result.get("snippet", "No preview")
            }
            for result in organic_results[:5]  # Process top 5 results
        ]
        
        # Add sources to state and update phase to data organization
        state.add_sources(sources)
        state.update_phase("analyzing_information", "organizing_data", 0.5)
    
    # Step 8: Return the compiled search results
    return compiled_results