"""
Onboarding Service

Business logic for user onboarding data management.
"""

from typing import Optional

from models.onboarding import OnboardingData, OnboardingStatus, OnboardingPartialUpdate


# In-memory storage for MVP (replace with database in production)
_onboarding_store: dict[str, OnboardingData] = {}


def get_onboarding_data(user_id: str) -> Optional[OnboardingData]:
    """Get onboarding data for a user."""
    return _onboarding_store.get(user_id)


def save_onboarding_data(user_id: str, data: OnboardingData) -> OnboardingData:
    """Save complete onboarding data for a user."""
    _onboarding_store[user_id] = data
    return data


def update_onboarding_data(
    user_id: str,
    update: OnboardingPartialUpdate
) -> Optional[OnboardingData]:
    """
    Update partial onboarding data.
    
    Merges with existing data if present.
    """
    existing = _onboarding_store.get(user_id)
    
    if existing is None:
        # Can't do partial update without existing data
        return None
    
    # Merge updates
    updated_dict = existing.model_dump()
    
    if update.academic_background:
        updated_dict["academic_background"] = update.academic_background.model_dump()
    if update.study_goal:
        updated_dict["study_goal"] = update.study_goal.model_dump()
    if update.budget:
        updated_dict["budget"] = update.budget.model_dump()
    if update.exams_readiness:
        updated_dict["exams_readiness"] = update.exams_readiness.model_dump()
    
    updated = OnboardingData(**updated_dict)
    _onboarding_store[user_id] = updated
    
    return updated


def calculate_completion(data: Optional[OnboardingData]) -> tuple[int, list[str]]:
    """
    Calculate onboarding completion percentage and missing sections.
    
    Returns:
        Tuple of (percentage, missing_sections)
    """
    if data is None:
        return 0, ["academic_background", "study_goal", "budget", "exams_readiness"]
    
    # All sections are required, so if we have data, it's 100%
    return 100, []


def get_onboarding_status(user_id: str) -> OnboardingStatus:
    """Get onboarding status for a user."""
    data = get_onboarding_data(user_id)
    percentage, missing = calculate_completion(data)
    
    return OnboardingStatus(
        user_id=user_id,
        is_complete=percentage == 100,
        completion_percentage=percentage,
        missing_sections=missing,
        data=data,
    )


def is_onboarding_complete(user_id: str) -> bool:
    """Check if user has completed onboarding."""
    data = get_onboarding_data(user_id)
    return data is not None
