"""
Google Gemini AI Client Wrapper

Handles communication with Google Gemini API for the AI Counsellor.
"""

import google.generativeai as genai
from config import get_settings

# Singleton for Gemini configuration
_configured = False

def configure_gemini_client():
    global _configured
    if not _configured:
        settings = get_settings()
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        genai.configure(api_key=settings.google_api_key)
        _configured = True

async def generate_response(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
    model: str = "gemini-2.0-flash-exp"
) -> str:
    """
    Generate a chat response using Google Gemini.
    """
    configure_gemini_client()
    
    gemini_model = genai.GenerativeModel(
        model,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    
    # Convert messages to Gemini format
    # Combine all messages into a single prompt for simplicity
    prompt_parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "system":
            prompt_parts.append(f"System: {content}")
        elif role == "user":
            prompt_parts.append(f"User: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")
    
    full_prompt = "\n\n".join(prompt_parts)
    
    response = await gemini_model.generate_content_async(full_prompt)
    
    return response.text
