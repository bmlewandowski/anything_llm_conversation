# Voice-Triggered Mode Switching

This integration now supports voice-triggered mode switching to customize the AI assistant's behavior for different use cases.

## Available Modes

### 1. Default Mode
Standard smart home management mode. Provides concise, everyday language responses for device control and status queries.

**Trigger phrases:**
- "default mode"
- "normal mode"
- "standard mode"

### 2. Analysis Mode
Expert data analyst mode that systematically analyzes your Home Assistant data using historical records, sensor readings, automation logs, and device statistics.

**Trigger phrases:**
- "analysis mode"
- "analyzer mode"
- "analyze mode"

**What it does:**
- Queries Home Assistant's recorder database for historical state data
- Analyzes device behavior patterns, uptime, and availability
- Tracks sensor readings over time (temperature, humidity, motion, etc.)
- Monitors automation execution history and trigger frequencies
- Calculates averages, peaks, trends, and anomalies
- Provides statistical context with specific numbers and timeframes

**Best for:**
- Energy usage analysis and cost tracking
- Device performance and reliability statistics
- Sensor data trends (climate, motion, door/window activity)
- Automation execution patterns ("how often does...", "when does...")
- Usage statistics ("how much", "how often", "most used")
- Time-based pattern analysis (daily, weekly, monthly)
- Comparative analysis ("more than usual", "compared to last week")
- Data-driven recommendations

### 3. Research Mode
Comprehensive research assistant that provides well-researched, in-depth explanations with pros/cons analysis and technical background.

**Trigger phrases:**
- "research mode"
- "researcher mode"

**What it does:**
- Uses @agent to search for current device specs and integration updates
- Compares multiple approaches with detailed pros/cons analysis
- References Home Assistant documentation and community best practices
- Explains underlying concepts and reasoning behind recommendations
- Evaluates trade-offs (cost, complexity, reliability, features)
- Provides educational context, not just answers

**Best for:**
- "How does" and "what is" questions
- Comparing devices or integration options
- "Should I" and "which is better" decisions
- Learning about setup, installation, and configuration
- Understanding compatibility and technical specifications

### 4. Code Review Mode
Senior Home Assistant expert that performs systematic code reviews with security checks, best practice validation, and specific improvement recommendations.

**Trigger phrases:**
- "code review mode"
- "review mode"
- "code mode"

**What it does:**
- Reviews YAML syntax for errors and proper indentation
- Verifies entity IDs exist and are correctly referenced
- Identifies security issues (exposed secrets, insecure protocols)
- Validates service calls and template syntax (Jinja2)
- Flags common anti-patterns and inefficiencies
- Provides corrected code examples with line-specific feedback

**Review structure:**
1. **Summary** - Overall assessment
2. **Critical Issues** - Security and functionality problems (fix immediately)
3. **Warnings** - Best practice violations (should fix)
4. **Suggestions** - Optimizations and improvements (nice to have)
5. **Improvements** - Corrected code examples

**Best for:**
- YAML configuration validation
- Automation and script review
- Security audits and vulnerability checks
- Performance optimization
- "Is this right?" validation questions

### 5. Troubleshooting Mode
Technical support specialist that follows a systematic 5-step diagnostic hierarchy to identify and resolve device and integration issues.

**Trigger phrases:**
- "troubleshooting mode"
- "debug mode"
- "fix mode"
- "troubleshoot mode"

**What it does:**
Follows this diagnostic hierarchy:

1. **Verify Current State** - Check entity state, timestamps, error attributes
2. **Check Connectivity** - Network status, integration loaded, device reachable
3. **Examine Configuration** - YAML syntax, entity naming, required parameters
4. **Analyze Logs** - Home Assistant error logs and patterns
5. **Test and Verify** - Manual control tests, configuration reload, fix verification

**Response format:**
- Immediate status check results
- Step-by-step diagnostic findings
- Specific commands and service calls needed
- Configuration changes with examples
- Verification steps to confirm resolution

