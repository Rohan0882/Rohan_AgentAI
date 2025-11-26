# Implementation Plan: V2 for Kotler Case Analyst

**Objective:** To define the workflow for the user-facing Orchestrator Agent. This agent's primary role is to receive a high-level user request (e.g., "Analyze the Nokia case using 5Cs") and decompose it into a sequence of calls to the `Kotler_MCP_Server`.

---

## Agent Workflow Breakdown

**User Request:** *"Analyze the [Case Name] using [Framework]."*

### Step 1: Deconstruct the Request
-   **Action:** The Orchestrator Agent parses the user's prompt to identify the core components:
    -   `Case_Name`: The subject of the analysis (e.g., "Nokia").
    -   `Framework_Requested`: The specific marketing model to apply (e.g., "5Cs", "SWOT", "4Ps").
-   **Artifact:** Log the deconstructed request parameters.
    -   `log_artifact("deconstructed_request", {"case": "Nokia", "framework": "5Cs"})`

### Step 2: Gather Contextual Data (RAG)
-   **Action:** The agent makes a call to the `/rag_query` endpoint on the `Kotler_MCP_Server` to retrieve foundational knowledge about the requested framework.
-   **Code Example:**
    ```python
    # Agent-generated script
    import requests

    framework_info = requests.post(
        "http://127.0.0.1:5000/rag_query",
        json={"question": "What is the 5Cs analysis?"}
    ).json()

    log_artifact("framework_definition", framework_info)
    ```
-   **Rationale:** This step ensures the agent has a clear, text-based understanding of the task before proceeding.

### Step 3: Execute Core Analysis
-   **Action:** Based on the `Framework_Requested`, the agent calls the appropriate endpoint on the server.
-   **Control Flow:**
    -   **If `Framework_Requested` is "SWOT":**
        -   Call `/swot_analyzer` with the case study text.
    -   **If `Framework_Requested` is "Market Segmentation":**
        -   Call `/market_segmenter` with demographic data from the case.
    -   **If `Framework_Requested` is "4Ps":**
        -   Call `/fourps_mix` with the strategic goals outlined in the case.
-   **Code Example (for SWOT):**
    ```python
    # Agent-generated script
    case_data = {"text": "Nokia had a strong brand but failed to adapt..."}

    swot_results = requests.post(
        "http://127.0.0.1:5000/swot_analyzer",
        json={"case_data": case_data}
    ).json()

    log_artifact("raw_swot_analysis", swot_results)
    ```

### Step 4: Synthesize and Present Findings
-   **Action:** The agent receives the raw JSON output from the MCP server. It then synthesizes this data into a human-readable summary.
-   **Token Efficiency:** The agent processes the (potentially large) raw data and generates a concise summary. This summary, not the raw data, is what is used in the final response to the user, ensuring efficient use of the LLM's context window.
-   **Artifact:**
    -   `log_artifact("final_summary", "Nokia's primary strength was its brand... Its key weakness was a slow response to the smartphone trend...")`

### Step 5: Final Output
-   **Action:** The agent presents the final, synthesized summary to the user.

---

This structured workflow ensures that the agent's process is transparent, verifiable through artifacts, and efficient in its use of both the specialized tools and the core LLM's capabilities.
