"""AnythingLLM Conversation agent entity."""

from __future__ import annotations

import html
import logging
import re
from typing import Literal

from homeassistant.components import conversation
from homeassistant.components.conversation import (
    ChatLog,
    ConversationEntity,
    ConversationEntityFeature,
    ConversationInput,
    ConversationResult,
    async_get_chat_log,
)
from homeassistant.components.homeassistant.exposed_entities import async_should_expose
from homeassistant.config_entries import ConfigSubentry
from homeassistant.const import ATTR_NAME, MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, TemplateError
from homeassistant.helpers import (
    device_registry as dr,
    entity_registry as er,
    intent,
    template,
)
from homeassistant.helpers.chat_session import async_get_chat_session
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AnythingLLMConfigEntry
from .const import (
    CONF_ATTACH_USERNAME,
    CONF_WORKSPACE_SLUG,
    CONF_MAX_TOKENS,
    CONF_PROMPT,
    CONF_TEMPERATURE,
    CONF_THREAD_SLUG,
    CONF_FAILOVER_THREAD_SLUG,
    DEFAULT_ATTACH_USERNAME,
    DEFAULT_WORKSPACE_SLUG,
    DEFAULT_MAX_TOKENS,
    DEFAULT_PROMPT,
    DEFAULT_TEMPERATURE,
    DEFAULT_THREAD_SLUG,
    DEFAULT_FAILOVER_THREAD_SLUG,
    DOMAIN,
    EVENT_CONVERSATION_FINISHED,
)

_LOGGER = logging.getLogger(__name__)

# Compiled regex patterns for text cleaning (performance optimization)
_RE_THINK_TAGS = re.compile(r'<think>.*?</think>', flags=re.DOTALL | re.IGNORECASE)
_RE_MARKDOWN_LINKS = re.compile(r'\[([^\]]+)\]\([^\)]+\)')
_RE_WHITESPACE = re.compile(r'\s+')
_RE_BR_TAGS = re.compile(r'<br\s*/?>', flags=re.IGNORECASE)
_RE_HTML_TAGS = re.compile(r'<[^>]+>')
_RE_CELSIUS = re.compile(r'(\d+)C\b')
_RE_FAHRENHEIT = re.compile(r'(\d+)F\b')

