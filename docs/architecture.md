# Medical Agents Architecture

## Overview

This project implements a **Hierarchical Agent Architecture** using the Google Agent Development Kit (ADK). The system is designed to handle diverse medical tasks by routing user inputs to specialized agents, ensuring high accuracy and context-specific processing.

## Agent Design

### The Router Pattern
At the core of the system is the **MedicalRouter** (Root Agent). Unlike a general-purpose chatbot, this agent does not attempt to solve every problem itself. Instead, its primary instruction is to classify the user's intent and input type, then delegate execution to a domain expert.

### Specialized Sub-Agents
We strictly separate concerns into distinct agents, each with its own system prompt and configuration:

1.  **SOAPGeneratorAgent**:
    - **Goal**: Documentation.
    - **Prompt Strategy**: Focuses on extracting Subjective, Objective, Assessment, and Plan sections from conversational text.
    - **Location**: `src/agent/sub_agents/soap.py`

2.  **ICD10Agent**:
    - **Goal**: Coding & Billing.
    - **Prompt Strategy**: Few-shot prompting with strict JSON output constraints for ICD-10 standard codes.
    - **Location**: `src/agent/sub_agents/icd10.py`

3.  **ImageAnalyzerAgent**:
    - **Goal**: Diagnostics support.
    - **Prompt Strategy**: Multimodal input handling (Text + Image) to generate radiology reports.
    - **Location**: `src/agent/sub_agents/image_analysis.py`

## Request Flow

1.  **Ingestion**: A request hits the `FastAPI` server (`src/agent/server.py`).
2.  **Session Retrieval**: The server retrieves or creates a session state from **PostgreSQL**.
3.  **Routing**: The `MedicalRouter` (`src/agent/agent.py`) receives the input.
    - If it's an image, it routes to `ImageAnalyzerAgent`.
    - If it's a transcript, it routes to `SOAPGeneratorAgent`.
    - If it's a clinical note, it routes to `ICD10Agent`.
4.  **Execution**: The selected sub-agent processes the input using the configured LLM (e.g., Gemini 1.5 Flash, GPT-4).
5.  **Response**: The sub-agent returns the structured output (JSON or formatted text) back to the Router, which delivers it to the user.

## Technical Stack

### Key choices

- **Framework**: Google ADK (Agent Development Kit) for agent orchestration and state management.
- **Server**: `FastAPI` wrapping the ADK application.
- **Runtime**: Python 3.13+ managed by `uv`.
- **Persistence**: **PostgreSQL** via `asyncpg`. We use standard Postgres instead of proprietary memory stores to ensure data ownership and easy migration.
- **Observability**: **OpenTelemetry** (OTel) instrumentation for tracing agent decisions and LLM costs (Langfuse compatible).

### What ADK uses the database for

ADK session persistence stores:

- **Session Rows**: IDs, user mapping, and current state.
- **Events**: Full conversation history, tool calls, and agent thoughts.
- **App/User State**: Snapshots of the agent's memory at each turn.

This architecture ensures that conversations are durable and can be resumed across server restarts.