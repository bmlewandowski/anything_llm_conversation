#!/usr/bin/env python3
"""Tests for AnythingLLM client functionality (mock-based)."""

import asyncio
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Optional


class MockHTTPResponse:
    """Mock HTTP response."""
    
    def __init__(self, status_code: int, json_data: Optional[dict] = None):
        self.status_code = status_code
        self._json_data = json_data or {}
    
    async def json(self):
        return self._json_data


class MockAnythingLLMClient:
    """Mock AnythingLLM client for testing."""
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        workspace_slug: str,
        failover_api_key: Optional[str] = None,
        failover_base_url: Optional[str] = None,
        failover_workspace_slug: Optional[str] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.workspace_slug = workspace_slug
        self.failover_api_key = failover_api_key
        self.failover_base_url = failover_base_url.rstrip("/") if failover_base_url else None
        self.failover_workspace_slug = failover_workspace_slug
        self.using_failover = False
        self.http_client = MagicMock()
    
    async def check_endpoint_health(self, base_url: str, api_key: str) -> bool:
        """Check if AnythingLLM endpoint is active."""
        try:
            health_url = f"{base_url}/v1/system"
            response = await self.http_client.get(
                health_url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=3.0,
            )
            return response.status_code in (200, 401, 403)
        except Exception:
            return False
    
    async def get_active_endpoint(self) -> tuple[str, str, str]:
        """Get active endpoint, failing over if necessary."""
        primary_healthy = await self.check_endpoint_health(self.base_url, self.api_key)
        
        if primary_healthy:
            if self.using_failover:
                self.using_failover = False
            return self.base_url, self.api_key, self.workspace_slug
        
        if self.failover_base_url and self.failover_api_key:
            if not self.using_failover:
                self.using_failover = True
            return (
                self.failover_base_url,
                self.failover_api_key,
                self.failover_workspace_slug or self.workspace_slug
            )
        else:
            raise Exception("AnythingLLM endpoint is unavailable")
    
    async def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.5,
        max_tokens: int = 150,
        thread_slug: Optional[str] = None,
    ) -> dict:
        """Send chat completion request to AnythingLLM."""
        base_url, api_key, workspace_slug = await self.get_active_endpoint()
        
        if thread_slug:
            chat_url = f"{base_url}/v1/workspace/{workspace_slug}/thread/{thread_slug}/chat"
        else:
            chat_url = f"{base_url}/v1/workspace/{workspace_slug}/chat"
        
        payload = {
            "message": messages[-1]["content"] if messages else "",
            "mode": "chat",
        }
        
        response = await self.http_client.post(
            chat_url,
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=45.0,
        )
        
        if response.status_code != 200:
            raise Exception(f"Chat request failed with status {response.status_code}")
        
        return await response.json()