# Follow-up detection phrases (compiled once for performance)
_FOLLOW_UP_PHRASES = frozenset([
    "which one",
    "would you like",
    "do you want",
    "would you prefer",
    "which do you",
    "what would you",
    "shall i",
    "should i",
    "choose from",
    "select from",
    "pick from",
])


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AnythingLLMConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the AnythingLLM Conversation entities."""
    for subentry in config_entry.subentries.values():
        if subentry.subentry_type != "conversation":
            continue

        async_add_entities(
            [AnythingLLMAgentEntity(hass, config_entry, subentry)],
            config_subentry_id=subentry.subentry_id,
        )


class AnythingLLMAgentEntity(
    ConversationEntity, conversation.AbstractConversationAgent
):
    """AnythingLLM conversation agent."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_features = ConversationEntityFeature.CONTROL

    def __init__(
        self,
        hass: HomeAssistant,
        entry: AnythingLLMConfigEntry,
        subentry: ConfigSubentry,
    ) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.subentry = subentry
        self.history: dict[str, list[dict]] = {}

        self.options = subentry.data
        self._attr_unique_id = subentry.subentry_id
        
        # Caching for performance optimization
        self._exposed_entities_cache: list[dict[str, any]] | None = None
        self._last_states_count: int = 0
        self._system_prompt_cache: dict[str, str] = {}  # Cache by device_id
        self._last_prompt_template: str = self.options.get(CONF_PROMPT, DEFAULT_PROMPT)

        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, subentry.subentry_id)},
            name=subentry.title,
            manufacturer="AnythingLLM",
            model=self.options.get(CONF_WORKSPACE_SLUG, DEFAULT_WORKSPACE_SLUG),
            entry_type=dr.DeviceEntryType.SERVICE,
        )
        self.client = entry.runtime_data

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        """Process a sentence."""
        with (
            async_get_chat_session(self.hass, user_input.conversation_id) as session,
            async_get_chat_log(self.hass, session, user_input) as chat_log,
        ):
            return await self._async_handle_message(user_input, chat_log)

    async def _async_handle_message(
        self,
        user_input: ConversationInput,
        chat_log: ChatLog,
    ) -> ConversationResult:
        """Call the API."""
        exposed_entities = self.get_exposed_entities()

        conversation_id = chat_log.conversation_id
        if conversation_id in self.history:
            messages = self.history[conversation_id]
        else:
            user_input.conversation_id = conversation_id
            try:
                system_message = self._generate_system_message(
                    exposed_entities, user_input
                )
            except TemplateError as err:
                _LOGGER.error("Error rendering prompt: %s", err)
                intent_response = intent.IntentResponse(language=user_input.language)
                intent_response.async_set_error(
                    intent.IntentResponseErrorCode.UNKNOWN,
                    f"Sorry, I had a problem with my template: {err}",
                )
                return conversation.ConversationResult(
                    response=intent_response, conversation_id=conversation_id
                )
            messages = [system_message]
        user_message = {"role": "user", "content": user_input.text}
        if self.options.get(CONF_ATTACH_USERNAME, DEFAULT_ATTACH_USERNAME):
            user = user_input.context.user_id
            if user is not None:
                user_message[ATTR_NAME] = user

        messages.append(user_message)

        try:
            query_response = await self.query(user_input, messages)
        except Exception as err:
            _LOGGER.error(err)
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                f"Sorry, I had a problem talking to AnythingLLM: {err}",
            )
            return conversation.ConversationResult(
                response=intent_response, conversation_id=conversation_id
            )

        # Store assistant response in history
        assistant_message = {"role": "assistant", "content": query_response.text}
        messages.append(assistant_message)
        self.history[conversation_id] = messages

        self.hass.bus.async_fire(
            EVENT_CONVERSATION_FINISHED,
            {
                "response": query_response.response,
                "user_input": user_input,
                "messages": messages,
                "agent_id": self.subentry.subentry_id,
            },
        )

        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(query_response.text)

        # Detect if LLM is asking a follow-up question to enable continued conversation
        response_text = query_response.text or ""
        response_lower = response_text.lower()
        should_continue = response_text.rstrip().endswith("?") or any(
            phrase in response_lower for phrase in _FOLLOW_UP_PHRASES
        )

        return conversation.ConversationResult(
            response=intent_response,
            conversation_id=conversation_id,
            continue_conversation=should_continue,
        )

    def _generate_system_message(
        self, exposed_entities, user_input: conversation.ConversationInput
    ):
        raw_prompt = self.options.get(CONF_PROMPT, DEFAULT_PROMPT)
        prompt = self._async_generate_prompt(raw_prompt, exposed_entities, user_input)
        return {"role": "system", "content": prompt}

    def _async_generate_prompt(
        self,
        raw_prompt: str,
        exposed_entities,
        user_input: conversation.ConversationInput,
    ) -> str:
        """Generate a prompt for the user."""
        # Check if prompt template changed - invalidate cache if so
        if raw_prompt != self._last_prompt_template:
            self._system_prompt_cache.clear()
            self._last_prompt_template = raw_prompt
            _LOGGER.debug("System prompt cache cleared due to template change")
        
        # Use device_id as cache key (different devices might have different prompts)
        cache_key = f"{user_input.device_id or 'default'}_{len(exposed_entities)}"
        
        # Return cached prompt if available
        if cache_key in self._system_prompt_cache:
            return self._system_prompt_cache[cache_key]
        
        # Generate and cache the prompt
        prompt = template.Template(raw_prompt, self.hass).async_render(
            {
                "ha_name": self.hass.config.location_name,
                "exposed_entities": exposed_entities,
                "current_device_id": user_input.device_id,
            },
            parse_result=False,
        )
        
        self._system_prompt_cache[cache_key] = prompt
        _LOGGER.debug("Cached system prompt for key: %s", cache_key)
        return prompt

    def get_exposed_entities(self) -> list[dict[str, any]]:
        # Check if we can use cached entities
        current_states_count = len(self.hass.states.async_all())
        
        # Invalidate cache if number of states changed (entities added/removed)
        if current_states_count != self._last_states_count:
            self._exposed_entities_cache = None
            self._system_prompt_cache.clear()  # Clear prompt cache when entities change
            self._last_states_count = current_states_count
            _LOGGER.debug("Entity cache invalidated due to state count change")
        
        # Return cached entities if available
        if self._exposed_entities_cache is not None:
            return self._exposed_entities_cache
        
        # Build fresh entity list - get registry once
        entity_registry = er.async_get(self.hass)
        states = [
            state
            for state in self.hass.states.async_all()
            if async_should_expose(self.hass, conversation.DOMAIN, state.entity_id)
        ]
        exposed_entities = []
        for state in states:
            entity_id = state.entity_id
            entity = entity_registry.async_get(entity_id)

            exposed_entities.append(
                {
                    "entity_id": entity_id,
                    "name": state.name,
                    "state": state.state,
                    "aliases": entity.aliases if entity and entity.aliases else [],
                }
            )
        
        # Cache the result
        self._exposed_entities_cache = exposed_entities
        _LOGGER.debug("Cached %d exposed entities", len(exposed_entities))
        return exposed_entities

    def _clean_response_for_tts(self, text: str) -> str:
        """Clean up LLM response for text-to-speech."""
        # Option 1: Remove <think> tags and their content
        text = _RE_THINK_TAGS.sub('', text)
        
        # Option 2: Remove only the <think> tags but keep the content inside
        # Uncomment below and comment out Option 1 above to use this instead
        # text = re.sub(r'</?think>', '', text, flags=re.IGNORECASE)
        
        # Option 3: Remove asterisks (markdown bold/italic)
        text = text.replace('*', '')
        
        # Option 4: Remove other common markdown formatting
        # Uncomment the ones you want to remove:
        # text = text.replace('_', '')  # Remove underscores (italic)
        # text = text.replace('~', '')  # Remove tildes (strikethrough)
        # text = text.replace('`', '')  # Remove backticks (code)
        # text = text.replace('#', '')  # Remove hash symbols (headers)
        text = _RE_MARKDOWN_LINKS.sub(r'\1', text)  # Convert [text](url) to just text
        # text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)  # Remove code blocks
        # text = re.sub(r'https?://\S+', '', text)  # Remove URLs
        text = _RE_WHITESPACE.sub(' ', text)  # Normalize whitespace to single spaces
        
        # Option 5: HTML entity handling
        # Uncomment to convert common HTML entities to readable text:
        text = html.unescape(text)  # Converts &nbsp; &amp; &lt; &gt; etc to actual characters
        text = _RE_BR_TAGS.sub(' ', text)  # Convert <br> to space
        text = _RE_HTML_TAGS.sub('', text)  # Remove any other HTML tags
        
        # Option 6: Emoji handling
        # Uncomment to handle emojis (requires emoji package: pip install emoji):
        # import emoji
        # text = emoji.replace_emoji(text, replace='')  # Remove all emojis
        # OR convert emojis to text descriptions:
        # text = emoji.demojize(text, delimiters=(" ", " "))  # 😀 becomes "grinning face"
        
        # Option 7: Special character cleanup
        # Uncomment to clean up characters that don't work well with TTS:
        text = text.replace('°', ' degrees ')  # Temperature symbols
        text = text.replace('%', ' percent ')  # Percent signs
        text = text.replace('$', ' dollars ')  # Currency
        text = text.replace('€', ' euros ')
        text = text.replace('£', ' pounds ')
        text = _RE_CELSIUS.sub(r'\1 degrees Celsius', text)  # 25C -> 25 degrees Celsius
        text = _RE_FAHRENHEIT.sub(r'\1 degrees Fahrenheit', text)  # 77F -> 77 degrees Fahrenheit
        
        return text.strip()

    async def query(
        self,
        user_input: conversation.ConversationInput,
        messages: list[dict],
    ) -> AnythingLLMQueryResponse:
        """Process a sentence."""
        workspace_slug = self.options.get(CONF_WORKSPACE_SLUG, DEFAULT_WORKSPACE_SLUG)
        max_tokens = self.options.get(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS)
        temperature = self.options.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE)
        thread_slug = self.options.get(CONF_THREAD_SLUG, DEFAULT_THREAD_SLUG)
        failover_thread_slug = self.options.get(CONF_FAILOVER_THREAD_SLUG, DEFAULT_FAILOVER_THREAD_SLUG)

        _LOGGER.debug("Sending request to AnythingLLM workspace %s with %d messages", workspace_slug, len(messages))

        # Call AnythingLLM API
        try:
            response = await self.client.chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                thread_slug=thread_slug if thread_slug else None,
                failover_thread_slug=failover_thread_slug if failover_thread_slug else None,
            )
        except Exception as err:
            _LOGGER.error("Error from AnythingLLM: %s", err)
            raise

        _LOGGER.debug("Received response from AnythingLLM (type: %s)", response.get("type", "unknown"))

        # Extract the text response from AnythingLLM
        # AnythingLLM returns: {"textResponse": "...", "type": "chat", ...}
        text_response = response.get("textResponse", "")
        
        if not text_response:
            raise HomeAssistantError("Empty response from AnythingLLM")

        # Remove <think> tags before sending to TTS
        text_response = self._clean_response_for_tts(text_response)

        return AnythingLLMQueryResponse(response=response, text=text_response)


class AnythingLLMQueryResponse:
    """AnythingLLM query response value object."""

    def __init__(
        self, response: dict, text: str
    ) -> None:
        """Initialize AnythingLLM query response value object."""
        self.response = response
        self.text = text
