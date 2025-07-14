"use client";

import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { ResearchAgentState } from "@/lib/research-agent-types";
import { Check as CheckIcon, LoaderCircle } from "lucide-react";
import { ReportCanvas } from "@/components/ReportCanvas";
import { useRef } from "react";
import { cn } from "@/lib/utils";

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
    render: ({ status }) => {
      if (status === "inProgress" || status === "complete") {
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
            completed:
              allPhases.indexOf(currentPhase) > allPhases.indexOf(phase),
            current: currentPhase === phase,
          }));
        };

        const steps = getStepsFromState();
        const currentStepIndex = steps.findIndex((step) => step.current);

        // Helper function to truncate URLs
        const truncateUrl = (url: string) => {
          if (url.length <= 50) return url;
          return url.substring(0, 47) + "...";
        };

        // Create logs array from state-derived steps
        const logs = steps.map((step, index) => ({
          done: step.completed || index < currentStepIndex,
          message: `${step.label}: ${step.description}`,
        }));

        return (
          <div className="research-in-progress bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            {/* Progress Steps */}
            <div data-test-id="progress-steps">
              <div className="border border-slate-200 bg-slate-100/30 shadow-md rounded-lg overflow-hidden text-sm py-2">
                {logs.map((log, index) => (
                  <div
                    key={index}
                    data-test-id="progress-step-item"
                    className={`flex ${
                      log.done || index === logs.findIndex((log) => !log.done)
                        ? ""
                        : "opacity-50"
                    }`}>
                    <div className="w-8">
                      <div
                        className="w-4 h-4 bg-slate-700 flex items-center justify-center rounded-full mt-[10px] ml-[12px]"
                        data-test-id={
                          log.done
                            ? "progress-step-item_done"
                            : "progress-step-item_loading"
                        }>
                        {log.done ? (
                          <CheckIcon className="w-3 h-3 text-white" />
                        ) : (
                          <LoaderCircle className="w-3 h-3 text-white animate-spin" />
                        )}
                      </div>
                      {index < logs.length - 1 && (
                        <div
                          className={cn(
                            "h-full w-[1px] bg-slate-200 ml-[20px]"
                          )}></div>
                      )}
                    </div>
                    <div className="flex-1 flex justify-center py-2 pl-2 pr-4">
                      <div className="flex-1 flex items-center text-xs text-gray-700">
                        {log.message.replace(
                          /https?:\/\/[^\s]+/g, // Regex to match URLs
                          (url) => truncateUrl(url) // Replace with truncated URL
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {state?.research?.sources_found > 0 && (
              <div className="text-xs text-gray-500 flex items-center gap-1.5">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="12"
                  height="12"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M13 12H3"></path>
                </svg>
                Found {state.research.sources_found} source
                {state.research.sources_found !== 1 ? "s" : ""}
              </div>
            )}
          </div>
        );
      }

      if (status === "complete") {
        isResearchInProgress.current = false;
        return null;
      }

      return null;
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
