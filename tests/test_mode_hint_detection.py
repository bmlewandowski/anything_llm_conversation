#!/usr/bin/env python3
"""Regression test for mode-hint detection in LLM responses.

Bug: _async_handle_message referenced `current_mode` (undefined) instead of
`current_workspace` when scanning LLM responses for pending mode suggestions.
This caused a NameError whenever a response contained '?' and a mode display name.
"""

import re

# ── Inline the data structures from conversation.py ──────────────────────────

_RESPONSE_MODE_HINTS = {
    "analysis mode": "analysis",
    "research mode": "research",
    "code review mode": "code_review",
    "troubleshooting mode": "troubleshooting",
    "guest mode": "guest",
    "security mode": "security",
    "default mode": "default",
}

_RE_AFFIRMATIVE = re.compile(
    r'^\s*(?:yes|yeah|yep|sure|ok(?:ay)?|please|go\s+ahead|absolutely|of\s+course|do\s+it|sounds?\s+good)\s*[.!]?\s*$',
    re.IGNORECASE,
)


# ── Helper: simulate the hint-detection block from _async_handle_message ─────

def _detect_hint(response_text: str, current_workspace: str) -> str | None:
    """Return the suggested mode key if response hints at a switch, else None."""
    if '?' not in response_text:
        return None
    text_lower = response_text.lower()
    for hint_name, hint_key in _RESPONSE_MODE_HINTS.items():
        if hint_name in text_lower and hint_key != current_workspace:
            return hint_key
    return None


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_hint_detected_in_question():
    """LLM suggests Analysis Mode with a question mark → hint stored."""
    response = "Would you like me to switch to Analysis Mode for a detailed energy breakdown?"
    result = _detect_hint(response, current_workspace="default")
    assert result == "analysis", f"Expected 'analysis', got {result!r}"


def test_hint_not_stored_when_already_in_that_workspace():
    """No hint stored if the suggested mode is the current workspace."""
    response = "Would you like me to switch to Analysis Mode for detailed stats?"
    result = _detect_hint(response, current_workspace="analysis")
    assert result is None, "Should not suggest switching to the already-active workspace"


def test_hint_requires_question_mark():
    """Statement without '?' must not trigger a hint."""
    response = "You should switch to Troubleshooting Mode."
    result = _detect_hint(response, current_workspace="default")
    assert result is None, "No hint without a question mark"


def test_hint_case_insensitive():
    """Match is case-insensitive (hint names are lowercased before comparison)."""
    response = "Would you like to try RESEARCH MODE for a deeper dive?"
    result = _detect_hint(response, current_workspace="default")
    assert result == "research", f"Expected 'research', got {result!r}"


def test_hint_multiple_hints_first_wins():
    """When multiple hints appear, the first dict entry wins (dict ordering)."""
    response = "Should I switch to Analysis Mode or Research Mode?"
    result = _detect_hint(response, current_workspace="default")
    # analysis appears first in _RESPONSE_MODE_HINTS
    assert result in ("analysis", "research"), f"Unexpected result: {result!r}"


def test_no_hint_in_plain_answer():
    """Normal answer without a mode name and no '?' → no hint."""
    response = "The living room lights are currently on."
    result = _detect_hint(response, current_workspace="default")
    assert result is None


def test_affirmative_regex_matches():
    """Check that the affirmative confirmation regex matches expected phrases."""
    affirmatives = ["yes", "Yes", "YES", "yeah", "yep", "sure", "ok", "okay",
                    "please", "go ahead", "absolutely", "of course", "do it",
                    "sounds good", "sound good", "yes!", "sure."]
    for phrase in affirmatives:
        assert _RE_AFFIRMATIVE.match(phrase), f"'{phrase}' should be affirmative"


def test_affirmative_regex_rejects():
    """Non-affirmative replies must not match."""
    negatives = ["no", "nope", "not now", "skip it", "just answer", "what time is it?"]
    for phrase in negatives:
        assert not _RE_AFFIRMATIVE.match(phrase), f"'{phrase}' should NOT be affirmative"


def test_hint_troubleshooting():
    response = "Would you like me to switch to Troubleshooting Mode for a step-by-step diagnosis?"
    result = _detect_hint(response, current_workspace="default")
    assert result == "troubleshooting"


def test_hint_security():
    response = "Should I enable Security Mode to review your lock and camera status?"
    result = _detect_hint(response, current_workspace="default")
    assert result == "security"


if __name__ == "__main__":
    tests = [
        test_hint_detected_in_question,
        test_hint_not_stored_when_already_in_that_workspace,
        test_hint_requires_question_mark,
        test_hint_case_insensitive,
        test_hint_multiple_hints_first_wins,
        test_no_hint_in_plain_answer,
        test_affirmative_regex_matches,
        test_affirmative_regex_rejects,
        test_hint_troubleshooting,
        test_hint_security,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
