"""
Universities Router

API endpoints for university search and recommendations.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from middleware.auth import get_current_user, get_optional_user
from models.user import ClerkUser
from models.university import (
    University,
    UniversityRecommendation,
    ShortlistedUniversity,
    ShortlistRequest,
    LockRequest,
)
from services.universities import search_universities, get_recommendations
from services.onboarding import get_onboarding_data


router = APIRouter()

# In-memory shortlist storage for MVP
_shortlist_store: dict[str, list[ShortlistedUniversity]] = {}


def get_user_shortlist(user_id: str) -> list[ShortlistedUniversity]:
    """Get user's shortlisted universities."""
    return _shortlist_store.get(user_id, [])


def add_to_shortlist(user_id: str, item: ShortlistedUniversity) -> None:
    """Add university to user's shortlist."""
    if user_id not in _shortlist_store:
        _shortlist_store[user_id] = []
    _shortlist_store[user_id].append(item)


class SearchParams(BaseModel):
    """University search parameters."""
    name: Optional[str] = None
    country: Optional[str] = None


@router.get("/search")
async def search(
    name: Optional[str] = None,
    country: Optional[str] = None,
    user: Optional[ClerkUser] = Depends(get_optional_user)
) -> list[University]:
    """
    Search universities by name and/or country.
    
    This endpoint is public but provides richer results for authenticated users.
    Uses the Hipo University API.
    """
    universities = await search_universities(name=name, country=country)
    return universities


@router.get("/recommendations")
async def recommendations(
    user: ClerkUser = Depends(get_current_user)
) -> list[UniversityRecommendation]:
    """
    Get personalized university recommendations.
    
    Based on user's onboarding profile.
    Returns universities categorized as Dream/Target/Safe.
    """
    profile = get_onboarding_data(user.user_id)
    
    recs = await get_recommendations(profile, limit=10)
    return recs


@router.get("/shortlist")
async def get_shortlist(
    user: ClerkUser = Depends(get_current_user)
) -> list[ShortlistedUniversity]:
    """
    Get user's shortlisted universities.
    
    Returns all universities the user has saved.
    """
    return get_user_shortlist(user.user_id)


@router.post("/shortlist")
async def add_to_user_shortlist(
    request: ShortlistRequest,
    user: ClerkUser = Depends(get_current_user)
) -> ShortlistedUniversity:
    """
    Add a university to the user's shortlist.
    
    The university is looked up and validated before adding.
    """
    # Search for the university to validate it exists
    universities = await search_universities(
        name=request.university_name,
        country=request.country
    )
    
    if not universities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"University '{request.university_name}' not found in {request.country}"
        )
    
    university = universities[0]
    
    # Check if already shortlisted
    current_shortlist = get_user_shortlist(user.user_id)
    for item in current_shortlist:
        if item.university.name == university.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="University already in shortlist"
            )
    
    shortlisted = ShortlistedUniversity(
        university=university,
        category=request.category,
        is_locked=False,
        added_at=datetime.utcnow().isoformat(),
    )
    
    add_to_shortlist(user.user_id, shortlisted)
    
    return shortlisted


@router.post("/lock")
async def lock_university(
    request: LockRequest,
    user: ClerkUser = Depends(get_current_user)
) -> ShortlistedUniversity:
    """
    Lock a university from the shortlist.
    
    Locking a university unlocks application guidance for it.
    User must have at least one locked university to access Stage 4.
    """
    shortlist = get_user_shortlist(user.user_id)
    
    for item in shortlist:
        if (item.university.name.lower() == request.university_name.lower() and
            item.university.country.lower() == request.country.lower()):
            item.is_locked = True
            return item
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="University not found in shortlist. Add it first."
    )


@router.delete("/shortlist/{university_name}")
async def remove_from_shortlist(
    university_name: str,
    user: ClerkUser = Depends(get_current_user)
) -> dict:
    """
    Remove a university from the shortlist.
    
    Cannot remove locked universities without explicit unlock.
    """
    if user.user_id not in _shortlist_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shortlist is empty"
        )
    
    for i, item in enumerate(_shortlist_store[user.user_id]):
        if item.university.name.lower() == university_name.lower():
            if item.is_locked:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot remove locked university. Unlock first."
                )
            _shortlist_store[user.user_id].pop(i)
            return {"message": "University removed from shortlist"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="University not found in shortlist"
    )
