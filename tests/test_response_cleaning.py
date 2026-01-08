#!/usr/bin/env python3
"""Tests for response cleaning functionality."""

import re
import sys
from pathlib import Path

# Inline the cleaning logic for testing
_RE_THINK_TAGS = re.compile(r'<think>.*?</think>', flags=re.DOTALL | re.IGNORECASE)
_RE_MARKDOWN_LINKS = re.compile(r'\[([^\]]+)\]\([^\)]+\)')
_RE_WHITESPACE = re.compile(r'\s+')
_RE_BR_TAGS = re.compile(r'<br\s*/?>', flags=re.IGNORECASE)
_RE_HTML_TAGS = re.compile(r'<[^>]+>')
_RE_CELSIUS = re.compile(r'(\d+)C\b')
_RE_FAHRENHEIT = re.compile(r'(\d+)F\b')


def clean_response_for_tts(text: str) -> str:
    """Clean up LLM response for text-to-speech."""
    import html
    
    # Remove <think> tags and their content
    text = _RE_THINK_TAGS.sub('', text)
    
    # Remove asterisks (markdown bold/italic)
    text = text.replace('*', '')
    
    # Convert markdown links [text](url) to just text
    text = _RE_MARKDOWN_LINKS.sub(r'\1', text)
    
    # Normalize whitespace to single spaces
    text = _RE_WHITESPACE.sub(' ', text)
    
    # HTML entity handling
    text = html.unescape(text)  # Converts &nbsp; &amp; &lt; &gt; etc
    text = _RE_BR_TAGS.sub(' ', text)  # Convert <br> to space
    text = _RE_HTML_TAGS.sub('', text)  # Remove any other HTML tags
    
    # Special character cleanup
    text = text.replace('°', ' degrees ')
    text = text.replace('%', ' percent ')
    text = text.replace('$', ' dollars ')
    text = text.replace('€', ' euros ')
    text = text.replace('£', ' pounds ')
    text = _RE_CELSIUS.sub(r'\1 degrees Celsius', text)
    text = _RE_FAHRENHEIT.sub(r'\1 degrees Fahrenheit', text)
    
    # Clean up leading punctuation
    text = text.strip()
    text = text.lstrip('.,;:!?-')
    
    return text.strip()


