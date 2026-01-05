# AnythingLLM Conversation


This is a custom component for Home Assistant that integrates with AnythingLLM to provide voice assistant functionality with RAG (Retrieval-Augmented Generation) capabilities.


## Overview


AnythingLLM Conversation allows you to use AnythingLLM as the conversation agent in Home Assistant's voice assistant pipeline. This integration leverages AnythingLLM's workspace feature to access your custom knowledge base, enable agents, and provide context-aware responses.


## Key Features

- **Voice Assistant Integration**: Seamlessly integrates with Home Assistant's voice assistant pipeline
- **Endpoint Failover**: Automatically fails over to a backup AnythingLLM server if the primary endpoint becomes unavailable
- **Workspace-Based Context**: Uses AnythingLLM workspace and threads to ensure proper context for your queries
- **RAG-Powered Responses**: Utilizes AnythingLLM workspaces to provide responses based on your custom knowledge base
- **Enable Agents**: Utilizes AnythingLLM workspaces to use agents to perform web searches, scrape websites, connect to SQL, etc.
- **Use MCP Servers**: Enables MCP Servers through AnythingLLM workspaces to expose additional api based tools


## How It Works


This integration connects to AnythingLLM via its API endpoint and uses workspace slugs to route requests to the appropriate workspace. The workspace slug you configure determines which AnythingLLM workspace your voice commands will interact with, ensuring access to the relevant knowledge base. Optional STT sanitizing toggles clean up responses before they complete voice pipeline, and keyword-enabled agent activation allows you to use features like web search and scraping through your workspace.


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


### Failover Configuration (Optional)
- **Failover API Key**: API key for the backup AnythingLLM server
- **Failover Base URL**: Base URL of the backup AnythingLLM instance
- **Failover Workspace Slug**: Workspace slug to use on the failover server (defaults to primary if not specified)


## Configuration Options


After adding the integration, you can configure each conversation agent with the following options:


- **Prompt Template**: Customize the system prompt for the conversation agent
- **Maximum Tokens**: Maximum number of tokens in the response
- **Temperature**: Controls randomness in responses (0.0 = deterministic, 1.0 = creative)
- **Attach Username**: Prepends the Home Assistant username to each message
- **Workspace Slug**: The workspace slug to use (defaults to the main integration's workspace) - workspace name lowercased and seperated by dashes
- **Thread Slug**: Optional AnythingLLM thread slug to use a specific conversation thread on the primary endpoint - right click on thread and select copy link, paste into notepad and get thread slug from url
- **Failover Workspace Slug**: Optional workspace slug for the failover endpoint (defaults to integration's failover workspace if not set)
- **Failover Thread Slug**: Optional AnythingLLM thread slug to use a specific conversation thread on the failover endpoint
- **Enable Agent Prefix**: Enables automatic `@agent` prefix for web searches and scraping
- **Agent Keywords**: Comma-separated keywords that trigger the `@agent` prefix (e.g., "search, lookup, find online")


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
3. Enter a **Thread Slug** for the primary endpoint (e.g., "home-assistant-main", "kitchen-assistant", etc.)
4. Optionally, enter a **Failover Thread Slug** for the failover endpoint if you want to use a different thread when failing over


**How thread slugs work:**
- **Blank/Empty** (default): Uses the workspace's default thread via `/v1/workspace/{slug}/chat`
- **Custom Slug** (e.g., "kitchen-thread"): Uses specific thread via `/v1/workspace/{slug}/thread/{thread-slug}/chat`
- Thread slugs are identifiers that correspond to threads you create in AnythingLLM
- You can find thread slugs in your AnythingLLM instance (check the thread URL or use browser DevTools to inspect API calls)
- When you specify a thread slug, the integration routes messages to that specific conversation thread


**Endpoint-specific thread behavior:**
- **Primary endpoint**: Uses the **Thread Slug** value
- **Failover endpoint**: Uses the **Failover Thread Slug** value (if configured), or the failover workspace's default thread (if left blank)
- Each endpoint maintains its own separate thread context - thread slugs are NOT shared between primary and failover


You can change or clear thread slugs at any time to switch between threads or return to the default workspace thread.


## Reconfiguring the Integration


You can modify the integration settings at any time:


### Reconfigure Main Integration Settings


To change API keys, base URLs, or workspace slugs:


1. Go to Settings > Devices & Services > AnythingLLM Conversation
2. Click the **three dots menu** on the integration card
3. Select **Reconfigure**
4. Update any of the following:
  - Primary API Key
  - Primary Base URL
  - Primary Workspace Slug
  - Failover API Key
  - Failover Base URL
  - Failover Workspace Slug


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
  - Failover Workspace Slug
  - Failover Thread Slug
  - Enable Agent Prefix
  - Agent Keywords


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


## Failover Functionality


The integration includes built-in endpoint monitoring and automatic failover:


1. **At conversation time** (when you send a message), the integration checks if the primary endpoint is responding
2. If the primary endpoint is unavailable, it automatically switches to the failover endpoint
3. The failover request includes automatic retry logic (up to 2 attempts with exponential backoff)
4. If the failover fails, it tries the primary endpoint one more time before giving up
5. When the primary endpoint comes back online, it automatically switches back
6. All endpoint switches are logged for monitoring


This ensures uninterrupted voice assistant functionality even if one AnythingLLM server goes offline.


**Note**: Health checks occur at conversation time, not during installation. This allows you to install the integration even when your AnythingLLM servers are temporarily offline.


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


### Failover Not Working


- Verify both endpoints are properly configured
- Check that both API keys are valid
- Monitor Home Assistant logs to see failover attempts


## Differences from Extended OpenAI Conversation


This integration is specifically designed for AnythingLLM and includes:


- Native AnythingLLM API support (not OpenAI-compatible)
- Endpoint health monitoring with automatic failover to backup server
- Retry logic with exponential backoff for improved reliability
- Workspace-based RAG integration
- Simplified configuration focused on AnythingLLM features
- TTS response cleaning (removes `<think>` tags before text-to-speech)
- **Zero external dependencies** - no pip packages required


Function calling and advanced automation features from the original Extended OpenAI Conversation have been removed, as AnythingLLM handles knowledge retrieval through its built-in RAG system.


## Response Cleaning for TTS


The integration automatically cleans LLM responses before sending them to text-to-speech. You can modify the `_clean_response_for_tts()` method in `conversation.py` to enable different cleaning options:


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
