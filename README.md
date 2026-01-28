# Medical Workflow Agents

A specialized AI system designed to automate critical clinical workflows including SOAP note generation, ICD-10 coding, and medical image analysis. Built on the **Google Agent Development Kit (ADK)**, this project provides a production-ready foundation for deploying medical AI agents on self-hosted infrastructure.

## capabilities

This system utilizes a **multi-agent architecture** orchestrated by a central router:

### 🧠 Medical Router (Root Agent)
The intelligent entry point for the system. It analyzes the user's input—whether it's a raw conversation transcript, a structured clinical note, or a medical image—and automatically routes it to the most appropriate specialist agent.

### 📝 SOAP Generator
Specialized in clinical documentation.
- **Input**: Raw transcripts of patient-clinician dialogues.
- **Output**: Structured **SOAP notes** (Subjective, Objective, Assessment, Plan).
- **Features**: Distinguishes between patient reports and clinician observations, ensuring accurate professional documentation.

### 🏷️ ICD-10 Coder
Specialized in medical coding.
- **Input**: Clinical notes or summaries.
- **Output**: JSON-formatted list of applicable **ICD-10 codes** with descriptions.
- **Features**: Adheres to coding guidelines, focusing on specific disease/symptom codes and avoiding generic administrative codes when possible.

### 🩻 Image Analyzer
Specialized in radiology and medical imaging.
- **Input**: Medical images (X-ray, MRI, CT, etc.).
- **Output**: Structured radiology reports including technique, findings, impression, and recommendations.
- **Features**: Can answer specific user questions about the provided image.

## Use Cases

### 1. Automated Scribing & Documentation
**Scenario**: A primary care physician records a consultation with a patient.
**Workflow**: The audio transcript is sent to the agent. The **Router** identifies it as a conversation and delegates to the **SOAP Generator**, which produces a formatted note ready for the EHR.

### 2. Revenue Cycle Management (RCM)
**Scenario**: A billing specialist needs to process a batch of clinical notes for claims.
**Workflow**: Notes are fed into the system. The **Router** detects clinical text and delegates to the **ICD-10 Coder**, which extracts valid billing codes, reducing manual review time.

### 3. Radiology Triage & Reporting
**Scenario**: A clinic receives an incoming X-ray.
**Workflow**: The image is uploaded. The **Router** sends it to the **Image Analyzer**, which generates a preliminary report listing findings and impressions, acting as a second pair of eyes for the radiologist.

---

## Quickstart

### Prerequisites
- Python **3.13+**
- [`uv`](https://github.com/astral-sh/uv)
- A Postgres connection string
- An LLM API Key (OpenRouter or Google)

### 1) Configure Environment

Copy `.env.example` to `.env`:

- **`AGENT_NAME`**: Unique ID for your agent (default: `medical_agents`).
- **`DATABASE_URL`**: Postgres connection string.
- **`OPENROUTER_API_KEY`**: Recommended for accessing varied models.
- **`GOOGLE_API_KEY`**: Optional. Required only if using Gemini models directly.

### 2) Install Dependencies

```bash
uv sync
```

### 3) Run Locally

```bash
uv run python -m agent.server
```
Visit `http://127.0.0.1:8080` to interact with the agent via the ADK web interface.

## Deployment

We've simplified deployment to the absolute basics. No Kubernetes required.

**Note:** The automated CD workflow (`deploy` job) in `.github/workflows/docker-publish.yml` is currently commented out. You must uncomment it, update the server path, and add your SSH secrets (`SERVER_HOST`, `SERVER_USER`, `SSH_PRIVATE_KEY`) to GitHub before auto-deployment will work.

### Option 1: Using the Pre-built Image (Recommended)

```bash
# 1. Pull the latest image
docker pull ghcr.io/queryplanner/medical-agents:main

# 2. Start the service
docker compose up -d
```

### Option 2: Build Yourself

```bash
git pull
docker compose up --build -d
```

👉 **[Read the Full Deployment Guide](docs/DEPLOYMENT.md)**

## Observability

The template comes pre-wired with **OpenTelemetry**. By default, it's set up to export traces to **Langfuse** for beautiful, actionable insights into your agent's performance and costs.

To change the backend, simply update the OTel exporter configuration in your `.env`.

## Documentation

- [Development Guide](docs/development.md)
- [Architecture](docs/architecture.md)
- [Observability Setup](docs/base-infra/observability.md)