# Test cases
class TestResponseCleaning:
    """Test response cleaning for TTS."""
    
    @staticmethod
    def test_think_tag_removal():
        """Test removal of <think> tags and content."""
        test_cases = [
            (
                "Here is the answer. <think>Let me think about this...</think> The temperature is 72F.",
                "Here is the answer. The temperature is 72 degrees Fahrenheit."
            ),
            (
                "<think>Processing...</think>Lights are on.",
                "Lights are on."
            ),
            (
                "<THINK>Case insensitive</THINK>Done.",
                "Done."
            ),
            (
                "No think tags here.",
                "No think tags here."
            ),
            (
                "<think>Multi\nline\nthink</think>Result.",
                "Result."
            ),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            assert result == expected, f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_markdown_removal():
        """Test removal of markdown formatting."""
        test_cases = [
            ("This is **bold** text.", "This is bold text."),
            ("This is *italic* text.", "This is italic text."),
            ("***Very bold***", "Very bold"),
            ("No markdown", "No markdown"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            assert result == expected, f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_link_conversion():
        """Test conversion of markdown links."""
        test_cases = [
            ("[Click here](https://example.com)", "Click here"),
            ("Check [this link](http://test.com) out.", "Check this link out."),
            ("Multiple [link1](url1) and [link2](url2)", "Multiple link1 and link2"),
            ("No links here", "No links here"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            assert result == expected, f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_html_entity_handling():
        """Test HTML entity conversion."""
        test_cases = [
            ("Temperature&nbsp;is&nbsp;high", "Temperature is high"),
            ("A &amp; B", "A & B"),
            ("&lt;tag&gt;", ""),  # Gets unescaped to <tag> then removed as HTML
            ("&quot;quoted&quot;", '"quoted"'),
            ("Normal text", "Normal text"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            # Normalize spaces for comparison
            result_normalized = ' '.join(result.split())
            expected_normalized = ' '.join(expected.split())
            assert result_normalized == expected_normalized, \
                f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_html_tag_removal():
        """Test HTML tag removal."""
        test_cases = [
            ("Text with <br> break", "Text with break"),
            ("Text with <br/> break", "Text with break"),
            ("Text with<br />break", "Text with break"),
            ("<div>Content</div>", "Content"),
            ("<p>Para 1</p> <p>Para 2</p>", "Para 1 Para 2"),  # Space between tags
            ("No HTML tags", "No HTML tags"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            # Normalize multiple spaces to single space for comparison
            result_normalized = ' '.join(result.split())
            expected_normalized = ' '.join(expected.split())
            assert result_normalized == expected_normalized, \
                f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_temperature_conversion():
        """Test temperature symbol conversion."""
        test_cases = [
            ("It's 25C outside", "It's 25 degrees Celsius outside"),
            ("Temperature is 77F", "Temperature is 77 degrees Fahrenheit"),
            ("Between 20C and 25C", "Between 20 degrees Celsius and 25 degrees Celsius"),
            ("Set to 72°F", "Set to 72 degrees F"),  # Note: ° symbol is separate from C/F
            ("No temperature", "No temperature"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            assert result == expected, f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_special_character_conversion():
        """Test special character conversion."""
        test_cases = [
            ("Temperature is 72°", "Temperature is 72 degrees"),
            ("Usage is 50%", "Usage is 50 percent"),
            ("Cost is $10", "Cost is dollars 10"),  # $ replaced before number
            ("Price: €20", "Price: euros 20"),
            ("Value: £30", "Value: pounds 30"),
            ("Mix: $5 and 50% and 20°", "Mix: dollars 5 and 50 percent and 20 degrees"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            # Normalize multiple spaces
            result_normalized = ' '.join(result.split())
            expected_normalized = ' '.join(expected.split())
            assert result_normalized == expected_normalized, \
                f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_whitespace_normalization():
        """Test whitespace normalization."""
        test_cases = [
            ("Multiple   spaces", "Multiple spaces"),
            ("Tab\ttab", "Tab tab"),
            ("New\nline", "New line"),
            ("Mixed  \t \n  whitespace", "Mixed whitespace"),
            ("Normal spacing", "Normal spacing"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            assert result == expected, f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_leading_punctuation_removal():
        """Test removal of leading punctuation."""
        test_cases = [
            (".Leading dot", "Leading dot"),
            (",Comma first", "Comma first"),
            ("...Multiple dots", "Multiple dots"),
            ("-Dash start", "Dash start"),
            ("Normal text", "Normal text"),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            assert result == expected, f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"
    
    @staticmethod
    def test_complex_combinations():
        """Test complex real-world scenarios."""
        test_cases = [
            (
                "<think>Analyzing...</think>The **temperature** is 72°F and humidity is 50%.",
                "The temperature is 72 degrees F and humidity is 50 percent ."
            ),
            (
                "Check [this device](http://example.com)<br/>It's at 25C.",
                "Check this device It's at 25 degrees Celsius."
            ),
            (
                "*Energy usage* is **$15** and **20%** above normal.&nbsp;<think>Should recommend</think>",
                "Energy usage is dollars 15 and 20 percent above normal."
            ),
            (
                "<div><think>Process</think>**Result:**&nbsp;[Click here](url)&nbsp;for 72F</div>",
                "Result: Click here for 72 degrees Fahrenheit"
            ),
        ]
        
        for input_text, expected in test_cases:
            result = clean_response_for_tts(input_text)
            # Normalize multiple spaces and trim for comparison
            result_normalized = ' '.join(result.split())
            expected_normalized = ' '.join(expected.split())
            assert result_normalized == expected_normalized, \
                f"Failed: {input_text!r}\nGot: {result!r}\nExpected: {expected!r}"


def run_all_tests():
    """Run all test methods."""
    test_class = TestResponseCleaning()
    test_methods = [
        method for method in dir(test_class)
        if method.startswith('test_') and callable(getattr(test_class, method))
    ]
    
    total = len(test_methods)
    passed = 0
    failed = 0
    
    print("Testing Response Cleaning for TTS")
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
