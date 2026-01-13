# Enable Debug Logging for Workspace Switching

To see detailed logs about workspace switching, add this to your Home Assistant `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.anything_llm_conversation: debug
    custom_components.anything_llm_conversation.conversation: info
    custom_components.anything_llm_conversation.helpers: info
```

After adding this configuration:

1. Restart Home Assistant or reload the logger configuration
2. Try switching workspaces with voice commands
3. Check the logs at **Settings → System → Logs**

## What to Look For

When you say "switch to finance workspace", you should see logs like:

```
INFO Workspace switched from default to finance for conversation abc123 (stored in conversation_workspaces dict)
DEBUG conversation_workspaces state: {'abc123': 'finance'}
```

When you make a query after switching:

```
INFO Using workspace 'finance' for conversation abc123 (workspace override: Yes)
INFO Using workspace override: finance
INFO Sending request to AnythingLLM workspace 'finance' with 2 messages
INFO Using primary endpoint - workspace: finance (override: finance, active: None, default: home-assistant), thread: None
INFO API URL: http://localhost:3001/api/v1/workspace/finance/chat
```

## If You Still Don't See Logs

The workspace switching code may not be triggered. This can happen if:

1. **Voice input is being sanitized before reaching the integration** - Check if your STT (Speech-to-Text) is modifying "switch to" patterns
2. **The conversation agent is not set correctly** - Verify AnythingLLM is selected as your conversation agent in Home Assistant
3. **The integration isn't processing the message** - Verify the integration is loaded and working for normal queries

Try typing the command directly in the Home Assistant Assist interface first to rule out STT issues.
