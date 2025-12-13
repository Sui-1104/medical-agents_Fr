## google-adk (without GCP)

This repo shows how to use **Google ADK (Agent Development Kit)** locally without
Google Cloud Platform:

- **LLM provider**: OpenRouter via `LiteLlm` (open-source-friendly routing layer)
- **Session persistence**: Postgres (e.g. Neon) via ADK’s `DatabaseSessionService`
- **ADK Dev UI**: served locally via a small FastAPI wrapper (`jarvis/server.py`)

The key idea is that ADK is an **agent framework**: you can use it without Vertex AI /
Agent Engine as long as you provide:

- a model backend (here: OpenRouter)
- a session store (here: Postgres)

## Quickstart

### Prerequisites

- Python **3.11+**
- [`uv`](https://github.com/astral-sh/uv)
- A Postgres connection string (Neon works great)
- An OpenRouter API key

### 1) Configure env

Create `jarvis/.env`:

- **`OPENROUTER_API_KEY`**: your OpenRouter key
- **`DATABASE_URL`**: a Postgres URL (can be the standard `postgresql://...` form)

Notes:
- We normalize Postgres URLs for SQLAlchemy+asyncpg automatically (e.g.
  `sslmode=require` becomes `ssl=require`).

### 2) Install deps

```bash
uv sync
```

### 3) Run ADK Web locally (but backed by Postgres)

```bash
uv run python -m jarvis.server
```

Then open `http://127.0.0.1:8000`.

Notes:
- The Dev UI lists apps by scanning directories under `AGENTS_DIR`.
  By default this repo points ADK at `./agents`, which contains only `jarvis`,
  so you don't have to manually select it each run.

## Why not `adk web --session_service_uri ...`?

ADK’s CLI defaults to local SQLite session storage unless you pass
`--session_service_uri`. This repo provides `jarvis/server.py` so:

- you don’t have to remember a long CLI command
- sessions always go to Postgres (once `DATABASE_URL` is set)

## Development

See:
- `docs/development.md`
