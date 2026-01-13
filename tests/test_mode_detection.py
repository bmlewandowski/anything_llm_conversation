#!/usr/bin/env python3
"""Test script for mode detection functionality."""

# Inline the detection logic for testing without Home Assistant dependencies

MODE_KEYWORDS = {
    "analysis": ["analysis mode", "analyzer mode", "analyze mode"],
    "research": ["research mode", "researcher mode"],
    "code_review": ["code review mode", "review mode", "code mode"],
    "troubleshooting": ["troubleshooting mode", "debug mode", "fix mode", "troubleshoot mode"],
    "guest": ["guest mode", "visitor mode", "simple mode"],
    "default": ["default mode", "normal mode", "standard mode"]
}

MODE_QUERY_KEYWORDS = ["what mode", "which mode", "current mode"]

PROMPT_MODES = {
    "default": {"name": "Default Mode"},
    "analysis": {"name": "Analysis Mode"},
    "research": {"name": "Research Mode"},
    "code_review": {"name": "Code Review Mode"},
    "troubleshooting": {"name": "Troubleshooting Mode"},
    "guest": {"name": "Guest Mode"}
}


def detect_mode_switch(user_input: str) -> str | None:
    """Detect if user input contains mode switch keywords."""
    input_lower = user_input.lower().strip()
    
    for mode_key, keywords in MODE_KEYWORDS.items():
        if any(keyword in input_lower for keyword in keywords):
            return mode_key
    
    return None


def is_mode_query(user_input: str) -> bool:
    """Check if user is asking about the current mode."""
    input_lower = user_input.lower().strip()
    return any(keyword in input_lower for keyword in MODE_QUERY_KEYWORDS)


def get_mode_name(mode_key: str) -> str:
    """Get the display name for a mode key."""
    return PROMPT_MODES.get(mode_key, {}).get("name", "Unknown Mode")


# Test mode detection
test_cases = [
    ("switch to analysis mode", "analysis"),
    ("analysis mode please", "analysis"),
    ("go to research mode", "research"),
    ("research mode", "research"),
    ("code review mode", "code_review"),
    ("troubleshooting mode", "troubleshooting"),
    ("debug mode", "troubleshooting"),
    ("fix mode", "troubleshooting"),
    ("guest mode", "guest"),
    ("visitor mode", "guest"),
    ("simple mode", "guest"),
    ("switch to default mode", "default"),
    ("normal mode", "default"),
    ("what is the weather", None),
    ("turn on the lights", None),
]

print("Testing mode switch detection:")
print("-" * 50)
for text, expected in test_cases:
    result = detect_mode_switch(text)
    status = "✓" if result == expected else "✗"
    print(f"{status} '{text}' -> {result} (expected: {expected})")

print("\n" + "=" * 50)

# Test mode queries
query_cases = [
    ("what mode are you in", True),
    ("which mode", True),
    ("current mode", True),
    ("what is the current mode", True),
    ("turn on the lights", False),
    ("analysis mode", False),
]

print("\nTesting mode query detection:")
print("-" * 50)
for text, expected in query_cases:
    result = is_mode_query(text)
    status = "✓" if result == expected else "✗"
    print(f"{status} '{text}' -> {result} (expected: {expected})")

print("\n" + "=" * 50)

# Test mode names
print("\nMode names:")
print("-" * 50)
for mode_key in ["default", "analysis", "research", "code_review", "troubleshooting", "guest"]:
    name = get_mode_name(mode_key)
    print(f"  {mode_key}: {name}")

print("\n✅ All tests completed!")

