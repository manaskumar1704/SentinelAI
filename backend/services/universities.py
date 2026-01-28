"""
University Service

Fetches university data from Hipo API and generates recommendations.
"""

from typing import Optional
import httpx

from config import get_settings
from models.university import University, UniversityRecommendation
from models.onboarding import OnboardingData


async def search_universities(
    name: Optional[str] = None,
    country: Optional[str] = None
) -> list[University]:
    """
    Search universities using the Hipo API.
    
    Args:
        name: Optional university name to search
        country: Optional country filter
    
    Returns:
        List of matching universities
    """
    settings = get_settings()
    url = f"{settings.university_api_url}/search"
    
    params = {}
    if name:
        params["name"] = name
    if country:
        params["country"] = country
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            universities = []
            for item in data:
                universities.append(University(
                    name=item.get("name", ""),
                    country=item.get("country", ""),
                    alpha_two_code=item.get("alpha_two_code", ""),
                    domains=item.get("domains", []),
                    web_pages=item.get("web_pages", []),
                    state_province=item.get("state-province"),
                ))
            
            return universities
        except httpx.HTTPError as e:
            print(f"Error fetching universities: {e}")
            return []


def calculate_acceptance_chance(
    university: University,
    profile: Optional[OnboardingData]
) -> str:
    """
    Calculate acceptance chance based on profile.
    
    This is a simplified heuristic for MVP.
    """
    if not profile:
        return "medium"
    
    # Simple heuristic based on GPA
    gpa = profile.academic_background.gpa
    if gpa is None:
        return "medium"
    
    if gpa >= 3.7:
        return "high"
    elif gpa >= 3.3:
        return "medium"
    else:
        return "low"


def categorize_university(
    university: University,
    profile: Optional[OnboardingData]
) -> str:
    """
    Categorize university as dream, target, or safe.
    
    Simplified heuristic for MVP.
    """
    # For MVP, we use a simple random-like distribution
    # In production, this would use actual ranking data
    name_hash = hash(university.name) % 3
    
    if name_hash == 0:
        return "dream"
    elif name_hash == 1:
        return "target"
    else:
        return "safe"


def estimate_cost_level(country: str) -> str:
    """Estimate cost level based on country."""
    high_cost = ["united states", "united kingdom", "australia", "singapore"]
    medium_cost = ["canada", "netherlands", "ireland", "new zealand"]
    
    country_lower = country.lower()
    
    if any(c in country_lower for c in high_cost):
        return "high"
    elif any(c in country_lower for c in medium_cost):
        return "medium"
    else:
        return "low"


def generate_fit_reasons(
    university: University,
    profile: Optional[OnboardingData]
) -> list[str]:
    """Generate reasons why the university fits the student."""
    reasons = []
    
    if profile:
        # Country match
        if profile.study_goal.preferred_countries:
            if university.country.lower() in [c.lower() for c in profile.study_goal.preferred_countries]:
                reasons.append(f"Located in your preferred country: {university.country}")
        
        # Add generic reasons
        reasons.append(f"Offers programs in {profile.study_goal.field_of_study}")
        reasons.append(f"Strong {profile.study_goal.intended_degree} programs")
    else:
        reasons.append("Complete onboarding for personalized fit analysis")
    
    return reasons


def generate_risks(
    university: University,
    profile: Optional[OnboardingData]
) -> list[str]:
    """Generate potential risks for applying to this university."""
    risks = []
    
    cost = estimate_cost_level(university.country)
    if cost == "high":
        risks.append("High tuition and living costs")
    
    if profile:
        if profile.exams_readiness.ielts_toefl_status == "not_started":
            risks.append("English proficiency test not yet taken")
        if profile.exams_readiness.sop_status == "not_started":
            risks.append("Statement of Purpose not yet started")
    
    return risks


async def get_recommendations(
    profile: Optional[OnboardingData],
    countries: Optional[list[str]] = None,
    limit: int = 10
) -> list[UniversityRecommendation]:
    """
    Get university recommendations based on user profile.
    
    Args:
        profile: User's onboarding data
        countries: Filter by countries
        limit: Maximum number of recommendations
    
    Returns:
        List of university recommendations
    """
    # Get universities for preferred countries
    target_countries = countries or (
        profile.study_goal.preferred_countries if profile else ["United States", "United Kingdom"]
    )
    
    all_universities = []
    for country in target_countries[:3]:  # Limit to 3 countries for API efficiency
        universities = await search_universities(country=country)
        all_universities.extend(universities[:20])  # Limit per country
    
    # Generate recommendations
    recommendations = []
    for university in all_universities[:limit]:
        recommendation = UniversityRecommendation(
            university=university,
            category=categorize_university(university, profile),
            fit_reasons=generate_fit_reasons(university, profile),
            risks=generate_risks(university, profile),
            cost_level=estimate_cost_level(university.country),
            acceptance_chance=calculate_acceptance_chance(university, profile),
        )
        recommendations.append(recommendation)
    
    return recommendations
