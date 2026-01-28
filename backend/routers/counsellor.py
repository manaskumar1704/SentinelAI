"""
AI Counsellor Router

API endpoints for AI chat functionality.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from middleware.auth import get_current_user
from models.user import ClerkUser
from services.groq_client import chat_with_counsellor, stream_chat_with_counsellor
from services.onboarding import get_onboarding_data, is_onboarding_complete


router = APIRouter()


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Chat request with message history."""
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    """Chat response from AI."""
    message: ChatMessage
    onboarding_complete: bool


def check_onboarding_required(user_id: str) -> None:
    """Raise exception if onboarding is not complete."""
    if not is_onboarding_complete(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Complete onboarding before accessing AI Counsellor"
        )


def get_user_context(user_id: str) -> Optional[dict]:
    """Get user's onboarding data as context dict."""
    data = get_onboarding_data(user_id)
    if data:
        return data.model_dump()
    return None


@router.post("/chat")
async def chat(
    request: ChatRequest,
    user: ClerkUser = Depends(get_current_user)
) -> ChatResponse:
    """
    Send a message to the AI Counsellor.
    
    Requires completed onboarding.
    Returns full AI response.
    """
    check_onboarding_required(user.user_id)
    
    # Convert messages to API format
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    
    # Get user context for personalization
    context = get_user_context(user.user_id)
    
    # Get AI response
    response_text = await chat_with_counsellor(messages, context)
    
    return ChatResponse(
        message=ChatMessage(role="assistant", content=response_text),
        onboarding_complete=True
    )


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    user: ClerkUser = Depends(get_current_user)
):
    """
    Stream a chat response from the AI Counsellor.
    
    Requires completed onboarding.
    Returns Server-Sent Events stream.
    """
    check_onboarding_required(user.user_id)
    
    # Convert messages to API format
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    
    # Get user context for personalization
    context = get_user_context(user.user_id)
    
    async def generate():
        async for chunk in stream_chat_with_counsellor(messages, context):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/status")
async def counsellor_status(
    user: ClerkUser = Depends(get_current_user)
) -> dict:
    """
    Check if AI Counsellor is available.
    
    Returns availability and context summary.
    """
    onboarding_complete = is_onboarding_complete(user.user_id)
    
    return {
        "available": onboarding_complete,
        "reason": None if onboarding_complete else "Complete onboarding first",
        "has_context": get_user_context(user.user_id) is not None,
    }
