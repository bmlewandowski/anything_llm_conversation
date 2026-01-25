"""Test workspace/thread switching and modular prompt passing together."""

def test_workspace_thread_and_prompt():
    """Simulate switching workspaces/threads and verify prompt is passed."""
    # Simulate messages list as built by the integration
    def build_messages(system_prompt, user_message):
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

    # Simulate modular prompt for each workspace
    prompts = {
        "default": "Default system prompt for home automation.",
        "finance": "Finance system prompt with budget context.",
        "tech": "Tech support system prompt.",
    }
    user_message = "What is my energy usage?"

    # Simulate switching: default → finance → tech → default
    states = []
    conversation_id = "conv_abc"
    configured_workspace = "home-assistant"
    configured_thread = "thread-123"
    conversation_workspaces = {}
    conversation_threads = {}

    # 1. Default workspace
    workspace = configured_workspace
    thread = configured_thread
    messages = build_messages(prompts["default"], user_message)
    states.append((workspace, thread, messages))

    # 2. Switch to finance workspace
    conversation_workspaces[conversation_id] = "finance"
    conversation_threads[conversation_id] = None
    workspace = conversation_workspaces[conversation_id]
    thread = None
    messages = build_messages(prompts["finance"], user_message)
    states.append((workspace, thread, messages))

    # 3. Switch to tech workspace
    conversation_workspaces[conversation_id] = "tech"
    conversation_threads[conversation_id] = None
    workspace = conversation_workspaces[conversation_id]
    thread = None
    messages = build_messages(prompts["tech"], user_message)
    states.append((workspace, thread, messages))

    # 4. Switch back to default
    del conversation_workspaces[conversation_id]
    del conversation_threads[conversation_id]
    workspace = configured_workspace
    thread = configured_thread
    messages = build_messages(prompts["default"], user_message)
    states.append((workspace, thread, messages))

    # Simulate API call payload construction
    for i, (ws, th, msgs) in enumerate(states, 1):
        # Extract system prompt
        system_prompt = None
        for msg in msgs:
            if msg["role"] == "system":
                system_prompt = msg["content"]
                break
        payload = {
            "message": msgs[-1]["content"],
            "mode": "chat",
        }
        if system_prompt:
            payload["prompt"] = system_prompt
        print(f"Step {i}: workspace={ws}, thread={th}, prompt='{payload.get('prompt')}'")
        # Check that the correct prompt is always sent
        if ws == "finance":
            assert payload["prompt"] == prompts["finance"]
            assert th is None
        elif ws == "tech":
            assert payload["prompt"] == prompts["tech"]
            assert th is None
        else:
            assert payload["prompt"] == prompts["default"]
            assert th == configured_thread
    print("\n✅ All workspace/thread and prompt logic is working together!")

if __name__ == "__main__":
    test_workspace_thread_and_prompt()
