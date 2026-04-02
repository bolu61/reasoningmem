import json
import pytest
from reasoningmem.parse_chat import parse_gemini_chat_json

def test_parse_gemini_chat_json_valid():
    content = json.dumps([
        {
            "role": "user",
            "parts": [{"text": "Hello, how are you?"}]
        },
        {
            "role": "model",
            "parts": [
                {"text": "I am doing well, thank you!"},
                {"thoughtSignature": "some-signature"}
            ]
        }
    ])
    
    parsed = parse_gemini_chat_json(content)
    
    assert len(parsed) == 2
    assert parsed[0]["role"] == "user"
    assert parsed[0]["text"] == "Hello, how are you?"
    assert "thought_signatures" not in parsed[0]
    
    assert parsed[1]["role"] == "model"
    assert parsed[1]["text"] == "I am doing well, thank you!"
    assert parsed[1]["thought_signatures"] == ["some-signature"]

def test_parse_gemini_chat_json_complex_parts():
    content = json.dumps([
        {
            "role": "model",
            "parts": [
                {"text": "Step 1: Thought"},
                {"thoughtSignature": "sig1"},
                {"functionCall": {"name": "test_func", "args": {}}},
                {"text": "\nStep 2: Conclusion"}
            ]
        }
    ])
    
    parsed = parse_gemini_chat_json(content)
    
    assert len(parsed) == 1
    assert parsed[0]["role"] == "model"
    # Note: text is joined by newline and stripped. 
    # Since the second part starts with \n, and join adds a \n, it will be two \n
    assert parsed[0]["text"] == "Step 1: Thought\n\nStep 2: Conclusion"
    assert parsed[0]["thought_signatures"] == ["sig1"]
    assert parsed[0]["function_calls"] == [{"name": "test_func", "args": {}}]

def test_parse_gemini_chat_json_invalid_format():
    with pytest.raises(ValueError, match="Expected a list of messages"):
        parse_gemini_chat_json('{"key": "value"}')

def test_parse_gemini_chat_json_malformed_json():
    with pytest.raises(ValueError, match="Failed to parse JSON content"):
        parse_gemini_chat_json("[{")
