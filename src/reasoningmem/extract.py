import json
import os
from array import array
from typing import Any, Dict

from openai import OpenAI
from .memory.memory import Memory

# Use more generic environment variable names
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")

def extract_memory_from_turn(
    turn: Dict[str, Any], 
    model: str = "anthropic/claude-3.5-haiku-20241022:beta"
) -> Memory:
    """
    Extracts reasoning information from a chat turn using an LLM via an 
    OpenAI-compatible API (e.g., OpenRouter) and returns a Memory object.
    """
    if not API_KEY:
        raise ValueError("LLM_API_KEY environment variable is not set.")

    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
        # OpenRouter-specific headers (ignored by other providers)
        default_headers={
            "HTTP-Referer": "https://github.com/bolu61/reasoningmem",
            "X-Title": "ReasoningMem",
        }
    )

    # Prepare context for the LLM
    role = turn.get("role", "unknown")
    text = turn.get("text", "")
    
    extra_context = []
    if turn.get("function_calls"):
        extra_context.append(f"Function Calls: {json.dumps(turn['function_calls'])}")
    if turn.get("function_responses"):
        extra_context.append(f"Function Responses: {json.dumps(turn['function_responses'])}")
    
    context_str = "\n".join(extra_context)
    
    prompt = f"""Extract the core reasoning components from the following AI agent interaction.
Role: {role}
Content: {text}
{context_str}

Respond strictly in JSON format with the following keys:
- assumptions: A list of strings representing underlying assumptions made.
- thought: A list of strings representing the step-by-step reasoning or internal logic.
- hypothesis: A list of strings representing potential outcomes or predictions.
- action: A list of strings representing the primary actions taken or intended.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("LLM returned an empty response.")
        
    extracted = json.loads(content)
        
    # Construct Memory object
    # Note: embedding is set to an empty array as a placeholder
    return Memory(
        assumptions=extracted.get("assumptions", []),
        thought=extracted.get("thought", []),
        hypothesis=extracted.get("hypothesis", []),
        action=extracted.get("action", []),
        embedding=array('f', [0.0] * 128) # Placeholder 128-dim embedding
    )
