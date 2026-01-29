"""
University Service

Fetches university data from Hipo API and generates recommendations.
"""

from typing import Optional
import httpx

from config import get_settings
from models.university import University, UniversityRecommendation
from models.onboarding import OnboardingData
from ai_engine.rag_pipeline import (
    batch_classify_universities,
    build_student_profile_for_classification,
)


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
    Get AI-powered university recommendations based on user profile.
    
    Uses Llama 3.3 70B via Groq to intelligently classify universities
    as Dream/Target/Safe based on the student's profile.
    
    Args:
        profile: User's onboarding data
        countries: Filter by countries
        limit: Maximum number of recommendations
    
    Returns:
        List of university recommendations with AI-generated classifications
    """
    # Get universities for preferred countries
    target_countries = countries or (
        profile.study_goal.preferred_countries if profile else ["United States", "United Kingdom"]
    )
    
    all_universities = []
    for country in target_countries[:3]:  # Limit to 3 countries for API efficiency
        universities = await search_universities(country=country)
        all_universities.extend(universities[:20])  # Limit per country
    
    # Limit total universities to process
    universities_to_classify = all_universities[:limit * 2]  # Get more than needed for better selection
    
    # Use AI classification if profile is available
    if profile:
        # Build student profile for AI classification
        student_profile = build_student_profile_for_classification(
            profile.model_dump() if hasattr(profile, 'model_dump') else profile.__dict__
        )
        
        # Convert universities to dict format for AI
        university_dicts = [
            {
                "name": uni.name,
                "country": uni.country,
                "domains": uni.domains,
                "web_pages": uni.web_pages,
                "state_province": uni.state_province,
            }
            for uni in universities_to_classify
        ]
        
        # Run AI classification in parallel
        classifications = await batch_classify_universities(
            student_profile=student_profile,
            universities=university_dicts
        )
        
        # Build recommendations from AI classifications
        recommendations = []
        for result in classifications[:limit]:
            university_data = result["university"]
            classification = result["classification"]
            
            # Reconstruct University object
            university = University(
                name=university_data["name"],
                country=university_data["country"],
                alpha_two_code=next(
                    (u.alpha_two_code for u in universities_to_classify if u.name == university_data["name"]),
                    ""
                ),
                domains=university_data["domains"],
                web_pages=university_data["web_pages"],
                state_province=university_data.get("state_province"),
            )
            
            # Map AI confidence to acceptance chance
            confidence = classification.get("confidence", 0.5)
            if confidence >= 0.7:
                acceptance_chance = "high"
            elif confidence >= 0.4:
                acceptance_chance = "medium"
            else:
                acceptance_chance = "low"
            
            recommendation = UniversityRecommendation(
                university=university,
                category=classification.get("category", "target"),
                fit_reasons=classification.get("reasons", []),
                risks=classification.get("risks", []),
                cost_level=estimate_cost_level(university.country),
                acceptance_chance=acceptance_chance,
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    else:
        # Fallback to simple heuristics if no profile
        recommendations = []
        for university in universities_to_classify[:limit]:
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

