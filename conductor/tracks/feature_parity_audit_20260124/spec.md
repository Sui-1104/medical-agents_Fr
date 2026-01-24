# Specification: Feature Parity Audit & Documentation Update

## Context
The current project is a fork/template derived from `doughayden/agent-foundation` but adapted for self-hosted (bare-metal/Docker) deployment instead of Google Cloud Platform (GCP). We need to ensure that all core agent capabilities from the original repo are present and functional in this version, while verifying that all documentation accurately reflects the self-hosted deployment model.

## Goals
1.  **Verify Feature Parity:** Confirm that the local codebase supports all agentic features (tools, memory, sub-agents) found in the upstream `agent-foundation` repo, excluding GCP-specific infrastructure (e.g., Cloud Run, Cloud SQL, Secret Manager).
2.  **Identify Gaps:** List any missing features or unnecessary GCP artifacts remaining in the codebase.
3.  **Update Documentation:** Ensure `/docs` and `README.md` provide accurate, complete instructions for the self-hosted setup, removing or clarifying GCP-specific references.

## Non-Goals
-   We are NOT re-implementing GCP deployment features.
-   We are NOT changing the core architecture unless required for parity.

## Requirements

### Feature Audit
-   **Comparison Source:** `git@github.com-personal:doughayden/agent-foundation.git`
-   **Scope:** `src/agent_foundation`, `src/tools`, `src/utils` (or equivalents).
-   **Exclusions:** `terraform/`, `k8s/`, `app.yaml`, or other GCP-only config files.

### Documentation Update
-   **Target:** `/docs` directory and `README.md`.
-   **Verification:** All guides must work for a user with `docker`, `python 3.13`, and a standard Postgres connection string.
-   **Removal:** Remove references to `gcloud deploy`, `Cloud Run`, etc., unless marked as optional/historical context.

## Success Criteria
-   A generated audit report listing feature parity status.
-   All discrepancies (missing features) are either resolved (ported) or documented as "wont-fix" (GCP only).
-   Documentation is updated and verified against the local setup.
