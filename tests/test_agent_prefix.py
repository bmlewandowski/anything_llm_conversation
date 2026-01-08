#!/usr/bin/env python3
"""Tests for agent prefix detection functionality."""

import sys


def should_use_agent_prefix(user_text: str, enabled: bool, keywords_str: str) -> bool:
    """Determine if @agent prefix should be added based on keywords."""
    if not enabled:
        return False
    
    keywords = [kw.strip().lower() for kw in keywords_str.split(",")]
    user_text_lower = user_text.lower()
    
    return any(keyword in user_text_lower for keyword in keywords if keyword)


class TestAgentPrefix:
    """Test agent prefix detection."""
    
    @staticmethod
    def test_basic_keyword_detection():
        """Test basic keyword matching."""
        keywords = "search, lookup, find online"
        test_cases = [
            ("search for the weather", True, True),
            ("lookup this device", True, True),
            ("find online information", True, True),
            ("turn on the lights", False, True),
            ("what's the temperature", False, True),
        ]
        
        for text, expected, enabled in test_cases:
            result = should_use_agent_prefix(text, enabled, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_case_insensitivity():
        """Test that keyword matching is case-insensitive."""
        keywords = "search, lookup"
        test_cases = [
            ("SEARCH for weather", True),
            ("Search For Weather", True),
            ("search for weather", True),
            ("SeArCh for weather", True),
            ("LOOKUP device", True),
            ("LookUp device", True),
        ]
        
        for text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_disabled_feature():
        """Test that disabled feature never adds prefix."""
        keywords = "search, lookup, find online"
        test_cases = [
            "search for weather",
            "lookup device",
            "find online information",
            "web search",
        ]
        
        for text in test_cases:
            result = should_use_agent_prefix(text, False, keywords)
            assert result == False, f"Failed: {text!r} should be False when disabled"
    
    @staticmethod
    def test_default_keywords():
        """Test with default keyword set."""
        keywords = "search, lookup, find online, web search, google, browse, check online, look up, scrape"
        test_cases = [
            ("search for the weather", True),
            ("lookup this device", True),
            ("find online information", True),
            ("web search Paris hotels", True),
            ("google the best restaurants", True),
            ("browse the web for news", True),
            ("check online for updates", True),
            ("look up the definition", True),
            ("scrape this website", True),
            ("turn on the lights", False),
            ("set temperature to 72", False),
            ("play music", False),
        ]
        
        for text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_partial_word_matching():
        """Test that partial words are matched (substring matching)."""
        keywords = "search, look"
        test_cases = [
            ("I want to search now", True),  # 'search' found
            ("please research this", True),  # 'search' is in 'research'
            ("look at this", True),  # 'look' found
            ("looking for info", True),  # 'look' is in 'looking'
            ("overlook this", True),  # 'look' is in 'overlook'
            ("turn on lights", False),  # no keyword
        ]
        
        for text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_multiple_keywords_in_message():
        """Test messages containing multiple keywords."""
        keywords = "search, lookup, find"
        test_cases = [
            ("search and lookup this", True),
            ("find and search online", True),
            ("lookup then find more", True),
        ]
        
        for text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_empty_and_whitespace_keywords():
        """Test handling of empty and whitespace-only keywords."""
        test_cases = [
            ("search, , lookup", "search for this", True),  # Empty keyword between
            ("search,,,lookup", "lookup device", True),  # Multiple empty
            (" search , lookup ", "search now", True),  # Whitespace around keywords
            ("", "search for this", False),  # No keywords at all
            ("   ", "search for this", False),  # Only whitespace
        ]
        
        for keywords, text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: keywords={keywords!r}, text={text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_single_keyword():
        """Test with single keyword."""
        keywords = "search"
        test_cases = [
            ("search for weather", True),
            ("please search", True),
            ("no keyword here", False),
        ]
        
        for text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_special_characters_in_keywords():
        """Test keywords with special characters."""
        keywords = "web-search, look.up"
        test_cases = [
            ("do a web-search", True),
            ("can you look.up this", True),
            ("websearch without hyphen", False),  # Exact match required for special chars
        ]
        
        for text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"
    
    @staticmethod
    def test_real_world_scenarios():
        """Test realistic voice command scenarios."""
        keywords = "search, lookup, find online, web search, google, browse, check online"
        test_cases = [
            # Should trigger @agent
            ("search for the weather in Paris", True),
            ("can you lookup the recipe for lasagna", True),
            ("find online the best hotels", True),
            ("do a web search for news", True),
            ("google the latest updates", True),
            ("browse for information", True),
            ("check online if the store is open", True),
            
            # Should NOT trigger @agent
            ("turn on the kitchen lights", False),
            ("set temperature to 72 degrees", False),
            ("what's the current temperature", False),
            ("play some jazz music", False),
            ("lock the front door", False),
            ("dim the bedroom lights", False),
            ("is the garage door open", False),
        ]
        
        for text, expected in test_cases:
            result = should_use_agent_prefix(text, True, keywords)
            assert result == expected, f"Failed: {text!r}\nGot: {result}\nExpected: {expected}"


def run_all_tests():
    """Run all test methods."""
    test_class = TestAgentPrefix()
    test_methods = [
        method for method in dir(test_class)
        if method.startswith('test_') and callable(getattr(test_class, method))
    ]
    
    total = len(test_methods)
    passed = 0
    failed = 0
    
    print("Testing Agent Prefix Detection")
    print("=" * 70)
    
    for method_name in test_methods:
        try:
            method = getattr(test_class, method_name)
            method()
            print(f"✓ {method_name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {method_name}")
            print(f"  {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ {method_name} (unexpected error)")
            print(f"  {type(e).__name__}: {str(e)}")
            failed += 1
    
    print("=" * 70)
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
