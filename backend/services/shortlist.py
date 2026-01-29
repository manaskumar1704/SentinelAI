"""
Shortlist Service

Business logic for university shortlist management with database persistence.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_models import ShortlistDB
from models.university import University, ShortlistedUniversity


async def get_user_shortlist(db: AsyncSession, user_id: str) -> list[ShortlistedUniversity]:
    """Get user's shortlisted universities from database."""
    result = await db.execute(
        select(ShortlistDB).where(ShortlistDB.user_id == user_id)
    )
    shortlist_items = result.scalars().all()
    
    return [
        ShortlistedUniversity(
            university=University(**item.university_data),
            category=item.category,
            is_locked=item.is_locked,
            added_at=item.added_at.isoformat(),
        )
        for item in shortlist_items
    ]


async def add_to_shortlist(
    db: AsyncSession, 
    user_id: str, 
    university: University,
    category: str = "target"
) -> ShortlistedUniversity:
    """Add university to user's shortlist in database."""
    
    # Check if already exists
    result = await db.execute(
        select(ShortlistDB).where(
            and_(
                ShortlistDB.user_id == user_id,
                ShortlistDB.university_name == university.name,
                ShortlistDB.country == university.country,
            )
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise ValueError("University already in shortlist")
    
    shortlist_item = ShortlistDB(
        user_id=user_id,
        university_name=university.name,
        country=university.country,
        university_data=university.model_dump(),
        category=category,
        is_locked=False,
    )
    
    db.add(shortlist_item)
    await db.commit()
    await db.refresh(shortlist_item)
    
    return ShortlistedUniversity(
        university=university,
        category=category,
        is_locked=False,
        added_at=shortlist_item.added_at.isoformat(),
    )


async def lock_university(
    db: AsyncSession,
    user_id: str,
    university_name: str,
    country: str
) -> Optional[ShortlistedUniversity]:
    """Lock a university in the shortlist."""
    result = await db.execute(
        select(ShortlistDB).where(
            and_(
                ShortlistDB.user_id == user_id,
                ShortlistDB.university_name.ilike(university_name),
                ShortlistDB.country.ilike(country),
            )
        )
    )
    item = result.scalar_one_or_none()
    
    if item is None:
        return None
    
    item.is_locked = True
    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return ShortlistedUniversity(
        university=University(**item.university_data),
        category=item.category,
        is_locked=item.is_locked,
        added_at=item.added_at.isoformat(),
    )


async def remove_from_shortlist(
    db: AsyncSession,
    user_id: str,
    university_name: str
) -> bool:
    """
    Remove a university from the shortlist.
    
    Returns True if removed, raises ValueError if locked.
    """
    result = await db.execute(
        select(ShortlistDB).where(
            and_(
                ShortlistDB.user_id == user_id,
                ShortlistDB.university_name.ilike(university_name),
            )
        )
    )
    item = result.scalar_one_or_none()
    
    if item is None:
        return False
    
    if item.is_locked:
        raise ValueError("Cannot remove locked university. Unlock first.")
    
    await db.delete(item)
    await db.commit()
    return True
