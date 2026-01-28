"""
User Router

API endpoints for user profile management.
"""

from datetime import datetime
from fastapi import APIRouter, Depends

from middleware.auth import get_current_user
from models.user import ClerkUser, UserProfile
from services.onboarding import is_onboarding_complete


router = APIRouter()

# In-memory user store for MVP
_user_store: dict[str, UserProfile] = {}


def get_or_create_user_profile(clerk_user: ClerkUser) -> UserProfile:
    """Get existing profile or create new one from Clerk user."""
    if clerk_user.user_id not in _user_store:
        _user_store[clerk_user.user_id] = UserProfile(
            id=clerk_user.user_id,
            email=clerk_user.email or "",
            full_name=clerk_user.full_name or "User",
            created_at=datetime.utcnow(),
            onboarding_completed=False,
        )
    
    # Update onboarding status
    profile = _user_store[clerk_user.user_id]
    profile.onboarding_completed = is_onboarding_complete(clerk_user.user_id)
    
    return profile


@router.get("/profile")
async def get_profile(
    user: ClerkUser = Depends(get_current_user)
) -> UserProfile:
    """
    Get the current user's profile.
    
    Returns user profile with onboarding status.
    """
    return get_or_create_user_profile(user)


@router.get("/stage")
async def get_current_stage(
    user: ClerkUser = Depends(get_current_user)
) -> dict:
    """
    Get the user's current stage in the application flow.
    
    Stages (from PLAN.md):
    1. Building Profile (onboarding)
    2. Discovering Universities
    3. Finalizing Universities (locking)
    4. Preparing Applications
    """
    profile = get_or_create_user_profile(user)
    
    # Determine stage based on progress
    if not profile.onboarding_completed:
        stage = 1
        stage_name = "Building Profile"
    else:
        # For MVP, default to stage 2 after onboarding
        stage = 2
        stage_name = "Discovering Universities"
    
    return {
        "stage": stage,
        "stage_name": stage_name,
        "stages": [
            {"number": 1, "name": "Building Profile"},
            {"number": 2, "name": "Discovering Universities"},
            {"number": 3, "name": "Finalizing Universities"},
            {"number": 4, "name": "Preparing Applications"},
        ]
    }
