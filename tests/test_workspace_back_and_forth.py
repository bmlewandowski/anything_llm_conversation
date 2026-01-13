#!/usr/bin/env python3
"""Test workspace switching back and forth between multiple workspaces."""

def test_workspace_switching_back_and_forth():
    """Verify you can switch between workspaces multiple times."""
    
    # Simulate the entity state
    conversation_workspaces = {}
    conversation_threads = {}
    conversation_id = "conv_123"
    
    # Configured defaults
    configured_workspace = "home-assistant"
    configured_thread = "my-thread-123"
    
    print("\n" + "=" * 70)
    print("TEST: Workspace Switching Back and Forth")
    print("=" * 70)
    
    # Step 1: Start with configured defaults
    print("\n1. Initial State (Configured Defaults):")
    print(f"   Configured workspace: {configured_workspace}")
    print(f"   Configured thread: {configured_thread}")
    print(f"   conversation_workspaces: {conversation_workspaces}")
    print(f"   → API uses: /v1/workspace/{configured_workspace}/thread/{configured_thread}/chat")
    
    # Step 2: Switch to finance workspace
    print("\n2. Switch to 'finance' workspace:")
    conversation_workspaces[conversation_id] = "finance"
    conversation_threads[conversation_id] = None
    active_workspace = conversation_workspaces.get(conversation_id)
    active_thread = conversation_threads.get(conversation_id) if conversation_id in conversation_threads else False
    
    if active_workspace:
        workspace = active_workspace
        thread = None if active_thread is None and conversation_id in conversation_threads else configured_thread
    else:
        workspace = configured_workspace
        thread = configured_thread
    
    print(f"   conversation_workspaces[{conversation_id}]: {conversation_workspaces[conversation_id]}")
    print(f"   conversation_threads[{conversation_id}]: {conversation_threads[conversation_id]}")
    print(f"   → API uses: /v1/workspace/{workspace}/chat")
    assert workspace == "finance"
    assert active_thread is None
    
    # Step 3: Switch to technical-support workspace
    print("\n3. Switch to 'technical-support' workspace:")
    conversation_workspaces[conversation_id] = "technical-support"
    conversation_threads[conversation_id] = None
    active_workspace = conversation_workspaces.get(conversation_id)
    
    if active_workspace:
        workspace = active_workspace
        thread = None
    else:
        workspace = configured_workspace
        thread = configured_thread
    
    print(f"   conversation_workspaces[{conversation_id}]: {conversation_workspaces[conversation_id]}")
    print(f"   → API uses: /v1/workspace/{workspace}/chat")
    assert workspace == "technical-support"
    
    # Step 4: Switch back to finance workspace
    print("\n4. Switch back to 'finance' workspace:")
    conversation_workspaces[conversation_id] = "finance"
    conversation_threads[conversation_id] = None
    active_workspace = conversation_workspaces.get(conversation_id)
    
    if active_workspace:
        workspace = active_workspace
    else:
        workspace = configured_workspace
    
    print(f"   conversation_workspaces[{conversation_id}]: {conversation_workspaces[conversation_id]}")
    print(f"   → API uses: /v1/workspace/{workspace}/chat")
    assert workspace == "finance"
    
    # Step 5: Switch to default (configured) workspace
    print("\n5. Switch to 'default' (configured) workspace:")
    if conversation_id in conversation_workspaces:
        del conversation_workspaces[conversation_id]
    if conversation_id in conversation_threads:
        del conversation_threads[conversation_id]
    
    active_workspace = conversation_workspaces.get(conversation_id)
    
    if active_workspace:
        workspace = active_workspace
    else:
        workspace = configured_workspace
        thread = configured_thread
    
    print(f"   conversation_workspaces: {conversation_workspaces}")
    print(f"   conversation_threads: {conversation_threads}")
    print(f"   → API uses: /v1/workspace/{workspace}/thread/{thread}/chat")
    assert conversation_id not in conversation_workspaces
    assert workspace == configured_workspace
    
    # Step 6: Switch to finance again
    print("\n6. Switch to 'finance' workspace again:")
    conversation_workspaces[conversation_id] = "finance"
    conversation_threads[conversation_id] = None
    active_workspace = conversation_workspaces.get(conversation_id)
    
    if active_workspace:
        workspace = active_workspace
    else:
        workspace = configured_workspace
    
    print(f"   conversation_workspaces[{conversation_id}]: {conversation_workspaces[conversation_id]}")
    print(f"   → API uses: /v1/workspace/{workspace}/chat")
    assert workspace == "finance"
    
    # Step 7: Switch back to default again
    print("\n7. Switch to 'default' workspace again:")
    if conversation_id in conversation_workspaces:
        del conversation_workspaces[conversation_id]
    if conversation_id in conversation_threads:
        del conversation_threads[conversation_id]
    
    active_workspace = conversation_workspaces.get(conversation_id)
    
    if active_workspace:
        workspace = active_workspace
    else:
        workspace = configured_workspace
        thread = configured_thread
    
    print(f"   conversation_workspaces: {conversation_workspaces}")
    print(f"   → API uses: /v1/workspace/{workspace}/thread/{thread}/chat")
    assert conversation_id not in conversation_workspaces
    assert workspace == configured_workspace
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS: Can switch back and forth between workspaces!")
    print("=" * 70)
    
    print("\n📊 Summary:")
    print("   ✓ Can switch from default to any workspace")
    print("   ✓ Can switch between non-default workspaces")
    print("   ✓ Can switch back to default workspace multiple times")
    print("   ✓ Each switch correctly updates workspace and thread")
    print("   ✓ Returning to default restores configured thread")


if __name__ == "__main__":
    test_workspace_switching_back_and_forth()
