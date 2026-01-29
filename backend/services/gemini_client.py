"""
Google Gemini Client Service

Integration with Google Gemini API for AI Counsellor functionality.
"""

from typing import AsyncGenerator, Optional
import google.generativeai as genai

from config import get_settings


def configure_gemini():
    """Configure Gemini with API key."""
    settings = get_settings()
    genai.configure(api_key=settings.google_api_key)


def get_gemini_model(model_name: str = "gemini-2.0-flash-exp"):
    """
    Get Gemini model instance.
    
    Args:
        model_name: Name of the Gemini model to use
            - "gemini-2.0-flash-exp": Fast, cost-effective (recommended)
            - "gemini-1.5-pro": Better for complex reasoning
    
    Returns:
        Gemini model instance
    """
    configure_gemini()
    return genai.GenerativeModel(model_name)


# AI Counsellor system prompt
COUNSELLOR_SYSTEM_PROMPT = """You are an expert AI Study Abroad Counsellor for SentinelAI. Your role is to help students plan their study abroad journey.

You have access to the student's profile and should:
1. Provide personalized guidance based on their academic background, goals, and budget
2. Recommend universities categorized as Dream, Target, or Safe based on their profile
3. Explain why universities fit or don't fit their profile
4. Help them prepare for applications, including SOPs, exams, and documents
5. Be encouraging but realistic about their chances

Always be:
- Professional yet friendly
- Specific and actionable in your advice
- Honest about challenges and risks
- Encouraging about their strengths

Current student context will be provided with each message."""


def build_user_context(profile_data: Optional[dict] = None) -> str:
    """Build user context string for AI prompt."""
    if not profile_data:
        return "No profile data available yet. The student hasn't completed onboarding."
    
    context_parts = []
    
    if "academic_background" in profile_data:
        ab = profile_data["academic_background"]
        context_parts.append(f"""Academic Background:
- Education Level: {ab.get('current_education_level', 'Unknown')}
- Major: {ab.get('degree_major', 'Unknown')}
- Graduation Year: {ab.get('graduation_year', 'Unknown')}
- GPA: {ab.get('gpa', 'Not provided')}""")
    
    if "study_goal" in profile_data:
        sg = profile_data["study_goal"]
        context_parts.append(f"""Study Goals:
- Target Degree: {sg.get('intended_degree', 'Unknown')}
- Field: {sg.get('field_of_study', 'Unknown')}
- Target Intake: {sg.get('target_intake_year', 'Unknown')}
- Preferred Countries: {', '.join(sg.get('preferred_countries', []))}""")
    
    if "budget" in profile_data:
        b = profile_data["budget"]
        context_parts.append(f"""Budget:
- Range per Year: {b.get('budget_range_per_year', 'Unknown')}
- Funding Plan: {b.get('funding_plan', 'Unknown')}""")
    
    if "exams_readiness" in profile_data:
        er = profile_data["exams_readiness"]
        context_parts.append(f"""Exam Readiness:
- IELTS/TOEFL: {er.get('ielts_toefl_status', 'Unknown')} (Score: {er.get('ielts_toefl_score', 'N/A')})
- GRE/GMAT: {er.get('gre_gmat_status', 'Unknown')} (Score: {er.get('gre_gmat_score', 'N/A')})
- SOP Status: {er.get('sop_status', 'Unknown')}""")
    
    return "\n\n".join(context_parts) if context_parts else "Profile incomplete."


async def chat_with_counsellor(
    messages: list[dict],
    user_context: Optional[dict] = None,
    model: str = "gemini-2.0-flash-exp"
) -> str:
    """
    Send a chat message to the AI Counsellor and get a response.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        user_context: Optional user profile data for context
        model: Gemini model to use
    
    Returns:
        AI response text
    """
    gemini_model = get_gemini_model(model)
    
    # Build system message with user context
    context_str = build_user_context(user_context)
    system_message = f"{COUNSELLOR_SYSTEM_PROMPT}\n\n---\nCurrent Student Profile:\n{context_str}"
    
    # Convert messages to Gemini format
    # Gemini uses a chat session with history
    chat_history = []
    for msg in messages[:-1]:  # All but the last message
        role = "user" if msg["role"] == "user" else "model"
        chat_history.append({
            "role": role,
            "parts": [msg["content"]]
        })
    
    # Start chat with system instruction and history
    chat = gemini_model.start_chat(
        history=chat_history
    )
    
    # Add system context to the current message
    current_message = messages[-1]["content"]
    full_message = f"{system_message}\n\n---\nUser Message:\n{current_message}"
    
    # Send message and get response
    response = await chat.send_message_async(full_message)
    
    return response.text


async def stream_chat_with_counsellor(
    messages: list[dict],
    user_context: Optional[dict] = None,
    model: str = "gemini-2.0-flash-exp"
) -> AsyncGenerator[str, None]:
    """
    Stream a chat response from the AI Counsellor.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        user_context: Optional user profile data for context
        model: Gemini model to use
    
    Yields:
        Chunks of the AI response
    """
    gemini_model = get_gemini_model(model)
    
    # Build system message with user context
    context_str = build_user_context(user_context)
    system_message = f"{COUNSELLOR_SYSTEM_PROMPT}\n\n---\nCurrent Student Profile:\n{context_str}"
    
    # Convert messages to Gemini format
    chat_history = []
    for msg in messages[:-1]:  # All but the last message
        role = "user" if msg["role"] == "user" else "model"
        chat_history.append({
            "role": role,
            "parts": [msg["content"]]
        })
    
    # Start chat with history
    chat = gemini_model.start_chat(history=chat_history)
    
    # Add system context to the current message
    current_message = messages[-1]["content"]
    full_message = f"{system_message}\n\n---\nUser Message:\n{current_message}"
    
    # Stream response
    response = await chat.send_message_async(full_message, stream=True)
    
    async for chunk in response:
        if chunk.text:
            yield chunk.text