class TestAnythingLLMClient:
    """Test AnythingLLM client functionality."""
    
    @staticmethod
    async def test_health_check_success():
        """Test successful health check."""
        client = MockAnythingLLMClient(
            api_key="test-key",
            base_url="http://localhost:3001/api",
            workspace_slug="test-workspace"
        )
        
        # Mock successful response
        client.http_client.get = AsyncMock(return_value=MockHTTPResponse(200))
        
        result = await client.check_endpoint_health("http://localhost:3001/api", "test-key")
        assert result == True, "Health check should succeed with status 200"
    
    @staticmethod
    async def test_health_check_auth_errors():
        """Test health check with auth errors (still considered healthy)."""
        client = MockAnythingLLMClient(
            api_key="test-key",
            base_url="http://localhost:3001/api",
            workspace_slug="test-workspace"
        )
        
        # 401 and 403 mean endpoint is up but auth issue
        for status_code in [401, 403]:
            client.http_client.get = AsyncMock(return_value=MockHTTPResponse(status_code))
            result = await client.check_endpoint_health("http://localhost:3001/api", "test-key")
            assert result == True, f"Health check should succeed with status {status_code}"
    
    @staticmethod
    async def test_health_check_failure():
        """Test health check failure."""
        client = MockAnythingLLMClient(
            api_key="test-key",
            base_url="http://localhost:3001/api",
            workspace_slug="test-workspace"
        )
        
        # Mock connection error
        client.http_client.get = AsyncMock(side_effect=Exception("Connection refused"))
        
        result = await client.check_endpoint_health("http://localhost:3001/api", "test-key")
        assert result == False, "Health check should fail on exception"
    
    @staticmethod
    async def test_primary_endpoint_selection():
        """Test that primary endpoint is used when healthy."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
            failover_api_key="failover-key",
            failover_base_url="http://failover:3001/api",
            failover_workspace_slug="failover-workspace"
        )
        
        # Mock primary as healthy
        client.http_client.get = AsyncMock(return_value=MockHTTPResponse(200))
        
        url, key, workspace = await client.get_active_endpoint()
        assert url == "http://primary:3001/api", "Should use primary URL"
        assert key == "primary-key", "Should use primary key"
        assert workspace == "primary-workspace", "Should use primary workspace"
        assert client.using_failover == False, "Should not be using failover"
    
    @staticmethod
    async def test_failover_when_primary_down():
        """Test failover to secondary endpoint when primary is down."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
            failover_api_key="failover-key",
            failover_base_url="http://failover:3001/api",
            failover_workspace_slug="failover-workspace"
        )
        
        # Mock primary as down, failover as up
        async def mock_health_check(url, headers, timeout):
            if "primary" in url:
                raise Exception("Connection refused")
            return MockHTTPResponse(200)
        
        client.http_client.get = mock_health_check
        
        url, key, workspace = await client.get_active_endpoint()
        assert url == "http://failover:3001/api", "Should use failover URL"
        assert key == "failover-key", "Should use failover key"
        assert workspace == "failover-workspace", "Should use failover workspace"
        assert client.using_failover == True, "Should be using failover"
    
    @staticmethod
    async def test_failover_workspace_default():
        """Test that failover uses primary workspace when not specified."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
            failover_api_key="failover-key",
            failover_base_url="http://failover:3001/api",
            failover_workspace_slug=None  # Not specified
        )
        
        # Mock primary as down
        async def mock_health_check(url, headers, timeout):
            if "primary" in url:
                raise Exception("Connection refused")
            return MockHTTPResponse(200)
        
        client.http_client.get = mock_health_check
        
        url, key, workspace = await client.get_active_endpoint()
        assert workspace == "primary-workspace", "Should use primary workspace as default"
    
    @staticmethod
    async def test_no_failover_configured():
        """Test error when primary down and no failover configured."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
            failover_api_key=None,
            failover_base_url=None
        )
        
        # Mock primary as down
        client.http_client.get = AsyncMock(side_effect=Exception("Connection refused"))
        
        try:
            await client.get_active_endpoint()
            assert False, "Should have raised exception"
        except Exception as e:
            assert "unavailable" in str(e).lower(), "Should indicate endpoint unavailable"
    
    @staticmethod
    async def test_return_to_primary_after_recovery():
        """Test that client returns to primary when it recovers."""
        client = MockAnythingLLMClient(
            api_key="primary-key",
            base_url="http://primary:3001/api",
            workspace_slug="primary-workspace",
            failover_api_key="failover-key",
            failover_base_url="http://failover:3001/api"
        )
        
        # First call - primary down, use failover
        call_count = 0
        
        async def mock_health_check(url, headers, timeout):
            nonlocal call_count
            call_count += 1
            if call_count == 1 and "primary" in url:
                raise Exception("Primary down")
            return MockHTTPResponse(200)
        
        client.http_client.get = mock_health_check
        
        # First request should use failover
        url1, _, _ = await client.get_active_endpoint()
        assert "failover" in url1, "First request should use failover"
        assert client.using_failover == True
        
        # Second request should return to primary
        url2, _, _ = await client.get_active_endpoint()
        assert "primary" in url2, "Should return to primary when recovered"
        assert client.using_failover == False
    
    @staticmethod
    async def test_chat_without_thread():
        """Test chat completion without thread slug."""
        client = MockAnythingLLMClient(
            api_key="test-key",
            base_url="http://localhost:3001/api",
            workspace_slug="test-workspace"
        )
        
        # Mock healthy endpoint and successful chat
        client.http_client.get = AsyncMock(return_value=MockHTTPResponse(200))
        client.http_client.post = AsyncMock(return_value=MockHTTPResponse(
            200,
            {"textResponse": "Hello!", "type": "chat"}
        ))
        
        messages = [{"role": "user", "content": "Hi"}]
        response = await client.chat_completion(messages)
        
        assert response["textResponse"] == "Hello!"
        # Verify URL doesn't include thread
        call_args = client.http_client.post.call_args
        assert "/thread/" not in call_args[0][0], "Should not include thread in URL"
    
    @staticmethod
    async def test_chat_with_thread():
        """Test chat completion with thread slug."""
        client = MockAnythingLLMClient(
            api_key="test-key",
            base_url="http://localhost:3001/api",
            workspace_slug="test-workspace"
        )
        
        # Mock healthy endpoint and successful chat
        client.http_client.get = AsyncMock(return_value=MockHTTPResponse(200))
        client.http_client.post = AsyncMock(return_value=MockHTTPResponse(
            200,
            {"textResponse": "Hello!", "type": "chat"}
        ))
        
        messages = [{"role": "user", "content": "Hi"}]
        response = await client.chat_completion(messages, thread_slug="my-thread")
        
        assert response["textResponse"] == "Hello!"
        # Verify URL includes thread
        call_args = client.http_client.post.call_args
        assert "/thread/my-thread/chat" in call_args[0][0], "Should include thread in URL"


async def run_all_tests():
    """Run all test methods."""
    test_class = TestAnythingLLMClient()
    test_methods = [
        method for method in dir(test_class)
        if method.startswith('test_') and callable(getattr(test_class, method))
    ]
    
    total = len(test_methods)
    passed = 0
    failed = 0
    
    print("Testing AnythingLLM Client (Mock-based)")
    print("=" * 70)
    
    for method_name in test_methods:
        try:
            method = getattr(test_class, method_name)
            await method()
            print(f"✓ {method_name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {method_name}")
            print(f"  {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ {method_name} (unexpected error)")
            print(f"  {type(e).__name__}: {str(e)}")
            failed += 1
    
    print("=" * 70)
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run_all_tests()))
