"""
Onboarding Models

Pydantic models for onboarding data based on PLAN.md requirements.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class AcademicBackground(BaseModel):
    """A. Academic Background section."""
    current_education_level: Literal[
        "high_school", "bachelors", "masters", "phd", "other"
    ]
    degree_major: str
    graduation_year: int
    gpa: Optional[float] = Field(None, ge=0, le=10)


class StudyGoal(BaseModel):
    """B. Study Goal section."""
    intended_degree: Literal["bachelors", "masters", "mba", "phd"]
    field_of_study: str
    target_intake_year: int
    preferred_countries: list[str] = Field(default_factory=list, max_length=5)


class Budget(BaseModel):
    """C. Budget section."""
    budget_range_per_year: Literal[
        "under_10k", "10k_20k", "20k_40k", "40k_60k", "above_60k"
    ]
    funding_plan: Literal["self_funded", "scholarship_dependent", "loan_dependent"]


class ExamsReadiness(BaseModel):
    """D. Exams & Readiness section."""
    ielts_toefl_status: Literal["not_started", "preparing", "scheduled", "completed"]
    ielts_toefl_score: Optional[float] = None
    gre_gmat_status: Literal["not_started", "preparing", "scheduled", "completed", "not_required"]
    gre_gmat_score: Optional[int] = None
    sop_status: Literal["not_started", "draft", "ready"]


class OnboardingData(BaseModel):
    """Complete onboarding data model."""
    academic_background: AcademicBackground
    study_goal: StudyGoal
    budget: Budget
    exams_readiness: ExamsReadiness


class OnboardingStatus(BaseModel):
    """Onboarding completion status."""
    user_id: str
    is_complete: bool
    completion_percentage: int = Field(ge=0, le=100)
    missing_sections: list[str] = Field(default_factory=list)
    data: Optional[OnboardingData] = None


class OnboardingPartialUpdate(BaseModel):
    """Partial onboarding update."""
    academic_background: Optional[AcademicBackground] = None
    study_goal: Optional[StudyGoal] = None
    budget: Optional[Budget] = None
    exams_readiness: Optional[ExamsReadiness] = None
