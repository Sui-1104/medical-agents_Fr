"""Tests for model configuration."""

import importlib
import os
import sys
from unittest.mock import MagicMock, patch

import pytest


def test_model_selection_default() -> None:
    """Test default model selection."""
    with patch.dict(os.environ, {}, clear=True):
        if "agent.model" in sys.modules:
            module = importlib.reload(sys.modules["agent.model"])
        else:
            import agent.model

            module = agent.model

        assert module.model == "gemini-2.5-flash"


def test_model_selection_litellm() -> None:
    """Test LiteLlm selection for openrouter models."""
    mock_litellm_class = MagicMock()

    # We need to mock the module google.adk.models so it has LiteLlm
    mock_adk_models = MagicMock()
    mock_adk_models.LiteLlm = mock_litellm_class

    with (
        patch.dict(os.environ, {"ROOT_AGENT_MODEL": "openrouter/gpt-4"}),
        patch.dict(sys.modules, {"google.adk.models": mock_adk_models}),
    ):
        if "agent.model" in sys.modules:
            module = importlib.reload(sys.modules["agent.model"])
        else:
            import agent.model

            module = agent.model

        mock_litellm_class.assert_called_with(model="openrouter/gpt-4")
        assert module.model == mock_litellm_class.return_value


def test_model_selection_litellm_import_error(caplog: pytest.LogCaptureFixture) -> None:


    """Test fallback when LiteLlm import fails."""


    # Assume 'google.adk.models' is not installed in the test env


    # (or force it to appear so).





    with patch.dict(


        os.environ, {"ROOT_AGENT_MODEL": "openrouter/gpt-4"}


    ), patch.dict(sys.modules):


        # Remove valid module if exists


        sys.modules.pop("google.adk.models", None)





        # We can't easily force an import error for a specific module via sys.modules


        # without interfering with others unless we use a custom finder.





        # Let's try to mock the module in sys.modules such that it does NOT have LiteLlm


        # But the code says `from google.adk.models import LiteLlm`.


        # If the module exists but doesn't have LiteLlm, it raises ImportError.





        # Wait, `from module import name` -> raises ImportError if name not found.


        # Let's try that.





        mock_models = MagicMock(spec=[])  # Empty spec





        with patch.dict(sys.modules, {"google.adk.models": mock_models}):


            if "agent.model" in sys.modules:


                module = importlib.reload(sys.modules["agent.model"])


            else:


                import agent.model





                module = agent.model





            # Check that we logged the warning


            assert "LiteLlm not available" in caplog.text


            # And model fell back to string


            assert module.model == "openrouter/gpt-4"



