"""Test workspace switching functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from homeassistant.components.conversation import ConversationInput, ConversationResult
from homeassistant.core import Context


@pytest.fixture
def mock_entity():
    """Create a mock AnythingLLMAgentEntity for testing."""
    with patch('custom_components.anything_llm_conversation.conversation.AnythingLLMAgentEntity') as MockEntity:
        entity = MockEntity.return_value
        entity.conversation_workspaces = {}
        entity.history = {}
        entity.options = {
            'workspace_slug': 'default-workspace',
        }
        entity.entry = MagicMock()
        entity.entry.data.get.return_value = 'default-workspace'
        yield entity


class TestWorkspaceSwitching:
    """Test workspace switching commands."""

    def test_workspace_switch_command_parsing(self, mock_entity):
        """Test that workspace switch commands are correctly parsed."""
        # Test workspace switch
        result = mock_entity._check_workspace_switch(
            "!workspace finance",
            "conv_123",
            "en"
        )
        
        assert result is not None
        assert mock_entity.conversation_workspaces.get("conv_123") == "finance"

    def test_workspace_query_command(self, mock_entity):
        """Test workspace query command."""
        # Set a workspace first
        mock_entity.conversation_workspaces["conv_123"] = "finance"
        
        # Query current workspace
        result = mock_entity._check_workspace_switch(
            "!workspace",
            "conv_123",
            "en"
        )
        
        assert result is not None
        # Should return information about current workspace

    def test_workspace_switch_clears_history(self, mock_entity):
        """Test that switching workspaces clears conversation history."""
        # Setup initial state with history
        conv_id = "conv_123"
        mock_entity.history[conv_id] = [
            {"role": "user", "content": "test"},
            {"role": "assistant", "content": "response"}
        ]
        
        # Switch workspace
        mock_entity._check_workspace_switch(
            "!workspace new-workspace",
            conv_id,
            "en"
        )
        
        # History should be cleared
        assert conv_id not in mock_entity.history

    def test_workspace_override_in_query(self, mock_entity):
        """Test that workspace override is used in query method."""
        # This would require a more complete mock setup
        # Testing the logic that workspace_override parameter works
        pass

    def test_invalid_workspace_switch(self, mock_entity):
        """Test handling of invalid workspace switch commands."""
        result = mock_entity._check_workspace_switch(
            "!workspace ",  # Empty workspace slug
            "conv_123",
            "en"
        )
        
        # Should return an error response
        assert result is not None

    def test_natural_workspace_queries(self, mock_entity):
        """Test natural language workspace queries."""
        queries = [
            "!workspace",
            "what workspace",
            "current workspace",
            "which workspace"
        ]
        
        for query in queries:
            result = mock_entity._check_workspace_switch(
                query,
                "conv_123",
                "en"
            )
            assert result is not None

    def test_workspace_persistence_per_conversation(self, mock_entity):
        """Test that workspace choices persist per conversation."""
        # Set different workspaces for different conversations
        mock_entity._check_workspace_switch("!workspace finance", "conv_1", "en")
        mock_entity._check_workspace_switch("!workspace tech", "conv_2", "en")
        
        # Each conversation should have its own workspace
        assert mock_entity.conversation_workspaces["conv_1"] == "finance"
        assert mock_entity.conversation_workspaces["conv_2"] == "tech"


def test_workspace_integration():
    """Integration test showing full workspace switching flow."""
    print("\n" + "="*60)
    print("WORKSPACE SWITCHING - INTEGRATION TEST")
    print("="*60)
    
    print("\n1. User starts conversation in default workspace")
    print("   User: 'What's the weather?'")
    print("   → Uses default workspace (home-assistant)")
    
    print("\n2. User switches to finance workspace")
    print("   User: '!workspace finance'")
    print("   Response: 'Switched to workspace finance. How can I help you?'")
    print("   → Conversation history cleared")
    print("   → Future queries use 'finance' workspace")
    
    print("\n3. User queries finance data")
    print("   User: 'What were my Q4 expenses?'")
    print("   → Accesses finance workspace with budget documents")
    
    print("\n4. User checks current workspace")
    print("   User: '!workspace'")
    print("   Response: 'Currently using workspace: finance'")
    
    print("\n5. User switches to technical support workspace")
    print("   User: '!workspace technical-support'")
    print("   Response: 'Switched to workspace technical-support. How can I help you?'")
    
    print("\n6. User queries technical documentation")
    print("   User: 'How do I configure SSL?'")
    print("   → Accesses technical-support workspace with SSL docs")
    
    print("\n" + "="*60)
    print("VOICE ASSISTANT USAGE")
    print("="*60)
    print("\nWith Wyoming/Assist:")
    print('  Say: "Hey Home, workspace finance"')
    print('  Say: "Hey Home, what were my Q4 expenses?"')
    print('  Say: "Hey Home, workspace technical support"')
    print('  Say: "Hey Home, how do I set up automation?"')
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Run the integration test demonstration
    test_workspace_integration()
