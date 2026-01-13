"""Test voice-friendly workspace switching patterns."""

def test_workspace_patterns():
    """Test if voice patterns are correctly detected."""
    
    test_cases = [
        # Original pattern
        ("!workspace finance", "finance"),
        ("!workspace technical-support", "technical-support"),
        
        # Voice-friendly patterns
        ("switch to finance workspace", "finance"),
        ("Switch to Finance Workspace", "finance"),  # Test case insensitivity
        ("use technical support workspace", "technical support"),
        ("change workspace to home automation", "home automation"),
        ("switch workspace to personal knowledge", "personal knowledge"),
        
        # Default handling
        ("switch to default workspace", "default"),
        ("use default workspace", "default"),
        
        # Query patterns (should return None for workspace)
        ("!workspace", None),
        ("what workspace", None),
        ("current workspace", None),
        ("what workspace are you in", None),
        ("what workspace am i in", None),
        ("which workspace are you in", None),
        ("what workspace are you using", None),
    ]
    
    results = []
    for text, expected_workspace in test_cases:
        text_lower = text.lower().strip()
        new_workspace = None
        
        # Pattern 1: "!workspace <name>"
        if text_lower.startswith("!workspace "):
            new_workspace = text.split(" ", 1)[1].strip()
        
        # Pattern 2: "switch to <name> workspace"
        elif text_lower.startswith("switch to ") and " workspace" in text_lower:
            parts = text_lower.replace("switch to ", "").replace(" workspace", "").strip()
            new_workspace = parts
        
        # Pattern 3: "use <name> workspace"
        elif text_lower.startswith("use ") and " workspace" in text_lower:
            parts = text_lower.replace("use ", "").replace(" workspace", "").strip()
            new_workspace = parts
        
        # Pattern 4: "change workspace to <name>"
        elif text_lower.startswith("change workspace to "):
            new_workspace = text_lower.replace("change workspace to ", "").strip()
        
        # Pattern 5: "switch workspace to <name>"
        elif text_lower.startswith("switch workspace to "):
            new_workspace = text_lower.replace("switch workspace to ", "").strip()
        
        # Check for query patterns (should not extract workspace)
        workspace_query_patterns = [
            "!workspace",
            "what workspace",
            "current workspace", 
            "which workspace",
            "what workspace are you in",
            "what workspace am i in",
            "which workspace are you in",
            "which workspace am i in",
            "what workspace are you using",
            "what workspace am i using",
        ]
        
        is_workspace_query = (
            text_lower in workspace_query_patterns or
            text_lower.startswith("what workspace") or
            text_lower.startswith("which workspace") or
            (text_lower.startswith("current") and "workspace" in text_lower)
        )
        
        # Don't extract workspace if it's a query (unless it's also a switch command)
        is_switch_command = any(
            text_lower.startswith(p) for p in ["switch to", "use ", "change workspace to", "switch workspace to", "!workspace "]
        )
        
        if is_workspace_query and not is_switch_command:
            new_workspace = None
        
        match = "✓" if new_workspace == expected_workspace else "✗"
        results.append((match, text, expected_workspace, new_workspace))
        print(f"{match} '{text}' -> Expected: {expected_workspace}, Got: {new_workspace}")
    
    # Summary
    passed = sum(1 for r in results if r[0] == "✓")
    total = len(results)
    print(f"\n{passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    success = test_workspace_patterns()
    exit(0 if success else 1)
