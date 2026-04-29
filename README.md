# AnythingLLM Conversation


This is a custom component for Home Assistant that integrates with AnythingLLM to provide voice assistant functionality with RAG (Retrieval-Augmented Generation) capabilities.


## Overview


AnythingLLM Conversation allows you to use AnythingLLM as the conversation agent in Home Assistant's voice assistant pipeline. This integration leverages AnythingLLM's workspace feature to access your custom knowledge base, enable agents, and provide context-aware responses.


## Key Features

- **Voice Assistant Integration**: Seamlessly integrates with Home Assistant's voice assistant pipeline
- **Voice-Triggered Workspace Switching**: Switch between AnythingLLM workspaces (Analysis, Research, Investigation, Security, Adventure, Visual) using voice commands
- **Automatic Mode Suggestions**: AI intelligently suggests switching to relevant workspaces based on your query patterns ("Would you like me to switch to Analysis Mode for a detailed energy breakdown?")
- **Workspace-Based Context**: Uses AnythingLLM workspace and threads to ensure proper context for your queries
- **RAG-Powered Responses**: Utilizes AnythingLLM workspaces to provide responses based on your custom knowledge base
- **Enable Agents**: Utilizes AnythingLLM workspaces to use agents to perform web searches, scrape websites, connect to SQL, etc.
- **Use MCP Servers**: Enables MCP Servers through AnythingLLM workspaces to expose additional api based tools
- **Connectivity Sensor**: Binary sensor reflects live health of your primary AnythingLLM endpoint for use in automations
- **Conversation History**: Messages are logged to the Home Assistant Assist panel so full conversation history is visible in the UI
- **State Persistence**: Active mode, workspace, and thread are stored in `.storage` and restored automatically after a Home Assistant reload


## How It Works


This integration connects to AnythingLLM via its API endpoint and uses workspace slugs to route requests to the appropriate workspace. The workspace slug you configure determines which AnythingLLM workspace your voice commands will interact with, ensuring access to the relevant knowledge base. Optional STT sanitizing toggles clean up responses before they complete voice pipeline, and keyword-enabled agent activation allows you to use features like web search and scraping through your workspace.


## Features

### Voice-Triggered Mode Switching

Customize your AI assistant's behavior for different use cases by simply saying the mode name. Available modes:

- **Default / JARVIS** - Standard smart home management
- **Analysis** - Data analysis, energy usage, and pattern identification
- **Research** - In-depth explanations, comparisons, and recommendations
- **Investigation** - Code review, troubleshooting, and diagnostics (also triggered by "code review mode", "troubleshooting mode", "debug mode")
- **Security** - Security system awareness and device access control
- **Adventure / Visual** - Specialized creative or visual workspaces

**Examples:**

*Manual Mode Switching:*
```
User: "Switch to analysis mode"
Assistant: "Switched to Analysis Mode. How can I help you?"
User: "What's my energy usage pattern?"
Assistant: [Provides detailed analytical response]
```

*Automatic Mode Suggestions:*
```
User: "Why is my energy bill so high?"
Assistant: "Would you like me to switch to Analysis Mode for a detailed energy usage breakdown?"
User: "Yes"
Assistant: "Switching to Analysis Mode. How can I help you?"
User: "Show me this month vs last month"
Assistant: [Provides detailed analytical response in Analysis Mode]
```

> **Note**: Replying with "yes", "sure", "ok", "go ahead", "absolutely", or similar to a mode suggestion is handled locally — no extra API call is made.

For complete documentation including all trigger phrases, use cases, and customization options, see [MODE_SWITCHING.md](MODE_SWITCHING.md).

### Dynamic Workspace Switching

Switch between different AnythingLLM workspaces on-the-fly during conversations to access different RAG sources, agents, and configurations.

**Voice Commands:**
```
User: "Switch to finance workspace"
Assistant: "Switched to workspace finance. How can I help you?"

User: "Use technical support workspace"
Assistant: "Switched to workspace technical-support. How can I help you?"

User: "Switch to default workspace"
Assistant: "Switched back to default workspace. How can I help you?"

User: "What workspace"
Assistant: "Currently using workspace: finance"
```

**Alternative Commands:**
- `!workspace <name>` - Traditional command format
- `switch to <name> workspace` - Natural voice command
- `use <name> workspace` - Alternative voice command
- `change workspace to <name>` - Another natural option
- `switch workspace to <name>` - Another alternative
- `what workspace` / `what workspace are you in` - Check active workspace
- `which workspace` / `current workspace` - Alternative queries

**Use Cases:**
- **Finance Workspace** - Access financial documents, budgets, and accounting data
- **Technical Support** - Switch to technical documentation and troubleshooting guides
- **Home Automation** - Use device manuals and automation examples
- **Personal Knowledge** - Access your personal notes and documents