**Best for:**
- "Not working" or "broken" devices
- Offline, unavailable, or unresponsive entities
- Automation not triggering issues
- Template errors and integration failures
- "Why isn't" and "what's wrong" questions

### 6. Guest Mode
Simplified, privacy-conscious mode with strict access restrictions and enforced security boundaries for visitors.

**Trigger phrases:**
- "guest mode"
- "visitor mode"
- "simple mode"

**What guests CAN do:**
- Control lights (on/off, brightness, color) in common areas
- Adjust temperature (limited to 68-76°F range)
- Control media playback (play, pause, volume)
- Activate pre-approved scenes ("Movie Time", "Relax")

**What is FORBIDDEN:**
- ❌ Security systems (locks, cameras, alarm, garage)
- ❌ Personal areas (bedrooms, office, private spaces)
- ❌ Automation schedules or routines
- ❌ Historical data, energy usage, analytics
- ❌ Integration details or network information
- ❌ User names or presence detection
- ❌ Settings or configuration changes
- ❌ Developer Tools access

**Privacy enforcement:**
- All responses filtered to exclude personal information
- Device counts and capabilities hidden
- No mention of restricted features
- Simple, welcoming language only

**Best for:**
- Temporary visitor access
- Privacy-conscious guest control
- Limited, essential functionality
- Non-technical family members or friends

## Automatic Mode Suggestions

The integration uses intelligent pattern detection to suggest mode switches when your query would benefit from specialized expertise. This combines programmatic keyword matching with AI decision-making for reliable, context-aware suggestions.

### How It Works

**Hybrid Approach:**
1. **Pattern Detection** - Analyzes your query for keywords that indicate a specialized mode would be helpful
2. **AI Evaluation** - The AI considers full context and decides whether to actually suggest the mode
3. **Natural Suggestions** - Offers to switch modes conversationally, never forcing

### Example Scenarios

**Energy Questions → Analysis Mode**
```
User: "Why is my energy bill so high?"
Assistant: "Would you like me to switch to Analysis Mode for a detailed energy usage breakdown?"
User: "Yes"
Assistant: "Switching to Analysis Mode. Let me analyze your energy consumption patterns..."
```

**Device Statistics → Analysis Mode**
```
User: "How often does my garage door open?"
Assistant: "Would you like me to switch to Analysis Mode for detailed statistics?"
User: "Yes"
Assistant: "Switching to Analysis Mode. Let me analyze your garage door usage patterns..."
```

**Device Questions → Research Mode**
```
User: "Should I get a Zigbee or Z-Wave smart lock?"
Assistant: "Would you like me to switch to Research Mode to compare different approaches?"
User: "Yes"
Assistant: "Switching to Research Mode. Let me research both protocols for you..."
```

**Configuration Questions → Code Review Mode**
```
User: "Is this automation YAML correct?"
Assistant: "Would you like me to switch to Code Review Mode for a thorough analysis?"
User: "Yes please"
Assistant: "Switching to Code Review Mode. Let me review your configuration..."
```

**Problem Reports → Troubleshooting Mode**
```
User: "My bedroom light isn't responding"
Assistant: "Would you like me to switch to Troubleshooting Mode for systematic diagnostics?"
User: "Yes"
Assistant: "Switching to Troubleshooting Mode. Let me check the current state..."
```

### Pattern Triggers

The system detects these patterns (you can view/customize in `MODE_SUGGESTION_PATTERNS`):

- **Analysis Mode**: statistics, trend, pattern, "how often", "how many times", historical data, sensor data, device uptime, automation triggered, most used, performance, "over time", "past week"
- **Research Mode**: "how does", "what is", "should I", compare, "which is better", recommend, "best way", compatibility, "pros and cons"
- **Code Review Mode**: "review my", "check this", validate, "my automation", "this yaml", "is this right", optimize, refactor, "better way to write"
- **Troubleshooting Mode**: "not working", "stopped working", broken, offline, unavailable, error, timeout, fix, debug, "why isn't", "connection lost"

