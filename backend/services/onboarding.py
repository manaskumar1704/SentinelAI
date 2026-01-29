"""
Onboarding Service

Business logic for user onboarding data management with database persistence.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.onboarding import OnboardingData, OnboardingStatus, OnboardingPartialUpdate
from models.db_models import OnboardingDB, UserDB


async def get_onboarding_data(db: AsyncSession, user_id: str) -> Optional[OnboardingData]:
    """Get onboarding data for a user from database."""
    result = await db.execute(
        select(OnboardingDB).where(OnboardingDB.user_id == user_id)
    )
    onboarding = result.scalar_one_or_none()
    
    if onboarding is None:
        return None
    
    # Convert database model to Pydantic model
    return OnboardingData(
        academic_background=onboarding.academic_background,
        study_goal=onboarding.study_goal,
        budget=onboarding.budget,
        exams_readiness=onboarding.exams_readiness,
    )


async def save_onboarding_data(
    db: AsyncSession, user_id: str, data: OnboardingData
) -> OnboardingData:
    """Save complete onboarding data for a user to database."""
    
    # Check if onboarding record exists
    result = await db.execute(
        select(OnboardingDB).where(OnboardingDB.user_id == user_id)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing record
        existing.academic_background = data.academic_background.model_dump()
        existing.study_goal = data.study_goal.model_dump()
        existing.budget = data.budget.model_dump()
        existing.exams_readiness = data.exams_readiness.model_dump()
        existing.is_complete = True
        existing.completion_percentage = 100
        existing.updated_at = datetime.utcnow()
        db.add(existing)
    else:
        # Create new record
        onboarding = OnboardingDB(
            user_id=user_id,
            academic_background=data.academic_background.model_dump(),
            study_goal=data.study_goal.model_dump(),
            budget=data.budget.model_dump(),
            exams_readiness=data.exams_readiness.model_dump(),
            is_complete=True,
            completion_percentage=100,
        )
        db.add(onboarding)
    
    # Also update user's onboarding status
    user_result = await db.execute(
        select(UserDB).where(UserDB.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    if user:
        user.onboarding_completed = True
        user.updated_at = datetime.utcnow()
        db.add(user)
    
    await db.commit()
    return data


async def update_onboarding_data(
    db: AsyncSession, user_id: str, update: OnboardingPartialUpdate
) -> Optional[OnboardingData]:
    """
    Update partial onboarding data.
    
    Merges with existing data if present.
    """
    result = await db.execute(
        select(OnboardingDB).where(OnboardingDB.user_id == user_id)
    )
    existing = result.scalar_one_or_none()
    
    if existing is None:
        return None
    
    # Merge updates
    if update.academic_background:
        existing.academic_background = update.academic_background.model_dump()
    if update.study_goal:
        existing.study_goal = update.study_goal.model_dump()
    if update.budget:
        existing.budget = update.budget.model_dump()
    if update.exams_readiness:
        existing.exams_readiness = update.exams_readiness.model_dump()
    
    existing.updated_at = datetime.utcnow()
    db.add(existing)
    await db.commit()
    
    return OnboardingData(
        academic_background=existing.academic_background,
        study_goal=existing.study_goal,
        budget=existing.budget,
        exams_readiness=existing.exams_readiness,
    )


def calculate_completion(data: Optional[OnboardingData]) -> tuple[int, list[str]]:
    """
    Calculate onboarding completion percentage and missing sections.
    
    Returns:
        Tuple of (percentage, missing_sections)
    """
    if data is None:
        return 0, ["academic_background", "study_goal", "budget", "exams_readiness"]
    
    return 100, []


async def get_onboarding_status(db: AsyncSession, user_id: str) -> OnboardingStatus:
    """Get onboarding status for a user."""
    data = await get_onboarding_data(db, user_id)
    percentage, missing = calculate_completion(data)
    
    return OnboardingStatus(
        user_id=user_id,
        is_complete=percentage == 100,
        completion_percentage=percentage,
        missing_sections=missing,
        data=data,
    )


async def is_onboarding_complete(db: AsyncSession, user_id: str) -> bool:
    """Check if user has completed onboarding."""
    data = await get_onboarding_data(db, user_id)
    return data is not None


async def ensure_user_exists(db: AsyncSession, user_id: str, email: Optional[str] = None, full_name: Optional[str] = None) -> UserDB:
    """Ensure user exists in database, create if not."""
    result = await db.execute(
        select(UserDB).where(UserDB.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        user = UserDB(
            id=user_id,
            email=email or "",
            full_name=full_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    return user
