"""FastAPI server entrypoint for local ADK Web that uses Postgres sessions by default.

Why this exists:
- `adk web` defaults to local SQLite (`<agent>/.adk/session.db`) unless you pass
  `--session_service_uri`.
- This module provides a stable, memorable entrypoint that wires the session
  service URI from environment variables.

Run:
  - `python -m jarvis.server`
"""

from __future__ import annotations

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app


def _import_local_utilities():
  """Import local helpers in a way that works in two execution modes.

  Supported:
  - `python -m jarvis.server` (preferred; package context is available)
  - `cd jarvis && python -m server` (no package context; relative imports fail)
  """

  try:
    from .utils.db_url import to_asyncpg_sqlalchemy_url  # type: ignore
    from .utils.env import load_standard_env_files  # type: ignore
    from .utils.env import require_env  # type: ignore
  except ImportError:
    # When `server.py` is executed as a top-level module, `__package__` is None
    # and relative imports won't work. In that case, fall back to local imports
    # from the current working directory (the `jarvis/` folder).
    from utils.db_url import to_asyncpg_sqlalchemy_url  # type: ignore
    from utils.env import load_standard_env_files  # type: ignore
    from utils.env import require_env  # type: ignore

  return to_asyncpg_sqlalchemy_url, load_standard_env_files, require_env


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


def _agents_dir() -> str:
  """Directory that ADK scans for agent folders.

  Important: ADK's current implementation lists *all directories* under
  `agents_dir` (it doesn't filter by `agent.py`). If we point it at repo root,
  the Dev UI will show `docs/`, `tests/`, etc and force manual selection.
  """

  repo_root = Path(__file__).resolve().parent.parent
  default_agents_dir = repo_root / "agents"
  return os.getenv("AGENTS_DIR", str(default_agents_dir))


def create_app() -> FastAPI:
  to_asyncpg_sqlalchemy_url, load_standard_env_files, require_env = (
      _import_local_utilities()
  )

  # Keep behavior close to `adk web` (which loads agent .env).
  repo_root = Path(__file__).resolve().parent.parent
  agent_dir = Path(__file__).resolve().parent
  load_standard_env_files(repo_root=repo_root, agent_dir=agent_dir)

  session_service_uri = to_asyncpg_sqlalchemy_url(require_env("DATABASE_URL"))

  return get_fast_api_app(
      agents_dir=_agents_dir(),
      session_service_uri=session_service_uri,
      web=True,
  )


app = create_app()


@app.get("/health")
async def health() -> dict[str, str]:
  return {"status": "ok"}


def main() -> None:
  host = os.getenv("HOST", DEFAULT_HOST)
  port = int(os.getenv("PORT", str(DEFAULT_PORT)))
  uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
  main()