"""Model configuration for the agents."""

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# Determine model configuration
# Determine LLM provider
llm_provider = os.getenv("LLM_PROVIDER", "openrouter").lower()

model: Any

try:
    from google.adk.models import LiteLlm

    if llm_provider == "local":
        model_name = os.getenv("LOCAL_LLM_MODEL", "ollama/medgemma")
        api_base = os.getenv("LOCAL_LLM_API_BASE")
        api_key = "local"  # dummy key for local servers

        logger.info(
            f"Using local LLM via LiteLlm | model={model_name} base={api_base}"
        )

        model = LiteLlm(
            model=model_name,
            api_base=api_base,
            api_key=api_key,
        )

    else:
        model_name = os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-flash")

        logger.info(f"Using OpenRouter model via LiteLlm: {model_name}")

        model = LiteLlm(
            model=model_name,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            api_base="https://openrouter.ai/api/v1",
        )

except ImportError:
    logger.warning(
        "LiteLlm not available, falling back to string model name."
    )
    model = os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-flash")
