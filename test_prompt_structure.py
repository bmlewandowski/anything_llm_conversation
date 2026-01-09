"""Test mode prompt generation and placeholder validation."""

import sys
sys.path.insert(0, 'custom_components/anything_llm_conversation')

from const import MODE_BEHAVIORS, BASE_PERSONA, PROMPT_MODES

print("Testing mode prompt structure and placeholders:")
print("=" * 70)

# Required placeholders in BASE_PERSONA
required_placeholders = [
    "{mode_specific_behavior}",
    "{mode_names}",
    "{mode_display_name}",
]

# Required Jinja2 templates (should be double-escaped)
required_jinja = [
    "{{{{now()}}}}",
    "{{% for entity in exposed_entities -%}}",
    "{{{{ entity.entity_id }}}}",
]

issues_found = []

print("\n1. BASE_PERSONA VALIDATION:")
print("-" * 70)

for placeholder in required_placeholders:
    if placeholder in BASE_PERSONA:
        print(f"✓ Found: {placeholder}")
    else:
        print(f"✗ MISSING: {placeholder}")
        issues_found.append(f"BASE_PERSONA missing {placeholder}")

for jinja in required_jinja:
    if jinja in BASE_PERSONA:
        print(f"✓ Found: {jinja}")
    else:
        print(f"✗ MISSING: {jinja}")
        issues_found.append(f"BASE_PERSONA missing Jinja2 template {jinja}")

print("\n2. MODE_BEHAVIORS VALIDATION:")
print("-" * 70)

for mode_key, mode_data in MODE_BEHAVIORS.items():
    print(f"\nMode: {mode_key}")
    
    # Check required fields
    if "name" not in mode_data:
        print(f"  ✗ Missing 'name' field")
        issues_found.append(f"{mode_key} missing 'name'")
    else:
        print(f"  ✓ Name: {mode_data['name']}")
    
    if "behavior" not in mode_data:
        print(f"  ✗ Missing 'behavior' field")
        issues_found.append(f"{mode_key} missing 'behavior'")
    else:
        behavior = mode_data['behavior']
        print(f"  ✓ Behavior defined ({len(behavior)} chars)")
        
        # Check if behavior has meaningful content
        if len(behavior.strip()) < 50:
            print(f"  ⚠ Behavior seems too short")
            issues_found.append(f"{mode_key} behavior is very short")

print("\n3. PROMPT_MODES VALIDATION:")
print("-" * 70)

for mode_key in MODE_BEHAVIORS.keys():
    if mode_key in PROMPT_MODES:
        print(f"✓ {mode_key} compiled into PROMPT_MODES")
        
        # Verify structure
        if "name" in PROMPT_MODES[mode_key]:
            print(f"  ✓ Has 'name': {PROMPT_MODES[mode_key]['name']}")
        else:
            print(f"  ✗ Missing 'name'")
            issues_found.append(f"PROMPT_MODES[{mode_key}] missing 'name'")
            
        if "system_prompt" in PROMPT_MODES[mode_key]:
            prompt = PROMPT_MODES[mode_key]['system_prompt']
            print(f"  ✓ Has 'system_prompt' ({len(prompt)} chars)")
            
            # Verify mode-specific behavior was injected
            mode_behavior = MODE_BEHAVIORS[mode_key]['behavior']
            if mode_behavior.strip() in prompt:
                print(f"  ✓ Behavior properly injected")
            else:
                print(f"  ✗ Behavior not found in compiled prompt")
                issues_found.append(f"{mode_key} behavior not in system_prompt")
            
            # Verify placeholders were replaced
            if "{mode_specific_behavior}" in prompt:
                print(f"  ✗ Placeholder {mode_specific_behavior} not replaced")
                issues_found.append(f"{mode_key} has unreplaced placeholder")
            
            # Verify Jinja2 templates are properly formatted (single braces in final)
            if "{{now()}}" in prompt and "{{{{now()}}}}" not in prompt:
                print(f"  ✓ Jinja2 templates properly formatted")
            else:
                print(f"  ⚠ Jinja2 template format may be incorrect")
                
        else:
            print(f"  ✗ Missing 'system_prompt'")
            issues_found.append(f"PROMPT_MODES[{mode_key}] missing 'system_prompt'")
    else:
        print(f"✗ {mode_key} NOT in PROMPT_MODES")
        issues_found.append(f"{mode_key} not compiled into PROMPT_MODES")

print("\n4. MODE INSTRUCTIONS VALIDATION:")
print("-" * 70)

# Check that each mode's prompt includes mode switching instructions
for mode_key, mode_info in PROMPT_MODES.items():
    prompt = mode_info.get('system_prompt', '')
    
    # Should mention mode switching
    has_mode_switching = "MODE SWITCHING" in prompt or "mode_names" in prompt
    if has_mode_switching:
        print(f"✓ {mode_key}: Has mode switching instructions")
    else:
        print(f"✗ {mode_key}: Missing mode switching instructions")
        issues_found.append(f"{mode_key} missing mode switching instructions")
    
    # Should mention current mode
    mode_name = mode_info['name']
    if mode_name in prompt or "mode_display_name" in prompt:
        print(f"✓ {mode_key}: References current mode")
    else:
        print(f"⚠ {mode_key}: May not reference current mode")

print("\n" + "=" * 70)
print("SUMMARY:")
print(f"Total modes defined: {len(MODE_BEHAVIORS)}")
print(f"Total modes compiled: {len(PROMPT_MODES)}")
print(f"Issues found: {len(issues_found)}")

if issues_found:
    print("\n❌ ISSUES FOUND:")
    for issue in issues_found:
        print(f"  - {issue}")
else:
    print("\n✅ All prompt structure tests passed!")