### Suggestion Behavior

**The AI will:**
- Suggest switching when query patterns match and context is appropriate
- Only suggest once per conversation topic (not repeatedly)
- Skip suggestions for simple queries the current mode handles well
- Make suggestions natural and conversational, never pushy

**You can:**
- Accept: "Yes", "sure", "okay" → Immediately switches and answers
- Decline: "No", "just answer", "not now" → Answers in current mode, won't suggest again
- Ignore: The AI won't force the switch

### Tuning Suggestions

You can adjust sensitivity in [`mode_patterns.py`](custom_components/anything_llm_conversation/mode_patterns.py):
```python
MODE_SUGGESTION_THRESHOLD = 1  # Pattern matches needed to trigger hint
```

## Usage

### Switching Modes Manually

You can also explicitly switch modes anytime by saying the mode name:

```
User: "Switch to analysis mode"
Assistant: "Switching to Analysis Mode."

User: "What's my energy usage pattern?"
Assistant: [Provides detailed analytical response]
```

### Checking Current Mode

Ask about the current mode at any time:

```
User: "What mode are you in?"
Assistant: "I'm currently in Analysis Mode."
```

Or use variations:
- "which mode"
- "current mode"

## Technical Details

### Mode Detection
- Keyword-based detection from voice transcription
- Case-insensitive matching
- Works with natural language (e.g., "switch to analysis mode" or just "analysis mode")

### Mode Persistence
- Modes persist per conversation ID
- Switching modes clears conversation history for clean context
- Each conversation can have its own mode

### System Prompts
- Each mode has a specialized system prompt
- Prompts include mode-awareness for seamless switching
- Device information is available in all modes

## Example Scenarios

### Energy Analysis Workflow
```
1. "Analysis mode"
2. "What devices used the most energy this week?"
3. "Are there any unusual patterns?"
4. "Default mode" (when done analyzing)
```

### Automation Review Workflow
```
1. "Code review mode"
2. "Review my morning automation"
3. "Any security concerns?"
4. "How can I optimize this?"
5. "Normal mode"
```

### Research Workflow
```
1. "Research mode"
2. "Tell me about Zigbee vs Z-Wave"
3. "What are the pros and cons of each?"
4. "Which is better for my setup?"
5. "Default mode"
```

### Troubleshooting Workflow
```
1. "Troubleshooting mode"
2. "My bedroom light isn't responding"
3. "Walk me through fixing it"
4. [Follow diagnostic steps]
5. "Normal mode"
```

### Guest Access Workflow
```
1. "Guest mode"
2. "Turn on the living room lights"
3. "Make it warmer"
4. "Play some music"
5. [Admin returns] "Default mode"
```

## Customization

The mode system uses a modular design with a base persona template and mode-specific behavioral overlays. This ensures consistency across all modes while allowing specialized behaviors.

### Using a Custom Base Persona

You can customize the base persona while still benefiting from mode switching. Your custom prompt will be used as the foundation, with mode-specific behaviors layered on top.

**To use a custom base persona:**

1. Go to Settings > Devices & Services > AnythingLLM Conversation
2. Click **Configure** on your conversation agent
3. Edit the **Prompt Template** field

**Your custom prompt must include these placeholders:**

- `{mode_specific_behavior}` - Where mode behaviors will be inserted
- `{mode_names}` - List of available modes for switching instructions
- `{mode_display_name}` - The current mode's display name

**Example Custom Base Persona:**

