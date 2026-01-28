"""
User Models

Pydantic models for user data and profiles.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base user model."""
    email: str
    full_name: str


class UserProfile(UserBase):
    """Complete user profile."""
    id: str
    created_at: datetime
    onboarding_completed: bool = False
    profile_strength: Optional[dict] = None
    current_stage: int = 1  # 1-4 based on PLAN.md stages


class UserProfileUpdate(BaseModel):
    """User profile update model."""
    full_name: Optional[str] = None
    email: Optional[str] = None


class ClerkUser(BaseModel):
    """User data from Clerk JWT."""
    user_id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
