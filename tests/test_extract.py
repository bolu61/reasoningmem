import json
from unittest.mock import MagicMock, patch

import pytest
from array import array
from reasoningmem.extract import extract_memory_from_turn
from reasoningmem.memory.memory import Memory

@patch("reasoningmem.extract.OpenAI")
@patch("reasoningmem.extract.API_KEY", "test-api-key")
def test_extract_memory_from_turn_success(mock_openai_class):
    # Setup mock
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=json.dumps({
            "assumptions": ["a1"],
            "thought": ["t1"],
            "hypothesis": ["h1"],
            "action": ["ac1"]
        })))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    
    turn = {
        "role": "model",
        "text": "The answer is 42.",
        "function_calls": [{"name": "compute", "args": {"x": 42}}]
    }
    
    memory = extract_memory_from_turn(turn)
    
    assert isinstance(memory, Memory)
    assert memory.assumptions == ["a1"]
    assert memory.thought == ["t1"]
    assert memory.hypothesis == ["h1"]
    assert memory.action == ["ac1"]
    assert isinstance(memory.embedding, array)
    assert len(memory.embedding) == 128
    
    # Verify OpenAI client was initialized correctly
    mock_openai_class.assert_called_once_with(
        api_key="test-api-key",
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/bolu61/reasoningmem",
            "X-Title": "ReasoningMem",
        }
    )
    
    # Verify call to chat completions
    mock_client.chat.completions.create.assert_called_once()
    args, kwargs = mock_client.chat.completions.create.call_args
    assert kwargs["model"] == "anthropic/claude-3.5-haiku-20241022:beta"
    assert "Respond strictly in JSON format" in kwargs["messages"][0]["content"]

@patch("reasoningmem.extract.OpenAI")
@patch("reasoningmem.extract.API_KEY", "test-api-key")
def test_extract_memory_from_turn_malformed_json(mock_openai_class):
    # Setup mock
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="invalid-json"))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    
    with pytest.raises(json.JSONDecodeError):
        extract_memory_from_turn({"role": "user", "text": "hello"})

@patch("reasoningmem.extract.API_KEY", None)
def test_extract_memory_from_turn_no_api_key():
    with pytest.raises(ValueError, match="LLM_API_KEY environment variable is not set"):
        extract_memory_from_turn({"role": "user", "text": "hello"})
