# ========================================
# STATE MANAGEMENT FOR RESEARCH WORKFLOW
# ========================================

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

# Import AG-UI protocol components for event encoding
from ag_ui.encoder import EventEncoder

# ========================================
# AG-UI PROTOCOL EVENT CLASSES
# ========================================

class StateDeltaEvent(BaseModel):
    """
    Custom AG-UI protocol event for partial state updates using JSON Patch.
    
    This event type allows for efficient state updates by sending only the
    changes (deltas) rather than the entire state object.
    """
    type: str = "STATE_DELTA"
    message_id: str
    delta: list  # List of JSON Patch operations (RFC 6902)

class StateSnapshotEvent(BaseModel):
    """
    Custom AG-UI protocol event for complete state replacement.
    
    This event type sends the entire state object, typically used for
    initial state setup or when a complete refresh is needed.
    """
    type: str = "STATE_SNAPSHOT"
    message_id: str
    snapshot: Dict[str, Any]  # Complete state object

# ========================================
# RESEARCH STATE MANAGEMENT CLASS
# ========================================

class ResearchState:
    """
    Manages the state of the research process and emits events for the UI.
    
    This class serves as the central state manager for the research workflow,
    tracking progress through different phases and emitting real-time updates
    to the frontend via AG-UI protocol events.
    """
    
    def __init__(self, message_id: str, query: str, event_emitter: Optional[callable] = None):
        """
        Initialize the research state manager.
        
        Step 1: Store essential identifiers and callback function
        Step 2: Set up the event encoder for AG-UI protocol
        Step 3: Initialize the comprehensive state structure
        """
        # Step 1: Store core properties
        self.message_id = message_id      # Unique identifier for this research session
        self.query = query                # The user's research query
        self.event_emitter = event_emitter # Callback function to emit events
        
        # Step 2: Initialize event encoder for AG-UI protocol compliance
        self.encoder = EventEncoder()
        
        # Step 3: Initialize comprehensive state structure
        # This state object tracks all aspects of the research process
        self.state = {
            # Overall status tracking
            "status": {
                "phase": "initialized",                    # Current major phase
                "timestamp": datetime.now().isoformat()   # When this state was created
            },
            
            # Research-specific data and progress
            "research": {
                "query": query,           # Original user query
                "stage": "not_started",   # Current research stage within the phase
                "sources_found": 0,       # Count of sources discovered
                "sources": [],            # Array of source objects with metadata
                "completed": False        # Whether research gathering is done
            },
            
            # Processing and report generation tracking
            "processing": {
                "progress": 0,            # Numerical progress from 0 to 1.0
                "report": None,           # Final generated report content
                "completed": False,       # Whether processing is completely done
                "inProgress": False       # Whether processing is currently active
            },
            
            # UI state management for frontend display
            "ui": {
                "showSources": False,     # Whether to display sources panel
                "showProgress": True,     # Whether to show progress indicators
                "activeTab": "chat"       # Which UI tab should be active
            }
        }
    
    def emit_snapshot(self):
        """
        Emit a complete state snapshot event.
        
        Step 1: Check if event emitter is available
        Step 2: Create StateSnapshotEvent with current state
        Step 3: Encode and emit the event
        """
        if self.event_emitter:
            # Step 1: Create snapshot event with complete state
            event = StateSnapshotEvent(
                message_id=self.message_id,
                snapshot=self.state
            )
            
            # Step 2: Encode event to AG-UI protocol format and emit
            self.event_emitter(self.encoder.encode(event))
    
    def emit_delta(self, operations: List[Dict[str, Any]]):
        """
        Emit a state delta event with JSON Patch operations.
        
        Step 1: Validate event emitter availability
        Step 2: Create StateDeltaEvent with patch operations
        Step 3: Encode and emit the delta event
        
        Args:
            operations: List of JSON Patch operations to apply to state
        """
        if self.event_emitter:
            # Step 1: Create delta event with JSON Patch operations
            event = StateDeltaEvent(
                message_id=self.message_id,
                delta=operations
            )
            
            # Step 2: Encode and emit the delta event
            self.event_emitter(self.encoder.encode(event))
    
    def update_phase(self, phase: str, stage: str, progress: float = None):
        """
        Update the current phase and stage of research with optional progress.
        
        Step 1: Build JSON Patch operations for phase/stage updates
        Step 2: Add progress update if provided
        Step 3: Apply changes to local state
        Step 4: Emit delta event with all changes
        
        Args:
            phase: The major phase (e.g., 'gathering_information', 'analyzing_information')
            stage: The specific stage within the phase (e.g., 'searching', 'organizing_data')
            progress: Optional progress value from 0.0 to 1.0
        """
        # Step 1: Create base JSON Patch operations
        operations = [
            {"op": "replace", "path": "/status/phase", "value": phase},
            {"op": "replace", "path": "/research/stage", "value": stage},
            {"op": "replace", "path": "/status/timestamp", "value": datetime.now().isoformat()}
        ]
        
        # Step 2: Add progress operation if specified
        if progress is not None:
            operations.append({"op": "replace", "path": "/processing/progress", "value": progress})
        
        # Step 3: Update local state to stay in sync
        self.state["status"]["phase"] = phase
        self.state["research"]["stage"] = stage
        self.state["status"]["timestamp"] = datetime.now().isoformat()
        if progress is not None:
            self.state["processing"]["progress"] = progress
        
        # Step 4: Emit the delta event
        self.emit_delta(operations)
    
    def set_in_progress(self, in_progress: bool):
        """
        Set whether processing is currently in progress.
        
        Step 1: Update local state
        Step 2: Create and emit delta event
        
        Args:
            in_progress: Boolean indicating if processing is active
        """
        # Step 1: Update local state
        self.state["processing"]["inProgress"] = in_progress
        
        # Step 2: Emit delta event with the change
        self.emit_delta([
            {"op": "replace", "path": "/processing/inProgress", "value": in_progress}
        ])
    
    def add_sources(self, sources: List[Dict[str, Any]]):
        """
        Add research sources to the state and update source count.
        
        Step 1: Append new sources to existing sources list
        Step 2: Update the source count
        Step 3: Emit delta event with updated sources and count
        
        Args:
            sources: List of source objects with title, url, snippet, etc.
        """
        # Step 1: Add sources to local state
        self.state["research"]["sources"].extend(sources)
        
        # Step 2: Update source count
        self.state["research"]["sources_found"] = len(self.state["research"]["sources"])
        
        # Step 3: Emit delta event with both sources and count updates
        self.emit_delta([
            {"op": "replace", "path": "/research/sources", "value": self.state["research"]["sources"]},
            {"op": "replace", "path": "/research/sources_found", "value": self.state["research"]["sources_found"]}
        ])
    
    def complete_research(self, report: str):
        """
        Mark research as complete and set the final report.
        
        Step 1: Build comprehensive completion operations
        Step 2: Update all relevant local state properties
        Step 3: Emit delta event with all completion updates
        
        Args:
            report: The final generated research report content
        """
        # Step 1: Create comprehensive completion operations
        operations = [
            {"op": "replace", "path": "/status/phase", "value": "completed"},
            {"op": "replace", "path": "/research/stage", "value": "report_complete"},
            {"op": "replace", "path": "/research/completed", "value": True},
            {"op": "replace", "path": "/processing/completed", "value": True},
            {"op": "replace", "path": "/processing/inProgress", "value": False},
            {"op": "replace", "path": "/processing/report", "value": report},
            {"op": "replace", "path": "/processing/progress", "value": 1.0}
        ]
        
        # Step 2: Update all local state properties
        self.state["status"]["phase"] = "completed"
        self.state["research"]["stage"] = "report_complete"
        self.state["research"]["completed"] = True
        self.state["processing"]["completed"] = True
        self.state["processing"]["inProgress"] = False
        self.state["processing"]["report"] = report
        self.state["processing"]["progress"] = 1.0
        
        # Step 3: Emit comprehensive completion delta
        self.emit_delta(operations)