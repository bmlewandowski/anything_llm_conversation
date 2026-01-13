#!/usr/bin/env python3
"""Demo script to show workspace switching in action."""

print("=" * 70)
print("WORKSPACE SWITCHING TROUBLESHOOTING GUIDE")
print("=" * 70)

print("\n📋 STEP 1: Enable Debug Logging")
print("-" * 70)
print("Add this to your Home Assistant configuration.yaml:")
print("""
logger:
  default: info
  logs:
    custom_components.anything_llm_conversation.conversation: info
    custom_components.anything_llm_conversation.helpers: info
""")
print("\nThen restart Home Assistant or run: Developer Tools > YAML > Reload Logger")

print("\n📋 STEP 2: Test Direct Text Input First")
print("-" * 70)
print("Before testing with voice, test with text in the Assist interface:")
print("  1. Open Home Assistant")
print("  2. Click the Assist button (bottom right)")
print("  3. Type: 'what workspace'")
print("  4. Type: 'switch to finance workspace'")
print("  5. Type: 'what workspace'")
print("\nCheck logs immediately after each command.")

print("\n📋 STEP 3: Verify Integration is Active")
print("-" * 70)
print("Ensure AnythingLLM Conversation is your active conversation agent:")
print("  1. Settings > Voice Assistants")
print("  2. Click on your assistant")
print("  3. Under 'Conversation agent', verify it's set to 'AnythingLLM Conversation'")

print("\n📋 STEP 4: Check What Logs Should Show")
print("-" * 70)
print("When you switch workspaces, you should see:")
print("""
INFO (MainThread) [custom_components.anything_llm_conversation.conversation]
  Workspace switched from default to finance for conversation xyz
  (stored in conversation_workspaces dict)

INFO (MainThread) [custom_components.anything_llm_conversation.conversation]
  Using workspace 'finance' for conversation xyz (workspace override: Yes)

INFO (MainThread) [custom_components.anything_llm_conversation.helpers]
  Using primary endpoint - workspace: finance (override: finance, ...), thread: None

INFO (MainThread) [custom_components.anything_llm_conversation.helpers]
  API URL: http://localhost:3001/api/v1/workspace/finance/chat
""")

print("\n📋 STEP 5: Verify Voice Commands")
print("-" * 70)
print("Supported voice-friendly commands:")
print("  ✓ 'switch to finance workspace'")
print("  ✓ 'use technical support workspace'")
print("  ✓ 'change workspace to home automation'")
print("  ✓ 'switch workspace to personal knowledge'")
print("  ✓ 'what workspace' (to check current)")
print("  ✓ 'switch to default workspace' (to go back)")

print("\n📋 STEP 6: Common Issues")
print("-" * 70)
print("❌ Speech-to-Text (STT) might be changing your input")
print("   Solution: Test with text input first")
print()
print("❌ Workspace slug doesn't exist in AnythingLLM")
print("   Solution: Check your workspace names in AnythingLLM")
print("   Remember: Use lowercase with dashes (e.g., 'technical-support')")
print()
print("❌ Integration not receiving the messages")
print("   Solution: Check Settings > Devices & Services > AnythingLLM")
print("   Verify the integration is loaded and configured")

print("\n📋 STEP 7: Manual Verification in AnythingLLM")
print("-" * 70)
print("To verify the workspace IS switching in AnythingLLM:")
print("  1. Open your AnythingLLM instance")
print("  2. Check the workspace tabs - the active one should change")
print("  3. Look at the thread history in each workspace")
print("  4. Messages should appear in the workspace you switched to")

print("\n📋 STEP 8: Check API Calls Directly")
print("-" * 70)
print("You can monitor AnythingLLM's logs to see incoming API calls:")
print("  - Watch for POST requests to /v1/workspace/<slug>/chat")
print("  - The <slug> should change when you switch workspaces")

print("\n" + "=" * 70)
print("Need more help? Check LOGGING_CONFIG.md for detailed logging setup")
print("=" * 70)
