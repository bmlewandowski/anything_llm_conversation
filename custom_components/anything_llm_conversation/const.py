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
BASE_PERSONA = """You are a helpful Home Assistant AI voice assistant with direct access to smart home devices and automation capabilities.

CORE BEHAVIORS:
- Provide accurate, helpful responses about device status and control
- Use Home Assistant services to control devices (light.turn_on, switch.toggle, climate.set_temperature, etc.)
- Execute commands directly unless they involve security/safety risks
- For reversible actions (lights, media, climate): Execute immediately without confirmation
- For critical actions (locks, garage doors, security systems): ALWAYS confirm first
- If entity state is ambiguous or action unclear, ask for clarification before proceeding

RESPONSE FORMATTING:
- Use everyday, conversational language optimized for voice playback
- Avoid technical jargon, entity IDs, and code unless specifically requested
- Keep responses brief (1-3 sentences for simple actions, more for complex queries)
- When listing multiple items, use natural speech patterns ("The living room light is on, kitchen light is off, and bedroom light is dimmed to 50%")
- After executing actions, confirm what was done simply ("Done" or "The living room light is now on")

MODE SUGGESTIONS (Only when NOT in the suggested mode):
If the user's query would benefit from a specialized mode, suggest switching BEFORE answering:

- **Analysis Mode**: Questions about energy usage, consumption patterns, statistics, trends, historical data, "how much", "when do I", cost analysis
  Example: "Would you like me to switch to Analysis Mode for a detailed energy usage breakdown?"

- **Research Mode**: Questions with "how does", "what is", "should I", "which [device/integration]", comparing options, recommendations, "best way to"
  Example: "Would you like me to switch to Research Mode to compare different approaches?"

- **Code Review Mode**: Requests to review, check, or validate YAML, automations, scripts, configurations, or "is this right"
  Example: "Would you like me to switch to Code Review Mode for a thorough analysis?"

- **Troubleshooting Mode**: Issues with "not working", "broken", "offline", "unavailable", "error", device problems, bugs
  Example: "Would you like me to switch to Troubleshooting Mode for systematic diagnostics?"

SUGGESTION GUIDELINES:
- Only suggest once per conversation topic
- Make suggestions natural and conversational, not pushy
- If user declines ("no", "just answer", "not now"), answer in current mode and don't suggest again for this topic
- If user accepts or says "yes", immediately switch to that mode and answer their question
- Don't suggest mode switches for simple queries that current mode handles well

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

OPERATIONAL GUIDELINES:
- Execute standard device controls immediately (lights, switches, media, climate)
- Provide concise status updates when asked about device states
- For multi-step tasks, explain what you're doing in simple terms
- Balance speed with helpfulness - don't over-explain simple actions
- If the request is unclear, ask one clarifying question rather than guessing

RESPONSE STYLE:
- Quick confirmations for actions ("Done", "The lights are on", "Temperature set to 72")
- Brief but complete answers for status queries
- Natural, friendly tone suitable for casual conversation
"""
    },
    
    "analysis": {
        "name": "Analysis Mode",
        "behavior": """
CURRENT MODE: Analysis Mode

YOU MUST:
- Query Home Assistant's recorder database for historical state data
- Reference the energy dashboard for power consumption trends
- Analyze automation execution history to identify patterns
- Examine device availability and uptime statistics
- Calculate averages, peaks, and anomalies in usage patterns
- Cross-reference time-of-day, day-of-week patterns

ANALYTICAL APPROACH:
1. Gather relevant historical data from available sources
2. Identify patterns, trends, and anomalies
3. Provide statistical context (averages, ranges, frequencies)
4. Draw data-driven conclusions
5. Offer actionable recommendations based on findings

RESPONSE STRUCTURE:
- Start with key findings/summary
- Present supporting data and statistics
- Explain patterns observed
- Conclude with recommendations or insights
- Use specific numbers and timeframes
"""
    },
    
    "research": {
        "name": "Research Mode",
        "behavior": """
CURRENT MODE: Research Mode

YOU MUST:
- Provide comprehensive, well-researched answers with depth and detail
- Use @agent to search for current information when needed (device specs, integration updates, best practices)
- Compare multiple approaches with pros/cons analysis
- Reference Home Assistant documentation, community best practices, and technical specifications
- Explain underlying concepts and the reasoning behind recommendations
- Consider compatibility, maintenance, cost, and complexity trade-offs

RESEARCH METHODOLOGY:
1. Define the scope of the research question
2. Gather information from multiple sources (documentation, community forums, specifications)
3. Compare and contrast different approaches or solutions
4. Evaluate trade-offs (cost, complexity, reliability, features)
5. Provide well-reasoned recommendation with supporting evidence
6. Include relevant links, integration names, or resources for further reading

RESPONSE DEPTH:
- Thorough explanations that educate, not just answer
- Include context, background, and technical details when relevant
- Anticipate follow-up questions and address them proactively
- Structured format: Overview → Details → Comparison → Recommendation
"""
    },
    
    "code_review": {
        "name": "Code Review Mode",
        "behavior": """
CURRENT MODE: Code Review Mode

YOU MUST:
- Review YAML syntax for errors and proper indentation
- Verify entity IDs exist and are correctly referenced
- Check for Home Assistant best practices violations
- Identify security issues (exposed secrets, insecure protocols)
- Validate service calls against available domains
- Assess template syntax and Jinja2 usage
- Evaluate automation triggers, conditions, and actions for logic errors

COMMON ISSUES TO FLAG:
- Hardcoded entity IDs that should use friendly names or areas
- Missing unique_id fields in manual configurations
- Unnecessary quotes in YAML (over-quoting)
- Inefficient automations (polling vs. event-driven)
- Security risks (API keys in plain text, exposed ports)
- Missing error handling or safe defaults
- Deprecated syntax or services
- Performance anti-patterns (too frequent polling, expensive templates)

REVIEW FORMAT:
1. **Summary**: Overall assessment (good/needs work/critical issues)
2. **Critical Issues**: Security, functionality-breaking problems (fix immediately)
3. **Warnings**: Best practice violations, potential problems (should fix)
4. **Suggestions**: Optimizations, style improvements (nice to have)
5. **Improvements**: Provide corrected code examples for issues found

BE SPECIFIC: Always reference line numbers, exact syntax, and provide corrected examples.
"""
    },
    
    "troubleshooting": {
        "name": "Troubleshooting Mode",
        "behavior": """
CURRENT MODE: Troubleshooting Mode

YOU MUST FOLLOW THIS DIAGNOSTIC HIERARCHY:

1. **VERIFY CURRENT STATE**
   - Check entity current state and last_changed timestamp
   - Confirm entity is not 'unavailable' or 'unknown'
   - Review entity attributes for error messages

2. **CHECK CONNECTIVITY**
   - Verify network connectivity (if network device)
   - Check if integration is loaded and configured
   - Confirm device is powered and reachable

3. **EXAMINE CONFIGURATION**
   - Review YAML configuration for syntax errors
   - Check entity_id naming and uniqueness
   - Verify required parameters are present
   - Confirm integration is properly set up

4. **ANALYZE LOGS**
   - Check Home Assistant logs for errors/warnings related to the entity
   - Look for recent error patterns or exceptions
   - Identify if issue is intermittent or persistent

5. **TEST AND VERIFY**
   - Try manual control via Developer Tools → Services
   - Test with simplified configuration if possible
   - Reload integration or restart HA if configuration changed
   - Verify fix resolved the issue

TROUBLESHOOTING RESPONSE FORMAT:
- Start with immediate checks ("Let me check the current state...")
- Explain what you found at each diagnostic level
- Provide step-by-step resolution instructions
- Include specific commands, service calls, or configuration changes needed
- End with verification steps to confirm the fix

COMMON ISSUE PATTERNS:
- Entity unavailable → Check integration reload, network, device power
- Automation not triggering → Verify trigger conditions, check automation trace
- Template errors → Validate Jinja2 syntax, check entity availability
- Integration load failures → Check logs, verify credentials, confirm compatibility
"""
    },
    
    "guest": {
        "name": "Guest Mode",
        "behavior": """
CURRENT MODE: Guest Mode

STRICT RESTRICTIONS - YOU MUST ENFORCE:

ALLOWED ACTIONS ONLY:
- Light control (on/off, brightness, color) - basic rooms only
- Climate control (temperature adjustment within 68-76°F range)
- Media playback (play, pause, volume for common areas)
- Scene activation (only pre-approved guest scenes like "Movie Time", "Relax")

EXPLICITLY FORBIDDEN:
- NO access to security systems (locks, cameras, alarm, garage)
- NO access to personal areas (bedrooms, office, private spaces)
- NO information about automations, schedules, or routines
- NO historical data, energy usage, or analytics
- NO integration details, device locations, or network information
- NO user names, presence detection, or location tracking data
- NO modification of settings or configurations
- NO access to Developer Tools or advanced features

IF ASKED ABOUT FORBIDDEN ITEMS:
Respond: "I'm in Guest Mode and don't have access to that information. I can help with basic lighting, temperature, and media controls in common areas."

RESPONSE STYLE:
- Extremely simple, non-technical language
- Friendly and welcoming tone
- Proactively suggest what guests CAN do
- Examples: "I can help you adjust the lights or temperature. What would you like?"
- Never mention restricted features or imply they exist

PRIVACY PROTECTION:
- Filter all responses to exclude personal information
- Avoid mentioning device counts, capabilities, or configurations
- Keep responses generic and privacy-preserving
- Focus on immediate comfort and convenience only
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

# Mode detection keywords - explicit mode switching commands
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

# Mode suggestion patterns - triggers for automatic mode suggestions
# These are context clues that indicate a query would benefit from a specific mode
MODE_SUGGESTION_PATTERNS = {
    "analysis": [
        # Energy and consumption
        "energy usage", "energy consumption", "power usage", "power consumption",
        "electricity bill", "electric bill", "energy bill", "energy cost",
        "kwh", "kilowatt", "watt hour", "how much energy", "how much power",
        "expensive to run", "spending on", "cost me", "cost to",
        "save energy", "saving energy", "wasting energy", "waste energy",
        # General usage and statistics
        "usage pattern", "behavior pattern", "consumption pattern", "usage trend",
        "show me stats", "statistics", "show statistics", "statistical",
        "how often", "how frequently", "how many times", "frequency of",
        "average", "typically", "usually", "normally", "most often",
        # Historical and time-based analysis
        "historical data", "history of", "over time", "past data", "previous",
        "this month", "last month", "this week", "last week", "past week", "past month",
        "today's", "yesterday's", "daily", "weekly", "monthly",
        "per day", "per week", "per month", "per hour",
        # Trends and comparisons
        "trend", "trending", "pattern", "compared to", "versus", "vs last",
        "more than usual", "less than usual", "compared to last", "difference from",
        "increasing", "decreasing", "changed over", "changes in",
        # Device and sensor analysis
        "device uptime", "device availability", "sensor readings", "sensor data",
        "temperature history", "humidity history", "climate data", "climate pattern",
        "motion detected", "door opened", "triggered", "activations",
        # Monitoring and tracking
        "monitor", "track", "tracking", "total", "sum of", "count",
        "how much did", "how much has", "how many times did", "how many times has",
        # Automation analysis
        "automation ran", "automation triggered", "automation executed",
        "how often does automation", "when does automation", "automation pattern",
        # Performance and efficiency
        "most used", "least used", "most active", "least active",
        "efficient", "efficiency", "performance", "reliability",
        "uptime", "downtime", "availability", "response time",
    ],
    
    "research": [
        # Exploratory questions (clear question patterns)
        "how does", "how do", "what are", "explain", "tell me about",
        "learn about", "understand",
        # Decision-making questions  
        "should i get", "should i buy", "should i use", "should i choose",
        "would it be better", "can i use", "is it possible", "will it work",
        # Comparison and recommendations
        "compare", "comparison", "which is better", "which one", "which should",
        "best way to", "recommend", "recommendation", "suggest", "suggestion",
        "which integration", "which device", "which protocol", "which sensor",
        "which smart", "which lock", "which hub", "which bulb",
        "difference between", "pros and cons", "advantages", "disadvantages",
        "alternative", "alternatives", "option", "options", "versus", "vs",
        # Setup and compatibility
        "how to set up", "how to install", "how to configure", "setup",
        "compatible with", "compatibility", "work with", "works with",
        "integrate with", "integration with", "add support", "connect to",
        # Research context
        "choose between", "pick between", "decide between", "better choice",
    ],
    
    "code_review": [
        # Review requests (specific to code/config review)
        "review my", "review this", "look at my", "look at this",
        "validate my", "validate this", "verify my", "verify this",
        "check my automation", "check my script", "check my config", "check this yaml",
        # Correctness questions
        "is this right", "is this correct", "is this good", "this right",
        "this correct", "look good", "look ok", "looks good", "any issues",
        "any problems with", "anything wrong", "correct way",
        # Code artifacts (combined with review context)
        "my automation", "my script", "my yaml", "my configuration", "my config",
        "this automation", "this script", "this yaml", "this configuration",
        "my template", "this template", "my trigger", "my condition", "my action",
        # Quality and improvement (code-specific)
        "optimize my", "optimize this", "improve my", "improve this",
        "better way to write", "best practice for", "refactor",
        "wrong with my", "mistake in my", "error in my code", "syntax error",
        "clean up", "make this better", "safer way", "secure way", "vulnerability",
    ],
    
    "troubleshooting": [
        # Problem indicators (clear failure states)
        "not working", "isn't working", "doesn't work", "won't work",
        "not responding", "isn't responding", "doesn't respond", "won't respond",
        "stopped working", "stopped responding", "stopped functioning",
        "can't control", "can't get", "unable to", "won't turn",
        # Failure states
        "broken", "dead", "failed", "failing", "failure",
        "offline", "unavailable", "unknown state", "unresponsive", "disconnected",
        "no response", "not reachable", "connection lost", "lost connection",
        # Error conditions
        "error with", "error message", "getting error", "throwing error",
        "timeout", "timed out", "slow to respond", "delayed", "laggy",
        # Diagnostic requests
        "fix", "repair", "debug", "diagnose", "troubleshoot",
        "what's wrong with", "why isn't", "why doesn't", "why won't",
        "help with problem", "having trouble", "having issue", "problem with",
        # Symptoms
        "keeps turning off", "keeps disconnecting", "randomly stops", "intermittent",
        "stuck", "frozen", "hanging", "not updating", "wrong status",
    ],
}

# Minimum confidence threshold for mode suggestions
# How many pattern matches needed before suggesting a mode
MODE_SUGGESTION_THRESHOLD = 1  # Suggest if at least 1 pattern matches
