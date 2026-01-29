"""
SQLModel Database Models

Defines persistent database tables for SentinelAI.
These models are used for PostgreSQL storage via Supabase.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON


class UserDB(SQLModel, table=True):
    """
    Persistent user data table.
    
    Stores user profile information synced from Supabase Auth.
    """
    __tablename__ = "users"
    
    id: str = Field(primary_key=True)  # Supabase Auth user ID
    email: str = Field(index=True)
    full_name: Optional[str] = None
    onboarding_completed: bool = Field(default=False)
    current_stage: int = Field(default=1, ge=1, le=4)  # PLAN.md stages

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OnboardingDB(SQLModel, table=True):
    """
    User onboarding data table.
    
    Stores the complete onboarding form data as JSON.
    """
    __tablename__ = "onboarding"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True, foreign_key="users.id")
    
    # Store onboarding sections as JSON for flexibility
    academic_background: dict = Field(default_factory=dict, sa_column=Column(JSON))
    study_goal: dict = Field(default_factory=dict, sa_column=Column(JSON))
    budget: dict = Field(default_factory=dict, sa_column=Column(JSON))
    exams_readiness: dict = Field(default_factory=dict, sa_column=Column(JSON))
    
    is_complete: bool = Field(default=False)
    completion_percentage: int = Field(default=0, ge=0, le=100)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ShortlistDB(SQLModel, table=True):
    """
    User university shortlist table.
    
    Stores shortlisted universities with category and lock status.
    """
    __tablename__ = "shortlist"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    
    # University data
    university_name: str
    country: str
    university_data: dict = Field(default_factory=dict, sa_column=Column(JSON))
    
    # Shortlist metadata
    category: str = Field(default="target")  # dream, target, safe
    is_locked: bool = Field(default=False)
    
    added_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Ensure unique constraint on user + university combination."""
        pass
