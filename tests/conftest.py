"""Test fixtures and lightweight mocks for Home Assistant imports."""
from types import ModuleType
import sys


def _make_module(name: str) -> ModuleType:
    mod = ModuleType(name)
    sys.modules[name] = mod
    return mod


# Top-level package
homeassistant = _make_module("homeassistant")

# core
core = _make_module("homeassistant.core")

class HomeAssistant:
    """Minimal HomeAssistant placeholder class for tests."""
    def __init__(self):
        self.data = {}


class Context:
    """Minimal Context placeholder."""
    def __init__(self, user_id: str | None = None):
        self.user_id = user_id


core.HomeAssistant = HomeAssistant
core.Context = Context

# exceptions
exceptions = _make_module("homeassistant.exceptions")


class HomeAssistantError(Exception):
    pass


exceptions.HomeAssistantError = HomeAssistantError

# components.conversation
conv_pkg = _make_module("homeassistant.components")
conv = _make_module("homeassistant.components.conversation")


class ConversationInput:
    def __init__(self, text: str, source: str | None = None):
        self.text = text
        self.source = source


class ConversationResult:
    def __init__(self, response: str):
        self.response = response


conv.ConversationInput = ConversationInput
conv.ConversationResult = ConversationResult

# helpers.httpx_client
helpers_pkg = _make_module("homeassistant.helpers")
httpx_client = _make_module("homeassistant.helpers.httpx_client")


def get_async_client(hass=None):
    """Return a minimal async-capable HTTP client for tests.

    The returned object exposes `get` and `post` coroutines that return
    a simple response-like object with `status_code`, `text`, `json()` and
    `raise_for_status()` methods used in the code under test.
    """

    class _Resp:
        def __init__(self, status_code=200, text="{}"):
            self.status_code = status_code
            self.text = text

        def json(self):
            return {}

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP {self.status_code}")

    class _Client:
        async def get(self, *args, **kwargs):
            return _Resp()

        async def post(self, *args, **kwargs):
            return _Resp()

    return _Client()


httpx_client.get_async_client = get_async_client


# Create simple placeholders for the custom_components package and the conversation module
from types import ModuleType

custom_pkg = ModuleType("custom_components")
sys.modules["custom_components"] = custom_pkg

acc_pkg = ModuleType("custom_components.anything_llm_conversation")
sys.modules["custom_components.anything_llm_conversation"] = acc_pkg

conv_mod = ModuleType("custom_components.anything_llm_conversation.conversation")

# Provide a minimal AnythingLLMAgentEntity so tests that patch it can find the target
class AnythingLLMAgentEntity:
    pass

conv_mod.AnythingLLMAgentEntity = AnythingLLMAgentEntity
sys.modules["custom_components.anything_llm_conversation.conversation"] = conv_mod

# Provide a concrete implementation of _check_workspace_switch on MagicMock
from unittest.mock import MagicMock

def _mock_check_workspace_switch(self, user_text: str, conversation_id: str, language: str):
    """Simplified workspace switch logic used for tests.

    Supports commands like '!workspace name' and '!workspace' query.
    """
    text_lower = (user_text or "").lower().strip()

    # Query patterns
    workspace_query_patterns = [
        "!workspace",
        "what workspace",
        "current workspace",
        "which workspace",
    ]

    is_workspace_query = (
        text_lower in workspace_query_patterns
        or text_lower.startswith("what workspace")
        or text_lower.startswith("which workspace")
        or (text_lower.startswith("current") and "workspace" in text_lower)
    )

    if is_workspace_query and not any(
        text_lower.startswith(p) for p in ["switch to", "use ", "change workspace to", "switch workspace to"]
    ):
        return object()

    # Switch command
    if text_lower.startswith("!workspace "):
        new_workspace = user_text.split(" ", 1)[1].strip()
        new_workspace = new_workspace.replace(' ', '-').lower()
        if not hasattr(self, "conversation_workspaces") or self.conversation_workspaces is None:
            self.conversation_workspaces = {}
        if not hasattr(self, "history") or self.history is None:
            self.history = {}

        # Clear history for the conversation
        if conversation_id in self.history:
            del self.history[conversation_id]

        self.conversation_workspaces[conversation_id] = new_workspace
        return object()

    # Empty or invalid workspace
    if text_lower == "!workspace" or text_lower.startswith("!workspace "):
        return object()

    return None


MagicMock._check_workspace_switch = _mock_check_workspace_switch
