"use client";

import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { ResearchAgentState } from "@/lib/research-agent-types";
import { Progress } from "@/components/Progress";
import { ReportCanvas } from "@/components/ReportCanvas";
import { useRef } from "react";
// import { cn } from "@/lib/utils";

export default function CopilotKitPage() {
  // Reference to track if research is in progress
  const isResearchInProgress = useRef(false);

  // Connect to the agent's state using CopilotKit's useCoAgent hook
  const {
    state,
    running,
    stop: stopResearchAgent,
  } = useCoAgent<ResearchAgentState>({
    name: "researchAgent",
    initialState: {
      status: { phase: "idle", error: null },
      research: {
        query: "",
        stage: "not_started",
        sources_found: 0,
        sources: [],
        completed: false,
      },
      processing: {
        progress: 0,
        report: null,
        completed: false,
        inProgress: false,
      },
      ui: { showSources: false, showProgress: false, activeTab: "chat" },
    },
  });

  // Helper function to get step details from state
  const getStepDetails = (phase: string, stage: string) => {
    const phaseMap = {
      idle: "Getting ready...",
      initialized: "Setting up research parameters",
      gathering_information:
        stage === "searching"
          ? "Searching the web for information"
          : "Gathering and collecting data",
      analyzing_information:
        stage === "organizing_data"
          ? "Organizing research data"
          : "Processing and analyzing information",
      generating_report: (() => {
        switch (stage) {
          case "creating_detailed_report":
          case "outlining_report":
            return "Creating report outline";
          case "drafting_executive_summary":
            return "Writing executive summary";
          case "writing_introduction":
            return "Drafting introduction";
          case "compiling_key_findings":
            return "Compiling key findings";
          case "developing_analysis":
            return "Developing detailed analysis";
          case "forming_conclusions":
            return "Forming conclusions";
          case "finalizing_report":
            return "Finalizing comprehensive report";
          default:
            return "Generating detailed report";
        }
      })(),
      completed:
        stage === "report_complete"
          ? "Research report completed"
          : "Research completed",
    };

    return phaseMap[phase as keyof typeof phaseMap] || "Processing...";
  };

  // Implement useCoAgentStateRender hook
  useCoAgentStateRender({
    name: "researchAgent",
    handler: ({ nodeName }) => {
      // Stop the research agent when the "__end__" node is reached
      if (nodeName === "__end__") {
        setTimeout(() => {
          isResearchInProgress.current = false; // Ensure flag is reset
          stopResearchAgent();
        }, 1000);
      }
    },
    render: ({ state }) => {
      // if (status === "inProgress" || status === "complete") {
      isResearchInProgress.current = true;

      // Get steps from state phases
      const getStepsFromState = () => {
        const currentPhase = state?.status?.phase || "idle";
        const currentStage = state?.research?.stage || "not_started";

        const allPhases = [
          "initialized",
          "gathering_information",
          "analyzing_information",
          "generating_report",
          "completed",
        ];

        return allPhases.map((phase) => ({
          id: phase,
          label: phase
            .split("_")
            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" "),
          description: getStepDetails(phase, currentStage),
          completed: allPhases.indexOf(currentPhase) > allPhases.indexOf(phase),
          current: currentPhase === phase,
        }));
      };

      const steps = getStepsFromState();
      const currentStepIndex = steps.findIndex((step) => step.current);

      // Create logs array from state-derived steps
      const logs = steps.map((step, index) => ({
        done: step.completed || index < currentStepIndex,
        message: `${step.label}: ${step.description}`,
      }));

      return <Progress logs={logs || []} state={state} />;
      // }

      // if (status === "complete") {
      //   isResearchInProgress.current = false;
      //   return null;
      // }

      // return null;
    },
  });

  return (
    <main className="flex">
      <div className="flex-1">
        {" "}
        {/* Add right margin to account for sidebar */}
        <ReportCanvas state={state} running={running} />
      </div>
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={false}
        labels={{
          title: "Research Assistant",
          initial:
            "Hello! I'm your Research assistant. Ask me anything and I'll research it for you.",
        }}
      />
    </main>
  );
}
