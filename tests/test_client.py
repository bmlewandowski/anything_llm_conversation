#!/usr/bin/env python3
"""Tests for AnythingLLM client functionality (mock-based, no failover)."""

import asyncio
import sys
from unittest.mock import AsyncMock, MagicMock
from typing import Optional


class MockHTTPResponse:
    """Mock HTTP response."""

    def __init__(self, status_code: int, json_data: Optional[dict] = None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.is_success = status_code < 400

    def json(self):
        return self._json_data


class MockAnythingLLMClient:
    """Simplified mock matching the post-failover-removal AnythingLLMClient."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        workspace_slug: str,
        enable_health_check: bool = True,
        health_check_timeout: float = 3.0,
        chat_timeout: float = 60.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.workspace_slug = workspace_slug
        self.enable_health_check = enable_health_check
        self.health_check_timeout = health_check_timeout
        self.chat_timeout = chat_timeout
        self._primary_healthy: bool | None = None
        self.http_client = MagicMock()

    async def check_endpoint_health(self, base_url: str, api_key: str) -> bool:
        """Check if AnythingLLM endpoint is reachable."""
        try:
            health_url = f"{base_url}/v1/system"
            response = await self.http_client.get(
                health_url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=self.health_check_timeout,
            )
            return response.status_code in (200, 401, 403)
        except Exception:
            return False

    def get_active_endpoint(self) -> tuple[str, str, str]:
        """Return the primary endpoint; raise if known-unhealthy."""
        if not self.enable_health_check or self._primary_healthy is None:
            return self.base_url, self.api_key, self.workspace_slug
        if not self._primary_healthy:
            raise Exception("AnythingLLM endpoint is unavailable")
        return self.base_url, self.api_key, self.workspace_slug

    async def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.5,
        max_tokens: int = 150,
        workspace_slug: Optional[str] = None,
        thread_slug: Optional[str] = None,
    ) -> dict:
        """Send chat completion request to AnythingLLM."""
        base_url, api_key, active_workspace = self.get_active_endpoint()
        final_workspace = workspace_slug or active_workspace or self.workspace_slug

        if thread_slug:
            chat_url = f"{base_url}/v1/workspace/{final_workspace}/thread/{thread_slug}/chat"
        else:
            chat_url = f"{base_url}/v1/workspace/{final_workspace}/chat"

        payload = {
            "message": messages[-1]["content"] if messages else "",
            "mode": "chat",
        }

        response = await self.http_client.post(
            chat_url,
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=self.chat_timeout,
        )

        if not response.is_success:
            raise Exception(f"Chat request failed with status {response.status_code}")

        return response.json()


class TestAnythingLLMClient:
    """Test AnythingLLM client functionality."""

    @staticmethod
    def test_health_check_success():
        """Health check returns True for HTTP 200."""
        async def run():
            client = MockAnythingLLMClient(
                api_key="test-key",
                base_url="http://localhost:3001/api",
                workspace_slug="test-workspace",
            )
            client.http_client.get = AsyncMock(return_value=MockHTTPResponse(200))
            result = await client.check_endpoint_health("http://localhost:3001/api", "test-key")
            assert result is True
        asyncio.run(run())

    @staticmethod
    def test_health_check_auth_errors_still_healthy():
        """HTTP 401 and 403 mean the server is up — considered healthy."""
        async def run():
            client = MockAnythingLLMClient(
                api_key="test-key",
                base_url="http://localhost:3001/api",
                workspace_slug="test-workspace",
            )
            for status_code in (401, 403):
                client.http_client.get = AsyncMock(return_value=MockHTTPResponse(status_code))
                result = await client.check_endpoint_health("http://localhost:3001/api", "test-key")
                assert result is True, f"Should be healthy for status {status_code}"
        asyncio.run(run())

    @staticmethod
    def test_health_check_failure_on_exception():
        """Connection error → health check returns False."""
        async def run():
            client = MockAnythingLLMClient(
                api_key="test-key",
                base_url="http://localhost:3001/api",
                workspace_slug="test-workspace",
            )
            client.http_client.get = AsyncMock(side_effect=Exception("Connection refused"))
            result = await client.check_endpoint_health("http://localhost:3001/api", "test-key")
            assert result is False
        asyncio.run(run())

    @staticmethod
    def test_primary_endpoint_returned_when_healthy():
        """get_active_endpoint returns primary when _primary_healthy is True."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
        )
        client._primary_healthy = True
        url, key, workspace = client.get_active_endpoint()
        assert url == "http://primary:3001/api"
        assert key == "primary-key"
        assert workspace == "primary-workspace"

    @staticmethod
    def test_get_active_endpoint_raises_when_unhealthy():
        """get_active_endpoint raises when primary is known unavailable."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
        )
        client._primary_healthy = False
        try:
            client.get_active_endpoint()
            assert False, "Should have raised"
        except Exception as e:
            assert "unavailable" in str(e).lower()

    @staticmethod
    def test_get_active_endpoint_optimistic_before_first_check():
        """Before first health check (_primary_healthy is None), optimistically use primary."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
        )
        assert client._primary_healthy is None
        url, key, workspace = client.get_active_endpoint()
        assert url == "http://primary:3001/api"

    @staticmethod
    def test_health_check_disabled_always_returns_primary():
        """When health checks disabled, always return primary regardless of state."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
            enable_health_check=False,
        )
        client._primary_healthy = False  # Even if marked unhealthy, disabled = always serve
        url, key, workspace = client.get_active_endpoint()
        assert url == "http://primary:3001/api"

    @staticmethod
    def test_chat_without_thread():
        """Chat URL should not include /thread/ when no thread slug given."""
        async def run():
            client = MockAnythingLLMClient(
                api_key="test-key",
                base_url="http://localhost:3001/api",
                workspace_slug="test-workspace",
            )
            client._primary_healthy = True
            client.http_client.post = AsyncMock(
                return_value=MockHTTPResponse(200, {"textResponse": "Hello!", "type": "chat"})
            )
            messages = [{"role": "user", "content": "Hi"}]
            response = await client.chat_completion(messages)
            assert response["textResponse"] == "Hello!"
            call_url = client.http_client.post.call_args[0][0]
            assert "/thread/" not in call_url
        asyncio.run(run())

    @staticmethod
    def test_chat_with_thread():
        """Chat URL should include /thread/<slug>/chat when thread slug given."""
        async def run():
            client = MockAnythingLLMClient(
                api_key="test-key",
                base_url="http://localhost:3001/api",
                workspace_slug="test-workspace",
            )
            client._primary_healthy = True
            client.http_client.post = AsyncMock(
                return_value=MockHTTPResponse(200, {"textResponse": "Hello!", "type": "chat"})
            )
            messages = [{"role": "user", "content": "Hi"}]
            response = await client.chat_completion(messages, thread_slug="my-thread")
            assert response["textResponse"] == "Hello!"
            call_url = client.http_client.post.call_args[0][0]
            assert "/thread/my-thread/chat" in call_url
        asyncio.run(run())

    @staticmethod
    def test_workspace_override_in_chat_url():
        """Workspace override is reflected in the chat URL."""
        async def run():
            client = MockAnythingLLMClient(
                api_key="test-key",
                base_url="http://localhost:3001/api",
                workspace_slug="default-workspace",
            )
            client._primary_healthy = True
            client.http_client.post = AsyncMock(
                return_value=MockHTTPResponse(200, {"textResponse": "OK", "type": "chat"})
            )
            messages = [{"role": "user", "content": "Hi"}]
            await client.chat_completion(messages, workspace_slug="override-workspace")
            call_url = client.http_client.post.call_args[0][0]
            assert "/v1/workspace/override-workspace/" in call_url
        asyncio.run(run())

    @staticmethod
    def test_chat_thread_and_workspace_override():
        """Both workspace and thread overrides combine correctly in the URL."""
        async def run():
            client = MockAnythingLLMClient(
                api_key="test-key",
                base_url="http://localhost:3001/api",
                workspace_slug="default-workspace",
            )
            client._primary_healthy = True
            client.http_client.post = AsyncMock(
                return_value=MockHTTPResponse(200, {"textResponse": "OK", "type": "chat"})
            )
            messages = [{"role": "user", "content": "Hi"}]
            await client.chat_completion(
                messages, workspace_slug="analysis", thread_slug="session-123"
            )
            call_url = client.http_client.post.call_args[0][0]
            assert "/v1/workspace/analysis/thread/session-123/chat" in call_url
        asyncio.run(run())


async def run_all_tests():
    """Run all test methods (used when invoked directly, not via pytest)."""
    test_instance = TestAnythingLLMClient()
    methods = [m for m in dir(test_instance) if m.startswith("test_")]
    passed = failed = 0
    print("Testing AnythingLLM Client (simplified, no failover)")
    print("=" * 60)
    for name in methods:
        try:
            getattr(test_instance, name)()
            print(f"  PASS  {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {name}: {type(e).__name__}: {e}")
            failed += 1
    print("=" * 60)
    print(f"{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    import sys
    result = asyncio.run(run_all_tests())
    sys.exit(result)
