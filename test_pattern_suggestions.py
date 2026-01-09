"""Test script for pattern-based mode suggestions."""

import sys
sys.path.insert(0, 'custom_components/anything_llm_conversation')

from helpers import detect_suggested_modes

# Test cases: (query, current_mode, expected_suggested_modes)
test_cases = [
    # Analysis Mode suggestions
    ("Why is my energy bill so high?", "default", ["analysis"]),
    ("How often does my garage door open?", "default", ["analysis"]),
    ("Show me temperature history", "default", ["analysis"]),
    ("What's the uptime of my sensors?", "default", ["analysis"]),
    ("Turn on the lights", "default", []),  # Should not suggest
    
    # Research Mode suggestions
    ("Should I get Zigbee or Z-Wave?", "default", ["research"]),
    ("How does the new integration work?", "default", ["research"]),
    ("What's the best way to automate this?", "default", ["research"]),
    ("Which smart lock is better?", "default", ["research"]),
    
    # Code Review Mode suggestions
    ("Review my automation", "default", ["code_review"]),
    ("Is this YAML correct?", "default", ["code_review"]),
    ("Check my configuration", "default", ["code_review"]),
    ("Optimize this script", "default", ["code_review"]),
    
    # Troubleshooting Mode suggestions
    ("My bedroom light isn't working", "default", ["troubleshooting"]),
    ("Why isn't my automation triggering?", "default", ["troubleshooting"]),
    ("Device is offline", "default", ["troubleshooting"]),
    ("Getting timeout errors", "default", ["troubleshooting"]),
    
    # Already in suggested mode - should not suggest
    ("How much energy did I use?", "analysis", []),
    ("My light is broken", "troubleshooting", []),
    
    # Multiple mode matches - should return sorted by match count
    ("Review my energy automation", "default", None),  # Could match multiple
]

print("Testing pattern-based mode suggestions:")
print("=" * 60)

passed = 0
failed = 0

for query, current_mode, expected in test_cases:
    result = detect_suggested_modes(query, current_mode)
    
    # For tests expecting specific modes
    if expected is not None and isinstance(expected, list):
        if expected:
            # Should suggest at least the expected mode(s)
            success = all(mode in result for mode in expected)
        else:
            # Should suggest nothing
            success = len(result) == 0
        
        status = "✓" if success else "✗"
        if success:
            passed += 1
        else:
            failed += 1
            
        print(f"{status} '{query}'")
        print(f"  Current: {current_mode} | Suggested: {result} | Expected: {expected}")
    else:
        # Just show what it detected (for multi-match cases)
        print(f"ℹ '{query}'")
        print(f"  Current: {current_mode} | Suggested: {result}")

print("\n" + "=" * 60)
print(f"Results: {passed} passed, {failed} failed")

if failed == 0:
    print("✅ All tests passed!")
else:
    print(f"❌ {failed} test(s) failed")
