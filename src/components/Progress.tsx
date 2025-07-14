import { cn } from "@/lib/utils";
import { CheckIcon, LoaderCircle } from "lucide-react";

export function Progress({
  logs,
  state,
}: {
  logs: {
    message: string;
    done: boolean;
  }[];
  state?: {
    research?: {
      sources_found: number;
    };
  };
}) {
  if (logs.length === 0) {
    return null;
  }

  // Helper function to truncate URLs
  const truncateUrl = (url: string) => {
    if (url.length <= 50) return url;
    return url.substring(0, 47) + "...";
  };

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

      {(state?.research?.sources_found ?? 0) > 0 && (
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
          Found {state?.research?.sources_found} source
          {state?.research?.sources_found !== 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}
