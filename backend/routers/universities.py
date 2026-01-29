"""
Universities Router

API endpoints for university search, recommendations, and shortlist with database persistence.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
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
from services.shortlist import (
    get_user_shortlist,
    add_to_shortlist,
    lock_university,
    remove_from_shortlist,
)


router = APIRouter()


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
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[UniversityRecommendation]:
    """
    Get personalized university recommendations.
    
    Based on user's onboarding profile.
    Returns universities categorized as Dream/Target/Safe.
    """
    profile = await get_onboarding_data(db, user.user_id)
    
    recs = await get_recommendations(profile, limit=10)
    return recs


@router.get("/shortlist")
async def get_shortlist_endpoint(
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ShortlistedUniversity]:
    """
    Get user's shortlisted universities.
    
    Returns all universities the user has saved.
    """
    return await get_user_shortlist(db, user.user_id)


@router.post("/shortlist")
async def add_to_user_shortlist(
    request: ShortlistRequest,
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
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
    
    try:
        shortlisted = await add_to_shortlist(
            db, user.user_id, university, request.category
        )
        return shortlisted
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/lock")
async def lock_university_endpoint(
    request: LockRequest,
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ShortlistedUniversity:
    """
    Lock a university from the shortlist.
    
    Locking a university unlocks application guidance for it.
    User must have at least one locked university to access Stage 4.
    """
    result = await lock_university(
        db, user.user_id, request.university_name, request.country
    )
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="University not found in shortlist. Add it first."
        )
    
    return result


@router.delete("/shortlist/{university_name}")
async def remove_from_shortlist_endpoint(
    university_name: str,
    user: ClerkUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Remove a university from the shortlist.
    
    Cannot remove locked universities without explicit unlock.
    """
    try:
        removed = await remove_from_shortlist(db, user.user_id, university_name)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="University not found in shortlist"
            )
        return {"message": "University removed from shortlist"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