**Features:**
- Conversation history is cleared when switching workspaces (fresh context)
- Each conversation can use a different workspace
- Workspace changes persist for the duration of the conversation
- Thread slug is automatically managed:
  - When switching to a non-default workspace: uses that workspace's default thread
  - When switching back to default workspace: restores your configured thread slug
- Works seamlessly with voice assistants

**Examples:**
```
User: "Switch to finance workspace"
Assistant: "Switched to workspace finance. How can I help you?"
User: "What were my Q4 expenses?"
Assistant: [Accesses finance workspace with Q4 budget documents]

User: "Use default workspace"
Assistant: "Switched back to default workspace. How can I help you?"
User: "Turn on the living room lights"
Assistant: [Back to your primary home automation workspace]
```


### Thread Reset Service


You can reset the active AnythingLLM thread for a conversation agent at any time using the `anything_llm_conversation.reset_thread` service. This clears the current thread context, causing the next message to start a fresh conversation.


**Service**: `anything_llm_conversation.reset_thread`

**Fields:**
- `config_entry` *(required)*: The config entry ID of the AnythingLLM integration to target
- `conversation_id` *(optional)*: Specific conversation ID to reset. If omitted, resets the thread for all active conversations on that entry

**Example:**
```yaml
service: anything_llm_conversation.reset_thread
data:
  config_entry: "<your_config_entry_id>"
```


## Installation


1. Install via HACS as a custom repository or by copying the `anything_llm_conversation` folder into `<config directory>/custom_components`
2. Restart Home Assistant
3. Go to Settings > Devices & Services
4. In the bottom right corner, select the Add Integration button
5. Search for "AnythingLLM Conversation" and follow the setup wizard


## Configuration


During setup, you'll be asked to provide:


### Primary Endpoint
- **Name**: A friendly name for the integration (e.g., "AnythingLLM")
- **API Key**: Your AnythingLLM API key (generated in AnythingLLM settings)
- **Base URL**: The base URL of your AnythingLLM instance (default: `http://localhost:3001/api`)
- **Workspace Slug**: The slug of the AnythingLLM workspace to use (e.g., "home-assistant-workspace")



## Configuration Options


After adding the integration, you can configure each conversation agent with the following options:


