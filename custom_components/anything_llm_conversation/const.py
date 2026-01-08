"""Constants for the AnythingLLM Conversation integration."""

DOMAIN = "anything_llm_conversation"
DEFAULT_NAME = "AnythingLLM Conversation"
DEFAULT_CONVERSATION_NAME = "AnythingLLM Conversation"

CONF_BASE_URL = "base_url"
DEFAULT_CONF_BASE_URL = "http://localhost:3001/api"

# Failover configuration
CONF_FAILOVER_BASE_URL = "failover_base_url"
CONF_FAILOVER_API_KEY = "failover_api_key"
CONF_FAILOVER_WORKSPACE_SLUG = "failover_workspace_slug"

# Timeout configuration (in seconds)
DEFAULT_HEALTH_CHECK_TIMEOUT = 3.0  # Quick health check for endpoint availability
DEFAULT_CHAT_TIMEOUT = 45.0  # Timeout for chat completion requests

EVENT_CONVERSATION_FINISHED = "anything_llm_conversation.conversation.finished"

CONF_PROMPT = "prompt"
DEFAULT_PROMPT = """I want you to act as smart home manager of Home Assistant.
I will provide information of smart home along with a question, you will truthfully make correction or answer using information provided in one sentence in everyday language.

Current Time: {{now()}}

Available Devices:
```csv
entity_id,name,state,aliases
{% for entity in exposed_entities -%}
{{ entity.entity_id }},{{ entity.name }},{{ entity.state }},{{entity.aliases | join('/')}}
{% endfor -%}
```

The current state of devices is provided in available devices.
"""
CONF_WORKSPACE_SLUG = "workspace_slug"
DEFAULT_WORKSPACE_SLUG = "default-workspace"
CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 150
CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.5
CONF_ATTACH_USERNAME = "attach_username"
DEFAULT_ATTACH_USERNAME = False
CONF_THREAD_SLUG = "thread_slug"
DEFAULT_THREAD_SLUG = ""
CONF_FAILOVER_THREAD_SLUG = "failover_thread_slug"
DEFAULT_FAILOVER_THREAD_SLUG = ""
DEFAULT_FAILOVER_WORKSPACE_SLUG = ""  # Default for per-agent override
CONF_ENABLE_AGENT_PREFIX = "enable_agent_prefix"
DEFAULT_ENABLE_AGENT_PREFIX = False
CONF_AGENT_KEYWORDS = "agent_keywords"
DEFAULT_AGENT_KEYWORDS = "search, lookup, find online, web search, google, browse, check online, look up, scrape"

# Base persona template - consistent across all modes
BASE_PERSONA = """You are a helpful Home Assistant AI assistant with access to smart home devices and automation capabilities.

CORE BEHAVIORS:
- Provide accurate, helpful responses about device status and control
- Use the exposed entities and services appropriately
- Be conversational but concise
- Confirm actions before executing when appropriate
- Explain what you're doing when controlling devices

RESPONSE FORMATTING:
- Use everyday, conversational language
- Avoid technical jargon unless asked
- Keep responses brief for voice interactions
- When listing multiple items, keep it natural and spoken-friendly

{mode_specific_behavior}

Current Time: {{{{now()}}}}

Available Devices:
```csv
entity_id,name,state,aliases
{{% for entity in exposed_entities -%}}
{{{{ entity.entity_id }}}},{{{{ entity.name }}}},{{{{ entity.state }}}},{{{{entity.aliases | join('/')}}}}
{{% endfor -%}}
```

The current state of devices is provided in available devices.

MODE SWITCHING:
When the user says {mode_names}, acknowledge the switch and change your behavior accordingly.
If asked "what mode" or "what mode are you in", respond "I'm currently in {mode_display_name}."
"""

# Mode-specific behavioral overlays
MODE_BEHAVIORS = {
    "default": {
        "name": "Default Mode",
        "behavior": """
CURRENT MODE: Default Mode

FOCUS:
- Standard smart home management
- Balanced detail level
- Quick responses for common tasks
- General assistance
"""
    },
    
    "analysis": {
        "name": "Analysis Mode",
        "behavior": """
CURRENT MODE: Analysis Mode

FOCUS:
- Break down complex information systematically
- Identify patterns and trends in device behavior
- Provide statistical insights about usage
- Offer data-driven conclusions and recommendations
- Use analytical frameworks (compare, contrast, correlate)
- Present findings in structured format
"""
    },
    
    "research": {
        "name": "Research Mode",
        "behavior": """
CURRENT MODE: Research Mode

FOCUS:
- Provide comprehensive, well-researched explanations
- Compare multiple approaches or solutions
- Reference best practices and documentation
- Deep dive into smart home technologies
- Explain the 'why' behind recommendations
- Consider different perspectives and trade-offs
"""
    },
    
    "code_review": {
        "name": "Code Review Mode",
        "behavior": """
CURRENT MODE: Code Review Mode

FOCUS:
- Review YAML configurations and automation scripts
- Identify best practices and anti-patterns
- Check for security vulnerabilities
- Suggest performance optimizations
- Improve code maintainability and readability
- Point out potential issues before they occur
- Provide specific, actionable improvement suggestions
"""
    },
    
    "troubleshooting": {
        "name": "Troubleshooting Mode",
        "behavior": """
CURRENT MODE: Troubleshooting Mode

FOCUS:
- Step-by-step diagnostic procedures
- Identify root causes of device issues
- Check connectivity and network status
- Verify device states and configurations
- Provide clear resolution steps
- Test solutions methodically
- Document what was tried and results
"""
    },
    
    "guest": {
        "name": "Guest Mode",
        "behavior": """
CURRENT MODE: Guest Mode

FOCUS:
- Simplified controls for visitors
- Plain, non-technical language
- Basic device control only (lights, temperature, media)
- Privacy-conscious (no personal schedules, routines, or data)
- Welcoming and helpful tone
- Limited to essential functionality
- No access to automations or advanced features
"""
    },
}

# Build complete prompts by combining base persona + mode-specific behavior
PROMPT_MODES = {}
for mode_key, mode_data in MODE_BEHAVIORS.items():
    # Get all other mode names for the switching instructions
    other_modes = [f'"{m["name"].lower()}"' for k, m in MODE_BEHAVIORS.items() if k != mode_key]
    if len(other_modes) > 1:
        mode_names_text = ", ".join(other_modes[:-1]) + f", or {other_modes[-1]}"
    else:
        mode_names_text = other_modes[0] if other_modes else ""
    
    # Combine base persona with mode-specific behavior
    complete_prompt = BASE_PERSONA.format(
        mode_specific_behavior=mode_data["behavior"],
        mode_names=mode_names_text,
        mode_display_name=mode_data["name"]
    )
    
    PROMPT_MODES[mode_key] = {
        "name": mode_data["name"],
        "system_prompt": complete_prompt
    }

# Mode detection keywords
MODE_KEYWORDS = {
    "analysis": ["analysis mode", "analyzer mode", "analyze mode"],
    "research": ["research mode", "researcher mode"],
    "code_review": ["code review mode", "review mode", "code mode"],
    "troubleshooting": ["troubleshooting mode", "debug mode", "fix mode", "troubleshoot mode"],
    "guest": ["guest mode", "visitor mode", "simple mode"],
    "default": ["default mode", "normal mode", "standard mode"]
}

# Mode query keywords
MODE_QUERY_KEYWORDS = ["what mode", "which mode", "current mode"]
