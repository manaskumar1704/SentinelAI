"""
Onboarding Router

API endpoints for user onboarding data with database persistence.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
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
    ensure_user_exists,
)


router = APIRouter()


@router.get("")
async def get_onboarding(
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OnboardingStatus:
    """
    Get current onboarding status.
    
    Returns completion percentage and existing data.
    """
    # Ensure user exists in database
    await ensure_user_exists(db, user.user_id, user.email, user.full_name)
    
    return await get_onboarding_status(db, user.user_id)


@router.post("")
async def submit_onboarding(
    data: OnboardingData,
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OnboardingStatus:
    """
    Submit complete onboarding data.
    
    This replaces any existing onboarding data.
    After completion, the AI Counsellor is unlocked.
    """
    # Ensure user exists in database
    await ensure_user_exists(db, user.user_id, user.email, user.full_name)
    
    await save_onboarding_data(db, user.user_id, data)
    return await get_onboarding_status(db, user.user_id)


@router.patch("")
async def update_onboarding(
    update: OnboardingPartialUpdate,
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OnboardingStatus:
    """
    Update partial onboarding data.
    
    Only provided sections will be updated.
    Requires existing onboarding data.
    """
    result = await update_onboarding_data(db, user.user_id, update)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No existing onboarding data to update. Use POST to submit initial data."
        )
    
    return await get_onboarding_status(db, user.user_id)


@router.get("/status")
async def check_completion(
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Quick check if onboarding is complete.
    
    Used to gate access to AI Counsellor.
    """
    onboarding_status = await get_onboarding_status(db, user.user_id)
    
    return {
        "is_complete": onboarding_status.is_complete,
        "can_access_counsellor": onboarding_status.is_complete,
        "completion_percentage": onboarding_status.completion_percentage,
    }
