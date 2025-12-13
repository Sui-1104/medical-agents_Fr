"""ADK agent entrypoint for the Dev UI.

Why this file exists:
- ADK Dev UI lists *directories* under `agents_dir` as candidate apps.
- Our repo has other top-level directories (`docs/`, `tests/`, etc), so pointing
  ADK at the repo root forces manual selection.
- We keep the real agent definition in `jarvis/agent.py` and re-export it here,
  so the agent remains a normal importable Python package.
"""

from __future__ import annotations

from jarvis.agent import root_agent


