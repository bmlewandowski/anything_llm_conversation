#!/usr/bin/env python3
"""Demonstration of workspace switching functionality."""


def demonstrate_workspace_switching():
    """Show how workspace switching works via voice commands."""
    
    print("\n" + "="*70)
    print(" DYNAMIC WORKSPACE SWITCHING - FEATURE DEMONSTRATION")
    print("="*70)
    
    print("\n📚 OVERVIEW")
    print("-" * 70)
    print("Switch between different AnythingLLM workspaces during conversations")
    print("to access different RAG sources, agents, and knowledge bases.")
    
    print("\n🎯 USE CASES")
    print("-" * 70)
    print("• Finance Workspace     → Budget docs, expense reports, accounting")
    print("• Technical Support     → Product manuals, troubleshooting guides")
    print("• Home Automation       → Device docs, automation examples")
    print("• Personal Knowledge    → Notes, research, personal documents")
    
    print("\n💬 VOICE COMMANDS")
    print("-" * 70)
    
    scenarios = [
        {
            "title": "SCENARIO 1: Switch to Finance Workspace",
            "commands": [
                ('User', 'workspace finance'),
                ('Assistant', 'Switched to workspace finance. How can I help you?'),
                ('User', 'What were my Q4 expenses?'),
                ('Assistant', '[Accesses finance workspace with Q4 budget documents]'),
            ]
        },
        {
            "title": "SCENARIO 2: Check Current Workspace",
            "commands": [
                ('User', 'what workspace am I using?'),
                ('Assistant', 'Currently using workspace: finance'),
            ]
        },
        {
            "title": "SCENARIO 3: Switch to Technical Support",
            "commands": [
                ('User', 'workspace technical-support'),
                ('Assistant', 'Switched to workspace technical-support. How can I help you?'),
                ('User', 'How do I configure SSL certificates?'),
                ('Assistant', '[Accesses technical documentation for SSL setup]'),
            ]
        },
        {
            "title": "SCENARIO 4: Switch to Home Automation Workspace",
            "commands": [
                ('User', 'workspace home-automation'),
                ('Assistant', 'Switched to workspace home-automation. How can I help you?'),
                ('User', 'How do I create a motion sensor automation?'),
                ('Assistant', '[Accesses automation examples and device manuals]'),
            ]
        },
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{scenario['title']}")
        print("." * 70)
        for role, text in scenario['commands']:
            if role == 'User':
                print(f"  🗣️  {role:12} → !{text}")
            else:
                print(f"  🤖 {role:12} → {text}")
    
    print("\n⚙️  TECHNICAL DETAILS")
    print("-" * 70)
    print("• Command Format:    !workspace <workspace-slug>")
    print("• Query Workspace:   !workspace (shows current workspace)")
    print("• History Cleared:   When switching (fresh context)")
    print("• Per-Conversation:  Each conversation tracks its own workspace")
    print("• Voice Compatible:  Works seamlessly with Wyoming/Assist")
    
    print("\n🔧 IMPLEMENTATION HIGHLIGHTS")
    print("-" * 70)
    print("✓ Added conversation_workspaces dictionary to track per-conversation")
    print("✓ Workspace switch detection in _check_workspace_switch() method")
    print("✓ Query method accepts workspace_override parameter")
    print("✓ History cleared on workspace switch for fresh context")
    print("✓ Voice feedback confirms workspace changes")
    
    print("\n📖 COMMAND REFERENCE")
    print("-" * 70)
    print("  !workspace finance              → Switch to finance workspace")
    print("  !workspace technical-support    → Switch to tech support workspace")
    print("  !workspace home-automation      → Switch to automation workspace")
    print("  !workspace                      → Show current workspace")
    print("  what workspace                  → Alternative query command")
    print("  current workspace               → Alternative query command")
    
    print("\n🎤 VOICE ASSISTANT INTEGRATION")
    print("-" * 70)
    print("With Wyoming/Assist, simply say:")
    print('  "Hey Home, workspace finance"')
    print('  "Hey Home, what were my Q4 expenses?"')
    print('  "Hey Home, workspace technical support"')
    print('  "Hey Home, how do I configure SSL?"')
    
    print("\n💡 BENEFITS")
    print("-" * 70)
    print("✓ Access multiple knowledge bases without reconfiguration")
    print("✓ Switch contexts instantly via voice commands")
    print("✓ Different agents and tools per workspace")
    print("✓ Clean conversation context when switching")
    print("✓ No need to create multiple Home Assistant agents")
    
    print("\n" + "="*70)
    print(" Ready to use! Try it with your AnythingLLM workspaces!")
    print("="*70 + "\n")


if __name__ == "__main__":
    demonstrate_workspace_switching()
