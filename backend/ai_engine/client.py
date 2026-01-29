"""
Groq AI Client Wrapper

Handles communication with Groq API for the AI Counsellor.
"""

import os
from groq import Groq
from config import get_settings

# Initialize Groq client
_client = None

def get_groq_client():
    global _client
    if _client is None:
        settings = get_settings()
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY not set")
        _client = Groq(api_key=settings.groq_api_key)
    return _client

async def generate_response(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> str:
    """
    Generate a chat response using Llama 3 via Groq.
    """
    client = get_groq_client()
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    return completion.choices[0].message.content
