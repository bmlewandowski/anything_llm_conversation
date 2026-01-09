# Test Suite Documentation

This directory contains automated tests to validate the mode switching and suggestion functionality.

## Available Tests

### 1. test_mode_detection.py
**Purpose:** Validates explicit mode switching keyword detection

**What it tests:**
- Mode switch detection for all trigger phrases
- Mode query detection ("what mode", "which mode")
- Mode name retrieval
- Negative cases (non-mode queries)

**Run:** `python3 test_mode_detection.py`

**Expected:** All mode keywords properly detected, non-mode queries return None

---

### 2. test_pattern_validation.py
**Purpose:** Validates pattern-based mode suggestion accuracy

**What it tests:**
- False positive prevention (simple queries shouldn't trigger suggestions)
- True positive detection (relevant queries should match correct modes)
- Pattern statistics and potential issues
- Short pattern warnings

**Run:** `python3 test_pattern_validation.py`

**Expected:**
- 0 false positives
- All true positives correctly detected
- Warnings for very short patterns (≤4 chars)

---

### 3. test_prompt_structure.py
**Purpose:** Validates mode prompt generation and structure

**What it tests:**
- BASE_PERSONA contains required placeholders
- Jinja2 templates properly formatted (double-escaped)
- All MODE_BEHAVIORS have required fields
- PROMPT_MODES properly compiled from behaviors
- Mode switching instructions present in all prompts

**Run:** `python3 test_prompt_structure.py`

**Expected:** All 6 modes compile correctly with proper structure

---

### 4. test_pattern_suggestions.py ⚠️
**Purpose:** End-to-end pattern suggestion testing

**Status:** Requires Home Assistant installation to run

**What it would test:**
- detect_suggested_modes() function behavior
- Multi-pattern matching priority
- Current mode filtering (no self-suggestions)

**Note:** Cannot run standalone due to Home Assistant dependencies

---

## Running All Tests

```bash
# Run the three standalone tests
python3 test_mode_detection.py
python3 test_pattern_validation.py
python3 test_prompt_structure.py
```

## Adding New Tests

When adding new modes or patterns:

1. **Update test_mode_detection.py:**
   - Add new mode keywords to test cases
   - Add mode name to expected outputs

2. **Update test_pattern_validation.py:**
   - Add representative queries for the new mode
   - Add edge cases that shouldn't match

3. **Update test_prompt_structure.py:**
   - Tests automatically validate all modes in MODE_BEHAVIORS
   - No changes needed unless adding new required fields

## Common Issues and Solutions

### Issue: False positives detected
**Solution:** Make patterns more specific by:
- Using multi-word phrases instead of single words
- Adding context words ("my automation" vs just "automation")
- Removing overly generic terms

### Issue: True positives failing
**Solution:** Add more pattern variations:
- Include common phrasings
- Add related terms
- Consider voice transcription variations

### Issue: Pattern too short warning
**Solution:** 
- Short patterns (≤4 chars) like "kwh", "vs", "fix" are acceptable if highly specific
- Review context to ensure they won't trigger false positives

## Test Coverage

Current coverage:
- ✅ Mode switching detection
- ✅ Mode queries
- ✅ Pattern validation (false positives/negatives)
- ✅ Prompt structure integrity
- ✅ Jinja2 template formatting
- ⚠️ Pattern suggestion integration (requires HA)

## CI/CD Integration

These tests can run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run mode tests
  run: |
    python3 test_mode_detection.py
    python3 test_pattern_validation.py
    python3 test_prompt_structure.py
```

---

**Last Updated:** January 9, 2026
