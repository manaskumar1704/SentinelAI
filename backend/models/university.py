"""
University Models

Pydantic models for university data and recommendations.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class University(BaseModel):
    """University data model from Hipo API."""
    name: str
    country: str
    alpha_two_code: str
    domains: list[str] = Field(default_factory=list)
    web_pages: list[str] = Field(default_factory=list)
    state_province: Optional[str] = None


class UniversityRecommendation(BaseModel):
    """University recommendation with fit analysis."""
    university: University
    category: Literal["dream", "target", "safe"]
    fit_reasons: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    cost_level: Literal["low", "medium", "high"]
    acceptance_chance: Literal["low", "medium", "high"]


class ShortlistedUniversity(BaseModel):
    """University in user's shortlist."""
    university: University
    category: Literal["dream", "target", "safe"]
    is_locked: bool = False
    added_at: str  # ISO datetime string


class UniversitySearchParams(BaseModel):
    """Search parameters for university API."""
    name: Optional[str] = None
    country: Optional[str] = None


class ShortlistRequest(BaseModel):
    """Request to add university to shortlist."""
    university_name: str
    country: str
    category: Literal["dream", "target", "safe"]


class LockRequest(BaseModel):
    """Request to lock a university."""
    university_name: str
    country: str
