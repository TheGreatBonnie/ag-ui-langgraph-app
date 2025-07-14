# ========================================
# REPORT GENERATION FUNCTIONALITY
# ========================================

import openai
from typing import Optional, Dict, Any

# Import the ResearchState from our state module
from .state import ResearchState

def report_node(search_results, state: Optional[ResearchState] = None):
    """
    Generate a comprehensive research report from search results using OpenAI GPT.
    
    Step 1: Update state to show report generation phase
    Step 2: Handle error cases (string results instead of structured data)
    Step 3: Extract and format organic search results
    Step 4: Process knowledge graph information
    Step 5: Format related searches section
    Step 6: Process "People Also Ask" questions and answers
    Step 7: Combine all research data into unified text
    Step 8: Generate detailed report using OpenAI GPT model
    Step 9: Log and return the generated report
    
    Args:
        search_results: Structured search results from web_search function
        state: Optional ResearchState instance for progress tracking
        
    Returns:
        Generated research report as a string
    """
    # Step 1: Update state to indicate report generation has begun
    if state:
        state.update_phase("generating_report", "creating_detailed_report", 0.8)
    
    # Step 2: Handle error case where search_results is an error message string
    if isinstance(search_results, str):
        return search_results  # Return error message directly
    
    # Step 3: Extract and format organic search results
    organic_results = search_results.get("organic", [])
    
    # Step 4: Process knowledge graph information if available
    knowledge_graph = search_results.get("knowledgeGraph")
    knowledge_graph_text = ""
    if knowledge_graph:
        # Extract meaningful information from knowledge graph
        kg_items = []
        for key, value in knowledge_graph.items():
            # Skip metadata fields, focus on descriptive content
            if key not in ["type", "title", "imageUrl"]:
                if isinstance(value, list):
                    kg_items.append(f"{key}: {', '.join(value)}")
                else:
                    kg_items.append(f"{key}: {value}")
        
        # Format knowledge graph section if we have content
        if kg_items:
            knowledge_graph_text = f"Knowledge Graph about {knowledge_graph.get('title', 'the topic')}:\n" + "\n".join(kg_items)
    
    # Step 5: Format related searches section
    related_searches = search_results.get("relatedSearches", [])
    related_searches_text = ""
    if related_searches:
        related_searches_text = "Related Searches:\n" + "\n".join([f"- {rs}" for rs in related_searches])
    
    # Step 6: Process "People Also Ask" questions and answers
    people_also_ask = search_results.get("peopleAlsoAsk", [])
    paa_text = ""
    if people_also_ask:
        paa_items = []
        for q in people_also_ask:
            question = q.get("question", "")
            answer = q.get("snippet", "No answer available")
            if question:
                paa_items.append(f"Q: {question}\nA: {answer}")
        
        # Format PAA section if we have content
        if paa_items:
            paa_text = "People Also Ask:\n" + "\n\n".join(paa_items)
    
    # Step 7: Format the main organic search results
    organic_text = "\n\n".join([
        f"Title: {r.get('title', 'No title')}\nSnippet: {r.get('snippet', 'No preview')}\nLink: {r.get('link', r.get('url', 'No link'))}"
        for r in organic_results
    ])
    
    # Step 8: Combine all formatted research data into a single text block
    all_research = "\n\n===\n\n".join(filter(None, [
        organic_text,           # Main search results
        knowledge_graph_text,   # Knowledge panel information
        related_searches_text,  # Related search suggestions
        paa_text               # People Also Ask Q&A
    ]))
    
    # Log the research data being processed (truncated for readability)
    print(f"[DEBUG] Creating detailed report from search results: {all_research[:500]}...")
    
    # Step 9: Generate comprehensive report using OpenAI GPT
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",  # Use model with larger context for detailed reports
        messages=[
            {
                "role": "system", 
                "content": """Create a comprehensive research report on the topic using the provided search results. 
                Your report should be well-structured with the following sections:

                1. EXECUTIVE SUMMARY: A brief overview of the topic and key findings (2-3 sentences)
                
                2. INTRODUCTION: Background information on the topic and why it matters
                
                3. KEY FINDINGS: The main insights organized as bullet points
                
                4. DETAILED ANALYSIS: In-depth exploration of the topic with subsections as needed
                   - Include answers to common questions when available
                   - Address related topics identified in the research
                
                5. CONCLUSIONS: Summary of the most important takeaways
                
                6. FURTHER RESEARCH: Suggest related topics worth exploring 
                
                7. SOURCES: List all sources from the search results with their URLs
                
                Format the report with clear section headings and organized content. Include relevant facts, statistics, 
                and quotes from the sources when available. Maintain a professional, objective tone throughout.
                Use markdown formatting for better readability, with # for main headings and ## for subheadings.
                """
            },
            {"role": "user", "content": all_research}  # Provide all research data as user input
        ],
        temperature=0.5,  # Lower temperature for more factual, structured output
        max_tokens=4000   # Allow for longer response to accommodate detailed report
    )
    
    # Extract the generated report from the API response
    report = completion.choices[0].message.content
    print(f"[DEBUG] Detailed research report generated (excerpt): {report[:300]}...")
    
    # Step 10: Update state to mark research as complete with final report
    if state:
        state.complete_research(report)
    
    # Return the completed research report
    return report