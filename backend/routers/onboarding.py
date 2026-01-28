"""
Onboarding Router

API endpoints for user onboarding data.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from middleware.auth import get_current_user
from models.user import ClerkUser
from models.onboarding import (
    OnboardingData,
    OnboardingStatus,
    OnboardingPartialUpdate,
)
from services.onboarding import (
    get_onboarding_status,
    save_onboarding_data,
    update_onboarding_data,
)


router = APIRouter()


@router.get("")
async def get_onboarding(
    user: ClerkUser = Depends(get_current_user)
) -> OnboardingStatus:
    """
    Get current onboarding status.
    
    Returns completion percentage and existing data.
    """
    return get_onboarding_status(user.user_id)


@router.post("")
async def submit_onboarding(
    data: OnboardingData,
    user: ClerkUser = Depends(get_current_user)
) -> OnboardingStatus:
    """
    Submit complete onboarding data.
    
    This replaces any existing onboarding data.
    After completion, the AI Counsellor is unlocked.
    """
    save_onboarding_data(user.user_id, data)
    return get_onboarding_status(user.user_id)


@router.patch("")
async def update_onboarding(
    update: OnboardingPartialUpdate,
    user: ClerkUser = Depends(get_current_user)
) -> OnboardingStatus:
    """
    Update partial onboarding data.
    
    Only provided sections will be updated.
    Requires existing onboarding data.
    """
    result = update_onboarding_data(user.user_id, update)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No existing onboarding data to update. Use POST to submit initial data."
        )
    
    return get_onboarding_status(user.user_id)


@router.get("/status")
async def check_completion(
    user: ClerkUser = Depends(get_current_user)
) -> dict:
    """
    Quick check if onboarding is complete.
    
    Used to gate access to AI Counsellor.
    """
    status = get_onboarding_status(user.user_id)
    
    return {
        "is_complete": status.is_complete,
        "can_access_counsellor": status.is_complete,
        "completion_percentage": status.completion_percentage,
    }