```python
"""You are JARVIS, an advanced AI assistant managing Tony Stark's smart home with sophistication and wit.

PERSONALITY:
- Polite, articulate, and slightly British
- Anticipate needs before they're expressed
- Dry humor when appropriate
- Professional but personable

CORE CAPABILITIES:
- Monitor and control all home systems
- Provide insightful analysis and recommendations
- Explain actions clearly and concisely
- Prioritize safety and efficiency

{mode_specific_behavior}

VOICE RESPONSES:
- Keep responses natural and conversational
- Avoid jargon unless specifically requested
- When uncertain, ask for clarification rather than assume

Current Time: {{{{now()}}}}

Available Devices:
```csv
entity_id,name,state,aliases
{{% for entity in exposed_entities -%}}
{{{{ entity.entity_id }}}},{{{{ entity.name }}}},{{{{ entity.state }}}},{{{{entity.aliases | join('/')}}}}
{{% endfor -%}}
```

MODE SWITCHING:
When the user says {mode_names}, acknowledge the switch and adapt accordingly.
If asked "what mode" or "what mode are you in", respond "I'm currently in {mode_display_name}, sir."
"""
```

With this custom persona:
- Default behavior: JARVIS personality with general assistance
- "analysis mode": JARVIS with data analysis focus
- "troubleshooting mode": JARVIS with diagnostic expertise
- All modes maintain the JARVIS personality and tone

**Important Notes:**
- If you don't include the placeholders, modes won't inject their specialized behaviors
- The `{{{{now()}}}}` and entity loop syntax is for Home Assistant's template engine (use double braces)
- The `{mode_specific_behavior}` uses single braces (Python string formatting)

### Adding a New Mode

Edit the `MODE_BEHAVIORS` dictionary in [`modes.py`](custom_components/anything_llm_conversation/modes.py):

```python
MODE_BEHAVIORS = {
    "your_mode": {
        "name": "Your Mode Name",
        "behavior": """
CURRENT MODE: Your Mode Name

FOCUS:
- Define your mode's specific focus areas
- Add behavioral guidelines
- Specify expertise or approach
- List key objectives
"""
    }
}
```

The mode will automatically inherit:
- Base AI personality and tone (default or custom)
- Core smart home capabilities
- Device list and state information
- Mode switching instructions
- Consistent response formatting

Then add trigger keywords in [`mode_patterns.py`](custom_components/anything_llm_conversation/mode_patterns.py):

```python
MODE_KEYWORDS = {
    "your_mode": ["your mode", "custom mode", "alternate trigger"]
}
```

You can also add suggestion patterns to enable automatic mode suggestions:

```python
MODE_SUGGESTION_PATTERNS = {
    "your_mode": [
        "pattern that indicates", "this mode would help", "relevant keywords"
    ]
}
```

### Modifying the Default Base Persona

To change the default core personality for users who haven't customized their prompt, edit `BASE_PERSONA` in [`modes.py`](custom_components/anything_llm_conversation/modes.py):

```python
BASE_PERSONA = """You are a helpful Home Assistant AI assistant...
[Your custom base personality and guidelines]
"""
```

This affects all modes for users with the default prompt while preserving their specialized behaviors.

## File Structure Reference

After refactoring, mode-related code is organized as follows:

- **[`modes.py`](custom_components/anything_llm_conversation/modes.py)** - Mode definitions and behaviors
  - `BASE_PERSONA` - Base AI personality template
  - `MODE_BEHAVIORS` - Specialized behaviors for each mode
  - `PROMPT_MODES` - Compiled prompts combining base + mode behaviors

- **[`mode_patterns.py`](custom_components/anything_llm_conversation/mode_patterns.py)** - Pattern matching
  - `MODE_KEYWORDS` - Explicit mode switch triggers
  - `MODE_QUERY_KEYWORDS` - Mode query detection
  - `MODE_SUGGESTION_PATTERNS` - Automatic suggestion patterns
  - `MODE_SUGGESTION_THRESHOLD` - Sensitivity threshold

- **[`const.py`](custom_components/anything_llm_conversation/const.py)** - Configuration constants only
  - Domain settings, URLs, timeouts, default prompts

This separation makes it easier to:
- Add or modify modes without touching configuration
- Tune suggestion patterns independently
- Maintain clear code organization
