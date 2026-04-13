#!/usr/bin/env python3
"""Test script for mode detection functionality."""

# Inline the detection logic for testing without Home Assistant dependencies

MODE_KEYWORDS = {
    "adventure": ["adventure mode", "author mode", "story mode", "creative mode"],
    "analysis": ["analysis mode", "analyzer mode", "analyze mode"],
    "research": ["research mode", "researcher mode"],
    "visual": ["visual mode", "vision mode", "image mode", "multimodal mode"],
    "investigation": ["investigation mode", "investigate mode", "forensics mode", "root cause mode"],
    "code_review": ["code review mode", "review mode", "code mode"],
    "troubleshooting": ["troubleshooting mode", "debug mode", "fix mode", "troubleshoot mode"],
    "guest": ["guest mode", "visitor mode", "simple mode"],
    "default": ["default mode", "normal mode", "standard mode"]
}

MODE_QUERY_KEYWORDS = ["what mode", "which mode", "current mode", "what workspace", "which workspace", "current workspace"]

MODE_TO_WORKSPACE = {
    "adventure": "adventure",
    "analysis": "analysis",
    "research": "research",
    "visual": "visual",
    "investigation": "investigation",
    "code_review": "investigation",
    "troubleshooting": "investigation",
    "guest": "default",
    "default": "default",
}

PROMPT_MODES = {
    "default": {"name": "Default Workspace"},
    "adventure": {"name": "Adventure Workspace"},
    "analysis": {"name": "Analysis Workspace"},
    "research": {"name": "Research Workspace"},
    "visual": {"name": "Visual Workspace"},
    "investigation": {"name": "Investigation Workspace"},
    "security": {"name": "Security Workspace"},
}


def detect_mode_switch(user_input):
    """Detect if user input contains mode switch keywords."""
    input_lower = user_input.lower().strip().rstrip(".")
    
    for mode_key, keywords in MODE_KEYWORDS.items():
        if any(keyword in input_lower for keyword in keywords):
            return MODE_TO_WORKSPACE.get(mode_key, mode_key)
    
    return None


def is_mode_query(user_input: str) -> bool:
    """Check if user is asking about the current mode."""
    input_lower = user_input.lower().strip()
    return any(keyword in input_lower for keyword in MODE_QUERY_KEYWORDS)


def get_mode_name(mode_key: str) -> str:
    """Get the display name for a workspace key."""
    return PROMPT_MODES.get(mode_key, {}).get("name", "Unknown Mode")


# Test mode detection
test_cases = [
    ("switch to analysis mode", "analysis"),
    ("analysis mode please", "analysis"),
    ("go to research mode", "research"),
    ("research mode", "research"),
    ("adventure mode", "adventure"),
    ("visual mode", "visual"),
    ("investigation mode", "investigation"),
    ("code review mode", "investigation"),
    ("troubleshooting mode", "investigation"),
    ("debug mode", "investigation"),
    ("fix mode", "investigation"),
    ("guest mode", "default"),
    ("visitor mode", "default"),
    ("simple mode", "default"),
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
    ("what workspace are you in", True),
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
for mode_key in ["default", "adventure", "analysis", "research", "visual", "investigation", "security"]:
    name = get_mode_name(mode_key)
    print(f"  {mode_key}: {name}")

print("\n✅ All tests completed!")

