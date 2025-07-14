
# Standard library imports
import os
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any, List

# Third-party imports
from dotenv import load_dotenv  # Environment variable management
load_dotenv()  # Load environment variables from .env file
from fastapi import FastAPI, Request  # Web framework
from fastapi.responses import StreamingResponse  # For streaming responses
from pydantic import BaseModel  # For data validation

# AG-UI protocol components for communication with frontend
from ag_ui.core import (
  RunAgentInput,   # Represents the input to an agent run
  Message,         # Represents a message in the conversation
  EventType,       # Enum of event types used in the protocol
  RunStartedEvent, # Event signaling the start of an agent run
  RunFinishedEvent,# Event signaling the end of an agent run
  TextMessageStartEvent,   # Event signaling the start of a text message
  TextMessageContentEvent, # Event carrying the content of a text message
  TextMessageEndEvent      # Event signaling the end of a text message
)
from ag_ui.encoder import EventEncoder  # Encodes events to Server-Sent Events format

# LangGraph and LangChain components for the research agent
from langgraph.graph import Graph
from langchain_core.messages import AIMessage, HumanMessage

# Local research agent components
from agui.langgraph.agent import research_graph, ResearchState

# INITIALIZATION: Create FastAPI application instance
# This app will handle HTTP requests and provide the research endpoint
app = FastAPI(title="AG-UI Endpoint")

@app.post("/")
async def langgraph_research_endpoint(input_data: RunAgentInput):
    """
    LangGraph-based research processing endpoint with integrated state management.
    This endpoint receives research requests and streams back real-time results.
    """
    async def event_generator():
        """
        Asynchronous generator that produces a stream of AG-UI protocol events.
        This function handles the entire research workflow and emits events.
        """
        # STEP 1: Initialize the event encoder for Server-Sent Events (SSE) format
        # This encoder converts our events into the proper SSE format for streaming
        encoder = EventEncoder()
        
        # STEP 2: Extract the research query from the incoming request
        # Get the content of the most recent message (user's query)
        query = input_data.messages[-1].content
        # Generate a unique identifier for this specific message/response
        message_id = str(uuid.uuid4())
        
        print(f"[DEBUG] LangGraph Research started with query: {query}")

        # STEP 3: Signal the start of the agent run to the frontend
        # This event tells the UI that processing has begun
        yield encoder.encode(
            RunStartedEvent(
                type=EventType.RUN_STARTED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id
            )
        )

        # STEP 4: Set up event collection and callback mechanism
        # Create a list to store events emitted by the research state
        emitted_events = []
        
        def event_emitter(encoded_event):
            """
            Callback function to collect events from the research state.
            This allows the research agent to emit events during processing.
            """
            emitted_events.append(encoded_event)
        
        # STEP 5: Initialize the research state with event handling capabilities
        # Create research state object that manages the workflow and emits events
        research_state = ResearchState(
            message_id=message_id,
            query=query,
            event_emitter=event_emitter
        )
        
        # STEP 6: Emit initial state snapshot to the frontend
        # This provides the UI with the initial state of the research process
        research_state.emit_snapshot()
        
        # STEP 7: Yield any events that were emitted during initialization
        # Send any setup events to the frontend before starting main processing
        for event in emitted_events:
            yield event
        emitted_events.clear()  # Clear the list for next batch of events
        
        # STEP 8: Build the LangGraph research workflow
        # Construct the graph that defines the research agent's behavior
        graph = research_graph(research_state)
        
        print(f"[DEBUG] Executing LangGraph workflow with state management")
        
        # STEP 9: Execute the main research workflow
        # Run the LangGraph with the user's query as a HumanMessage
        result = graph.invoke([HumanMessage(content=query)])
        
        # STEP 10: Stream any events emitted during processing
        # Send real-time updates that occurred during research execution
        for event in emitted_events:
            yield event
        emitted_events.clear()  # Clear events after streaming
        
        # STEP 11: Process and validate the research results
        # Log success and examine the structure of the returned data
        print(f"[DEBUG] LangGraph invoke API succeeded")
        print(f"[DEBUG] LangGraph result type: {type(result)}, content: {str(result)[:100]}...")
        
        # STEP 12: Extract the AI response message from the result
        # The result is expected to be a list with the AI-generated response
        print(f"[DEBUG] Result is a list with {len(result)} items")

        ai_message_item = result[0]  # Get the first item (should be the AI response)
        
        print(f"[DEBUG] First item type: {type(ai_message_item)}")
        
        # STEP 13: Extract the AI-generated response content
        # Get the text content from the AI message object (contextual response, not full report)
        ai_response_content = ai_message_item.content
        print(f"[DEBUG] AI response content extracted, length: {len(ai_response_content)}")
        
        # STEP 14: Begin streaming the AI response to the frontend
        # Signal the start of a new text message from the assistant
        yield encoder.encode(
            TextMessageStartEvent(
                type=EventType.TEXT_MESSAGE_START,
                message_id=message_id,
                role="assistant"  # Indicates this is the AI's response
            )
        )
        
        # STEP 15: Stream the AI-generated response content
        # Send the AI's contextual response (detailed report is sent via state updates)
        yield encoder.encode(
            TextMessageContentEvent(
                type=EventType.TEXT_MESSAGE_CONTENT,
                message_id=message_id,
                delta=ai_response_content  # The AI-generated contextual response
            )
        )
        
        # STEP 16: Signal the end of the text message
        # Indicate that the message streaming is complete
        yield encoder.encode(
            TextMessageEndEvent(
                type=EventType.TEXT_MESSAGE_END,
                message_id=message_id
            )
        )

        # STEP 17: Signal completion of the entire agent run
        # Tell the frontend that all processing is finished
        yield encoder.encode(
            RunFinishedEvent(
                type=EventType.RUN_FINISHED,
                thread_id=input_data.thread_id,
                run_id=input_data.run_id
            )
        )

    # STEP 18: Return the streaming response to the client
    # Create and return a Server-Sent Events (SSE) streaming response
    # This allows real-time communication with the frontend
    return StreamingResponse(
        event_generator(),  # Use our async generator as the content source
        media_type="text/event-stream"  # Set proper MIME type for SSE
    )

def main():
    """
    Entry point for running the FastAPI server.
    This function starts the development server with hot reload enabled.
    """
    # Import uvicorn (ASGI server) for running the FastAPI application
    import uvicorn
    
    # Start the server with the following configuration:
    # - Module path: "src.agui.main:app" (points to our FastAPI app)
    # - Host: "0.0.0.0" (accept connections from any IP address)
    # - Port: 8000 (standard development port)
    # - Reload: True (automatically restart server when code changes)
    uvicorn.run("agui.main:app", host="0.0.0.0", port=8000, reload=True)
 
# ENTRY POINT: Check if this script is being run directly
if __name__ == "__main__":
    # If run directly (not imported), start the development server
    main()