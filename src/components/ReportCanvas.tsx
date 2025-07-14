import { ResearchAgentState } from "@/lib/research-agent-types";
import { LoaderCircle } from "lucide-react";
import ReactMarkdown from "react-markdown";

export function ReportCanvas({
  state,
  running,
}: {
  state: ResearchAgentState | null;
  running: boolean;
}) {
  return (
    <div className="min-h-screen flex justify-center items-start flex-col transition-colors duration-300 p-8 bg-gray-50 overflow-y-auto">
      <div className="max-w-4xl w-full mx-auto">
        <div className="text-center mb-8 pt-4">
          <h1 className="text-4xl font-bold mb-2 text-gray-900">
            Research Report
          </h1>
          <p className="text-lg text-gray-600">
            AI-powered research and analysis
          </p>
        </div>

        {/* Research Question Card */}
        {state?.research?.query && (
          <div className="mb-6 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <svg
                  className="w-4 h-4 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  Research Question
                </h3>
                <p className="text-gray-700 leading-relaxed">
                  {state.research?.query}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Status Card */}
        {running && !state?.processing?.report && (
          <div className="mb-6 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border border-blue-200">
            <div className="flex items-center gap-3">
              <div className="flex-shrink-0">
                <LoaderCircle className="w-6 h-6 text-blue-600 animate-spin" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-blue-900">
                  Research in Progress
                </h3>
                <p className="text-blue-700">Research in progress...</p>
              </div>
            </div>
          </div>
        )}

        {/* Report Card */}
        {state?.processing?.report ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6">
            <div className="p-6">
              <div className="prose prose-gray max-w-none">
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-2xl font-bold text-gray-900 mt-6 mb-4 first:mt-0">
                        {children}
                      </h1>
                    ),
                    h2: ({ children }) => (
                      <h2 className="text-xl font-semibold text-gray-900 mt-5 mb-3">
                        {children}
                      </h2>
                    ),
                    h3: ({ children }) => (
                      <h3 className="text-lg font-medium text-gray-900 mt-4 mb-2">
                        {children}
                      </h3>
                    ),
                    p: ({ children }) => (
                      <p className="text-gray-700 mb-4 leading-relaxed">
                        {children}
                      </p>
                    ),
                    ul: ({ children }) => (
                      <ul className="space-y-2 mb-4">{children}</ul>
                    ),
                    ol: ({ children }) => (
                      <ol className="space-y-2 mb-4">{children}</ol>
                    ),
                    li: ({ children }) => (
                      <div className="flex items-start gap-2">
                        <div className="flex-shrink-0 w-1.5 h-1.5 bg-gray-400 rounded-full mt-2"></div>
                        <div className="text-gray-700">{children}</div>
                      </div>
                    ),
                  }}>
                  {state?.processing?.report}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center bg-white rounded-xl shadow-sm border border-gray-200 p-12">
            <div className="max-w-md mx-auto">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {running ? "Generating Report" : "Ready to Research"}
              </h3>
              <p className="text-gray-600 mb-4">
                {running
                  ? "Your research report will appear here once the analysis is complete."
                  : "Ask me to research any topic and I'll generate a comprehensive, well-structured report for you."}
              </p>
              {(state?.research?.sources?.length ?? 0) > 0 && (
                <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-full text-sm">
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  {state?.research?.sources?.length} source
                  {state?.research?.sources?.length !== 1 ? "s" : ""} found
                </div>
              )}
            </div>
          </div>
        )}

        {/* Sources Card */}
        {state?.research?.sources && state.research?.sources?.length > 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg
                    className="w-4 h-4 text-gray-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                    />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    Research Sources
                  </h3>
                  <p className="text-sm text-gray-600">
                    {state.research?.sources?.length} source
                    {state.research?.sources?.length !== 1 ? "s" : ""} used in
                    this research
                  </p>
                </div>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {state.research?.sources?.map((resource, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-medium text-sm">
                      {index + 1}
                    </div>
                    <div className="flex-1 min-w-0">
                      <a
                        href={resource.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 font-medium text-sm block hover:underline">
                        {resource.title}
                      </a>
                      {resource.snippet && (
                        <p className="text-gray-600 text-sm mt-1 leading-relaxed">
                          {resource.snippet}
                        </p>
                      )}
                      <p className="text-gray-400 text-xs mt-1 truncate">
                        {resource.url}
                      </p>
                    </div>
                    <div className="flex-shrink-0">
                      <svg
                        className="w-4 h-4 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                        />
                      </svg>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
