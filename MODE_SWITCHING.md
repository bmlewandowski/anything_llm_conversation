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
Expert data analyst mode focused on breaking down complex information, identifying patterns, and providing statistical insights about your smart home.

**Trigger phrases:**
- "analysis mode"
- "analyzer mode"
- "analyze mode"

**Best for:**
- Energy usage analysis
- Device behavior patterns
- Trend identification
- Data-driven recommendations

### 3. Research Mode
Thorough research assistant mode for deep dives into smart home technologies, comparing approaches, and comprehensive explanations.

**Trigger phrases:**
- "research mode"
- "researcher mode"

**Best for:**
- Learning about new devices
- Comparing automation strategies
- Technical explanations
- Integration research

### 4. Code Review Mode
Senior Home Assistant expert mode for reviewing configurations, automations, and scripts.

**Trigger phrases:**
- "code review mode"
- "review mode"
- "code mode"

**Best for:**
- YAML configuration review
- Automation script optimization
- Security vulnerability checks
- Best practice recommendations

### 5. Troubleshooting Mode
Technical support specialist mode for diagnosing and fixing device issues.

**Trigger phrases:**
- "troubleshooting mode"
- "debug mode"
- "fix mode"
- "troubleshoot mode"

**Best for:**
- Step-by-step diagnostics
- Device connectivity issues
- Configuration error identification
- Network status checks
- Common problem resolution

### 6. Guest Mode
Simplified, privacy-conscious mode for visitors with limited device access.

**Trigger phrases:**
- "guest mode"
- "visitor mode"
- "simple mode"

**Best for:**
- Basic device control (lights, temperature, media)
- Plain, non-technical language
- Privacy protection (no personal data exposed)
- Essential functionality only
- Welcoming experience for visitors

## Usage

### Switching Modes

Simply say the mode name during a conversation:

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

To add or modify modes, edit the `PROMPT_MODES` dictionary in [`const.py`](custom_components/anything_llm_conversation/const.py):

```python
PROMPT_MODES = {
    "your_mode": {
        "name": "Your Mode Name",
        "system_prompt": """Your custom system prompt here..."""
    }
}
```

Then add trigger keywords in `MODE_KEYWORDS`:

```python
MODE_KEYWORDS = {
    "your_mode": ["your mode", "custom mode"]
}
```
