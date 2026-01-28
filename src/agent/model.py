"""Model configuration for the agents."""

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# Determine model configuration
model_name = os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-flash")
model: Any = model_name

# Explicitly use LiteLlm for OpenRouter or other provider-prefixed models
# that might not be auto-detected by ADK's registry.
if model_name.lower().startswith("openrouter/") or "/" in model_name:
    try:
        from google.adk.models import LiteLlm

        logger.info(f"Using LiteLlm for model: {model_name}")
        model = LiteLlm(model=model_name)
    except ImportError:
        logger.warning(
            "LiteLlm not available, falling back to string model name. "
            "OpenRouter models may not work."
        )
