"""Helper functions for AnythingLLM Conversation component."""

import asyncio
import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.httpx_client import get_async_client

from .const import DEFAULT_HEALTH_CHECK_TIMEOUT, DEFAULT_CHAT_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class AnythingLLMClient:
    """AnythingLLM API client."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        base_url: str,
        workspace_slug: str,
        failover_api_key: str | None = None,
        failover_base_url: str | None = None,
        failover_workspace_slug: str | None = None,
        failover_thread_slug: str | None = None,
    ):
        """Initialize AnythingLLM client."""
        self.hass = hass
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.workspace_slug = workspace_slug
        self.failover_api_key = failover_api_key
        self.failover_base_url = failover_base_url.rstrip("/") if failover_base_url else None
        self.failover_workspace_slug = failover_workspace_slug
        self.failover_thread_slug = failover_thread_slug
        self.http_client = get_async_client(hass)
        self.using_failover = False

    async def check_endpoint_health(self, base_url: str, api_key: str) -> bool:
        """Check if AnythingLLM endpoint is active."""
        try:
            # Try to ping the API - AnythingLLM may not have a dedicated health endpoint
            # So we'll try a simple workspace list or system endpoint
            health_url = f"{base_url}/v1/system"
            response = await self.http_client.get(
                health_url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=DEFAULT_HEALTH_CHECK_TIMEOUT,
            )
            return response.status_code in (200, 401, 403)  # 401/403 means endpoint is up but auth issue
        except Exception as err:
            _LOGGER.debug("Health check failed for %s: %s", base_url, err)
            return False

    async def get_active_endpoint(self) -> tuple[str, str, str]:
        """Get active endpoint, failing over if necessary."""
        # Check primary endpoint
        primary_healthy = await self.check_endpoint_health(self.base_url, self.api_key)
        
        if primary_healthy:
            if self.using_failover:
                _LOGGER.info("Primary endpoint is back online, switching from failover")
                self.using_failover = False
            return self.base_url, self.api_key, self.workspace_slug

        # Primary is down, try failover if configured
        if self.failover_base_url and self.failover_api_key:
            _LOGGER.warning("Primary endpoint unavailable, switching to failover")
            if not self.using_failover:
                _LOGGER.info("Switched to failover endpoint")
                self.using_failover = True
            return self.failover_base_url, self.failover_api_key, self.failover_workspace_slug or self.workspace_slug
        else:
            _LOGGER.error("Primary endpoint unavailable and no failover configured")
            raise HomeAssistantError("AnythingLLM endpoint is unavailable")

    async def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.5,
        max_tokens: int = 150,
        thread_slug: str | None = None,
        failover_thread_slug: str | None = None,
    ) -> dict:
        """Send chat completion request to AnythingLLM."""
        base_url, api_key, workspace_slug = await self.get_active_endpoint()
        
        # Update failover_thread_slug if provided (allows dynamic updates without client reload)
        if failover_thread_slug is not None:
            self.failover_thread_slug = failover_thread_slug
        
        # Determine which thread slug to use based on active endpoint
        # When using failover, use failover_thread_slug if set, otherwise use workspace default (None)
        # When using primary, use thread_slug
        if self.using_failover:
            active_thread_slug = self.failover_thread_slug
        else:
            active_thread_slug = thread_slug
        
        # Construct AnythingLLM API endpoint - use thread slug in URL if provided
        if active_thread_slug:
            chat_url = f"{base_url}/v1/workspace/{workspace_slug}/thread/{active_thread_slug}/chat"
        else:
            chat_url = f"{base_url}/v1/workspace/{workspace_slug}/chat"
        
        payload = {
            "message": messages[-1]["content"] if messages else "",
            "mode": "chat",
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Try up to 2 times on the selected endpoint
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = await self.http_client.post(
                    chat_url,
                    json=payload,
                    headers=headers,
                    timeout=DEFAULT_CHAT_TIMEOUT,
                )
                _LOGGER.debug("AnythingLLM response status: %s, body: %s", response.status_code, response.text[:500])
                response.raise_for_status()
                return response.json()
            except Exception as err:
                _LOGGER.error("Error calling AnythingLLM API at %s (attempt %d/%d): %s", base_url, attempt + 1, max_retries, err)
                
                # If this was the last retry, try switching endpoints
                if attempt == max_retries - 1:
                    # If we were using failover and it failed, try primary one more time
                    if self.using_failover and self.failover_base_url:
                        _LOGGER.warning("Failover endpoint failed after retries, trying primary endpoint")
                        try:
                            # Construct primary URL with thread slug if provided
                            if thread_slug:
                                primary_url = f"{self.base_url}/v1/workspace/{self.workspace_slug}/thread/{thread_slug}/chat"
                            else:
                                primary_url = f"{self.base_url}/v1/workspace/{self.workspace_slug}/chat"
                            primary_headers = {
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json",
                            }
                            response = await self.http_client.post(
                                primary_url,
                                json=payload,
                                headers=primary_headers,
                                timeout=DEFAULT_CHAT_TIMEOUT,
                            )
                            _LOGGER.debug("Primary retry response status: %s, body: %s", response.status_code, response.text[:500])
                            response.raise_for_status()
                            _LOGGER.info("Primary endpoint succeeded, switching back")
                            self.using_failover = False
                            return response.json()
                        except Exception as primary_err:
                            _LOGGER.error("Primary endpoint also failed: %s", primary_err)
                    
                    raise HomeAssistantError(f"AnythingLLM API error: {err}") from err
                
                # Wait a bit before retrying (exponential backoff)
                await asyncio.sleep(0.5 * (attempt + 1))



async def get_anythingllm_client(
    hass: HomeAssistant,
    api_key: str,
    base_url: str,
    workspace_slug: str,
    failover_api_key: str | None = None,
    failover_base_url: str | None = None,
    failover_workspace_slug: str | None = None,
    failover_thread_slug: str | None = None,
) -> AnythingLLMClient:
    """Create and validate AnythingLLM client."""
    client = AnythingLLMClient(
        hass,
        api_key,
        base_url,
        workspace_slug,
        failover_api_key,
        failover_base_url,
        failover_workspace_slug,
        failover_thread_slug,
    )
    
    # Skip health check during setup - it will be done at conversation time
    # This allows installation even if the server is temporarily down
    _LOGGER.info("AnythingLLM client created for %s (health check will occur at conversation time)", base_url)
    
    return client