- **Prompt Template**: Customize the system prompt for the conversation agent
- **Maximum Tokens**: Maximum number of tokens in the response
- **Temperature**: Controls randomness in responses (0.0 = deterministic, 1.0 = creative)
- **Attach Username**: Prepends the Home Assistant username to each message
- **Workspace Slug**: The workspace slug to use (defaults to the main integration's workspace) - workspace name lowercased and seperated by dashes
- **Thread Slug**: Optional AnythingLLM thread slug for a specific conversation thread - right-click a thread in AnythingLLM and copy the link, then extract the slug from the URL
- **Enable Agent Prefix**: Enables automatic `@agent` prefix for web searches and scraping
- **Agent Keywords**: Comma-separated keywords that trigger the `@agent` prefix (e.g., "search, lookup, find online")

### Options Precedence and Retention
- Conversation agents read workspace/thread values from the agent options first; if unset, they fall back to the main integration settings.
- The options form now pre-fills saved values, so changes persist reliably across reloads.


### Agent Prefix for Web Searches

AnythingLLM supports the `@agent` prefix to trigger web searches and scraping capabilities. This integration can automatically add this prefix to user messages based on keyword detection:

1. **Enable the feature**: Turn on "Enable Agent Prefix" in the conversation agent configuration
2. **Configure keywords**: Customize the "Agent Keywords" field with comma-separated trigger words
3. **Default keywords**: "search, lookup, find online, web search, google, browse, check online, look up"

When enabled, any message containing one of the keywords will automatically have `@agent` prepended before being sent to AnythingLLM.

**Example:**
- User says: "search for the weather in Paris"
- Sent to AnythingLLM: "@agent search for the weather in Paris"
- AnythingLLM uses its web search agent to find current information


### Thread/Session Support


By default (when thread slugs are left blank), AnythingLLM uses the workspace's default thread for all conversations. If you want to use a different thread or separate conversations into multiple threads, you can specify thread slugs for each endpoint:


1. Go to Settings > Devices & Services > AnythingLLM Conversation
2. Click **Configure** on your conversation agent
3. Enter a **Thread Slug** (e.g., "home-assistant-main", "kitchen-assistant", etc.)


**How thread slugs work:**
- **Blank/Empty** (default): Uses the workspace's default thread via `/v1/workspace/{slug}/chat`
- **Custom Slug** (e.g., "kitchen-thread"): Uses a specific thread via `/v1/workspace/{slug}/thread/{thread-slug}/chat`
- Thread slugs correspond to threads you create in AnythingLLM
- You can find the thread slug in the AnythingLLM thread URL (right-click → Copy Link, then extract the slug)
- When you specify a thread slug, the integration routes all messages to that specific conversation thread

You can change or clear the thread slug at any time to switch threads or return to the workspace default.


### Adding Home Assistant Automation Custom Skill in AnythingLLM

1. Go to Community Hub on side menu
2. Import Home Assistant Automation
3. Click Agent Skills
4. Enter Home Assistant URL in homeAssistantUrl field
5. Enter API Key (officially called a Long-Lived Access Token) in homeAssistantApiKey field

**Steps to Generate Long-Lived Access Token**
1. Log in to your Home Assistant instance using a web browser with an administrator account.
2. Navigate to your Profile by clicking your user icon (or picture) in the bottom-left corner of the sidebar.
3. Go to the Security tab within your profile settings.
4. Scroll down to the Long-Lived Access Tokens section.
5. Click the "+ Create Token" button.
6. Enter a name for the token (e.g., "Automation Script" or "Hass Agent") to help you remember its purpose, and click Create.
7. Copy the generated token string immediately. For security reasons, you will not be able to view this token again after you close the window. 


## Reconfiguring the Integration


You can modify the integration settings at any time:


### Reconfigure Main Integration Settings


To change API keys, base URLs, or workspace slugs:


1. Go to Settings > Devices & Services > AnythingLLM Conversation
2. Click the **three dots menu** on the integration card
3. Select **Reconfigure**
4. Update any of the following:
  - API Key
  - Base URL
  - Workspace Slug
  - Health Check and Timeout settings


The integration will validate the connection and reload automatically after saving changes.


### Configure Conversation Agent Options


To change per-agent settings (prompt, tokens, temperature, etc.):


1. Go to Settings > Devices & Services > AnythingLLM Conversation
2. Click **Configure** on the specific conversation agent you want to modify
3. Update any of the following:
  - Prompt Template
  - Maximum Tokens
  - Temperature
  - Attach Username
  - Workspace Slug
  - Thread Slug
  - Enable Agent Prefix
  - Agent Keywords
  - Enable Health Check


## Setting Up Voice Assistant


1. Go to Settings > [Voice Assistants](https://my.home-assistant.io/redirect/voice_assistants/)
2. Click to edit your Assistant (named "Home Assistant" by default)
3. Select "AnythingLLM Conversation" from the "Conversation agent" dropdown


## AnythingLLM Setup


### Getting Your API Key


1. Open your AnythingLLM instance
2. Navigate to Settings > API Keys
3. Generate a new API key
4. Copy the key for use in Home Assistant


### Finding Your Workspace Slug


1. In AnythingLLM, open the workspace you want to use
2. The workspace slug is typically shown in the URL or workspace settings
3. It's usually a lowercase, hyphenated version of your workspace name
4. Example: "Home Assistant Knowledge" becomes "home-assistant-knowledge"


## Endpoint Health Monitoring


The integration includes a non-blocking background health monitor:


1. A background task checks the primary endpoint every **30 seconds** and caches the result
2. Voice requests never block waiting for a health check — the cached result is used immediately
3. If the endpoint is unavailable, requests fail fast with a clear error rather than timing out
4. Failed API calls are retried up to 2 times with exponential backoff before surfacing an error
5. When the endpoint comes back online, the background monitor detects it automatically
6. All health state changes are logged for monitoring


**Note**: The integration starts the background health monitor as soon as it loads, so voice commands are never delayed by health checks.


### Connectivity Sensor


When the integration loads, it creates a **binary sensor** that reflects the live health of your primary AnythingLLM endpoint:

- **Entity**: `binary_sensor.<name>_connectivity`
- **On (Connected)**: Primary endpoint responded to the last health check
- **Off (Disconnected)**: Primary endpoint is unreachable

You can use this sensor in automations to alert you when your AnythingLLM server goes offline or comes back online.


### Disabling Health Checks


If you're using only a single AnythingLLM endpoint without failover, you can disable health checks:


1. Navigate to **Settings** → **Devices & Services** → **AnythingLLM Conversation**
2. Click **Configure** on your integration
3. Uncheck **Enable health check**
4. Click **Submit**


When disabled, the integration skips background health monitoring and always uses the primary endpoint. Because health checks now run in the background (not at conversation time), disabling them has no meaningful effect on voice response latency — this option is mainly useful for reducing API polling when failover is not configured.


**Benefits of disabling health checks:**
- Reduced periodic API calls to your AnythingLLM server
- Simpler behavior when failover isn't configured


**Keep health checks enabled if:**
- You want the connectivity binary sensor to stay current
- You want fast-fail behavior when the server is temporarily unavailable


### Configurable Timeouts

You can now configure the following timeouts in the integration and agent options:

- **Health Check Timeout**: How long to wait for endpoint health checks (default: 3 seconds)
- **Chat Completion Timeout**: How long to wait for chat completion responses (default: 60 seconds)

To adjust these:
1. Go to **Settings** → **Devices & Services** → **AnythingLLM Conversation**
2. Click **Configure** on your integration or agent
3. Set your desired values for **Health Check Timeout** and **Chat Completion Timeout** (in seconds)
4. Click **Submit**

**Use Cases:**
- Lower the health check timeout to detect server downtime faster
- Increase chat completion timeout for longer, more complex responses
- Tune timeouts to match your server/network performance

These settings are used for all API calls and can be changed at any time for optimal performance.


## API Endpoint Structure


The integration uses the following AnythingLLM API endpoints:


- Health Check: `GET /v1/system`
- Chat Completion: `POST /v1/workspace/{workspace-slug}/chat`


## Troubleshooting


### Integration Won't Connect


- Verify your AnythingLLM instance is running and accessible
- Check that the Base URL is correct (include `/api` at the end)
- Ensure your API key is valid and has proper permissions
- Check Home Assistant logs for detailed error messages


### Voice Commands Not Working


- Verify the integration is selected as the conversation agent in Voice Assistant settings
- Check that your workspace slug is correct
- Ensure your AnythingLLM workspace has relevant knowledge for home automation



## Differences from Extended OpenAI Conversation


This integration is specifically designed for AnythingLLM and includes:


- Native AnythingLLM API support (not OpenAI-compatible)
- Background endpoint health monitoring with connectivity binary sensor
- Retry logic with exponential backoff for improved reliability
- Workspace-based RAG integration
- Simplified configuration focused on AnythingLLM features
- TTS response cleaning (removes `<think>` tags before text-to-speech)
- **Zero external dependencies** - no pip packages required


Function calling and advanced automation features from the original Extended OpenAI Conversation have been removed, as AnythingLLM handles knowledge retrieval through its built-in RAG system.


## Response Cleaning for TTS


The integration automatically cleans LLM responses before sending them to text-to-speech. You can modify `clean_response_for_tts()` in `response_processor.py` to enable different cleaning options:


### Basic Options (enabled by default)
- **Option 1**: Removes `<think>` tags and all content inside them
- **Option 3**: Removes asterisks used for markdown bold/italic formatting
- **Option 4**: Link conversion (`[text](url)` → "text") and whitespace normalization (active by default)


### Alternative Options (commented out, uncomment to enable)
- **Option 2**: Removes only the `<think>` tags but keeps the content inside (use instead of Option 1)
- **Option 4 - Additional markdown**:
 - Underscores (italic)
 - Tildes (strikethrough)
 - Backticks (code)
 - Hash symbols (headers)
 - Code blocks
 - Standalone URLs
- **Option 5 - HTML handling**:
 - HTML entity decoding (`&nbsp;` → space, `&amp;` → &, etc.)
 - Convert `<br>` tags to spaces
 - Remove all HTML tags
- **Option 6 - Emoji handling** (requires `emoji` package):
 - Remove emojis entirely, OR
 - Convert to text descriptions (😀 → "grinning face")
- **Option 7 - Special characters** (recommended for home automation):
 - Temperature symbols: `°` → "degrees"
 - Currency: `$` → "dollars", `€` → "euros", `£` → "pounds"
 - Percentages: `%` → "percent"
 - Smart temperature conversion: `25C` → "25 degrees Celsius", `77F` → "77 degrees Fahrenheit"


### Recommendations for Natural TTS
The most useful combinations for natural-sounding text-to-speech are:
- **Minimal** (default): Options 1 + 3 + basic Option 4 (link/whitespace)
- **Home Automation**: Add Option 7 for temperature and percentage handling
- **HTML Responses**: Enable Option 5 if AnythingLLM returns HTML-formatted content
- **Emoji Support**: Enable Option 6 if your LLM uses emojis (set to text descriptions for better TTS)
- **Aggressive**: Enable all markdown options from Option 4 to strip all formatting


This prevents the voice assistant from reading out unwanted formatting, URLs, HTML tags, or the LLM's internal reasoning process.


## Support


For issues, questions, or feature requests, please visit the [GitHub repository](https://github.com/bmlewandowski/anything_llm_conversation/issues).


## Credits


This integration is derived from [Extended OpenAI Conversation](https://github.com/jekalmin/extended_openai_conversation) by @jekalmin, adapted specifically for AnythingLLM integration.


## License


This project follows the same license as the original Extended OpenAI Conversation integration.
