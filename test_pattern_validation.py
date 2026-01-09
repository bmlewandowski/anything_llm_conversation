"""Test pattern validation - verify patterns don't create false positives."""

import sys
sys.path.insert(0, 'custom_components/anything_llm_conversation')

from const import MODE_SUGGESTION_PATTERNS, MODE_SUGGESTION_THRESHOLD

print("Testing pattern false positives and edge cases:")
print("=" * 70)

# Test queries that should NOT trigger any mode suggestions
false_positive_tests = [
    # Simple device control - shouldn't suggest anything
    "turn on the lights",
    "turn off the power strip",
    "set temperature to 72",
    "lock the front door",
    "play music in the living room",
    
    # Questions that are too simple for specialized modes
    "what time is it",
    "what's the weather",
    "is anyone home",
    
    # Simple status checks
    "are the lights on",
    "is the garage door closed",
    "what's the temperature",
]

# Test queries that SHOULD trigger specific modes
true_positive_tests = {
    "analysis": [
        "how much energy did I use this month",
        "show me my usage statistics",
        "how often does my garage open",
        "what's the temperature trend this week",
    ],
    "research": [
        "should I get Zigbee or Z-Wave",
        "how does the new integration work",
        "which smart lock is better",
        "what's the best way to automate this",
    ],
    "code_review": [
        "review my automation",
        "is this yaml correct",
        "check my configuration please",
        "optimize this script",
    ],
    "troubleshooting": [
        "my light isn't working",
        "bedroom sensor is offline",
        "getting timeout errors",
        "why isn't my automation triggering",
    ],
}

def count_matches(query, mode_patterns):
    """Count how many patterns match in a query."""
    query_lower = query.lower()
    return sum(1 for pattern in mode_patterns if pattern in query_lower)

print("\n1. FALSE POSITIVE TESTS (should match 0 patterns):")
print("-" * 70)

false_positive_issues = []
for query in false_positive_tests:
    total_matches = 0
    matched_modes = []
    
    for mode, patterns in MODE_SUGGESTION_PATTERNS.items():
        matches = count_matches(query, patterns)
        if matches >= MODE_SUGGESTION_THRESHOLD:
            total_matches += matches
            matched_modes.append(f"{mode}({matches})")
    
    if total_matches > 0:
        status = "✗ FAIL"
        false_positive_issues.append((query, matched_modes))
    else:
        status = "✓ PASS"
    
    print(f"{status}: '{query}'")
    if matched_modes:
        print(f"  Incorrectly matched: {', '.join(matched_modes)}")

print("\n2. TRUE POSITIVE TESTS (should match expected mode):")
print("-" * 70)

true_positive_issues = []
for expected_mode, queries in true_positive_tests.items():
    for query in queries:
        matches = count_matches(query, MODE_SUGGESTION_PATTERNS[expected_mode])
        
        if matches >= MODE_SUGGESTION_THRESHOLD:
            status = "✓ PASS"
        else:
            status = "✗ FAIL"
            true_positive_issues.append((query, expected_mode, matches))
        
        print(f"{status}: '{query}' -> {expected_mode} (matches: {matches})")

print("\n3. PATTERN STATISTICS:")
print("-" * 70)

for mode, patterns in MODE_SUGGESTION_PATTERNS.items():
    print(f"{mode}: {len(patterns)} patterns")
    
    # Check for very short patterns (potential false positives)
    short_patterns = [p for p in patterns if len(p) <= 4]
    if short_patterns:
        print(f"  ⚠ Short patterns (≤4 chars): {short_patterns}")

print("\n" + "=" * 70)
print("SUMMARY:")
print(f"False positives: {len(false_positive_issues)}")
print(f"True positive failures: {len(true_positive_issues)}")

if false_positive_issues:
    print("\n⚠ FALSE POSITIVE ISSUES:")
    for query, modes in false_positive_issues:
        print(f"  '{query}' → {', '.join(modes)}")

if true_positive_issues:
    print("\n⚠ TRUE POSITIVE FAILURES:")
    for query, mode, matches in true_positive_issues:
        print(f"  '{query}' should match {mode} (got {matches} matches, need {MODE_SUGGESTION_THRESHOLD})")

if not false_positive_issues and not true_positive_issues:
    print("\n✅ All pattern tests passed!")
else:
    print(f"\n❌ {len(false_positive_issues) + len(true_positive_issues)} issue(s) found")
