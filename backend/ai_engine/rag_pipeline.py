"""
AI Classification Pipeline for University Recommendations

Uses Llama 3.3 70B via Groq for AI-powered university classification
and recommendation explainability.

Note: This is Context-Augmented Generation, not Retrieval-Augmented Generation (RAG).
For small university lists, passing full context is more accurate than vector retrieval.
"""

import asyncio
import json
from typing import Optional
from groq import AsyncGroq

from config import get_settings
from ai_engine.prompts import get_classifier_prompt, get_recommendation_explainer_prompt

# Singleton pattern for AsyncGroq client
_async_client: AsyncGroq = None


def get_async_groq_client() -> AsyncGroq:
    """Get singleton async Groq client (reuses connections)."""
    global _async_client
    if _async_client is None:
        settings = get_settings()
        _async_client = AsyncGroq(api_key=settings.groq_api_key)
    return _async_client


async def classify_university_with_ai(
    student_profile: dict,
    university_data: dict,
    model: str = "llama-3.3-70b-versatile"
) -> dict:
    """
    Use AI to classify a university as Dream, Target, or Safe.
    
    Args:
        student_profile: Student's onboarding data
        university_data: University information
        model: Groq model to use
    
    Returns:
        Classification result with category, confidence, and reasons
    """
    client = get_async_groq_client()
    
    prompt = get_classifier_prompt(student_profile, university_data)
    
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a university admissions expert. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # Lower temperature for more deterministic output
        max_tokens=512,
    )
    
    content = response.choices[0].message.content
    
    # Parse JSON response
    try:
        # Handle markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content.strip())
        
        # Ensure required fields
        if "category" not in result:
            result["category"] = "target"
        if "confidence" not in result:
            result["confidence"] = 0.5
        if "reasons" not in result:
            result["reasons"] = []
        if "risks" not in result:
            result["risks"] = []
            
        return result
    except json.JSONDecodeError:
        # Fallback to simple parsing
        content_lower = content.lower()
        if "dream" in content_lower:
            category = "dream"
        elif "safe" in content_lower:
            category = "safe"
        else:
            category = "target"
        
        return {
            "category": category,
            "confidence": 0.5,
            "reasons": ["AI classification based on profile match"],
            "risks": [],
            "recommendation": "Please review university details for more information."
        }


async def get_recommendation_explanation(
    student_profile: dict,
    university_name: str,
    university_country: str,
    category: str,
    fit_reasons: list[str],
    risks: list[str],
    model: str = "llama-3.3-70b-versatile"
) -> str:
    """
    Generate a human-friendly explanation for a university recommendation.
    
    Returns:
        Explanation text
    """
    client = get_async_groq_client()
    
    prompt = get_recommendation_explainer_prompt(
        student_profile=student_profile,
        university_name=university_name,
        university_country=university_country,
        category=category,
        fit_reasons=fit_reasons,
        risks=risks
    )
    
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an encouraging study abroad counselor. Write warm, personalized explanations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=512,
    )
    
    return response.choices[0].message.content


async def batch_classify_universities(
    student_profile: dict,
    universities: list[dict],
    model: str = "llama-3.3-70b-versatile"
) -> list[dict]:
    """
    Classify multiple universities for a student in parallel.
    
    Uses asyncio.gather for parallel execution, significantly improving
    performance when classifying many universities.
    
    Returns:
        List of classification results with university data included
    """
    # Create classification tasks for all universities
    async def classify_single(university: dict) -> dict:
        classification = await classify_university_with_ai(
            student_profile=student_profile,
            university_data=university,
            model=model
        )
        return {
            "university": university,
            "classification": classification
        }
    
    # Run all classifications in parallel
    tasks = [classify_single(uni) for uni in universities]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out any failed classifications and log errors
    valid_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # Log error but continue with other results
            print(f"Classification failed for university {i}: {result}")
            # Add fallback classification
            valid_results.append({
                "university": universities[i],
                "classification": {
                    "category": "target",
                    "confidence": 0.3,
                    "reasons": ["Classification failed, defaulting to target"],
                    "risks": ["Unable to perform AI analysis"],
                    "recommendation": "Please review university details manually."
                }
            })
        else:
            valid_results.append(result)
    
    return valid_results


def build_student_profile_for_classification(onboarding_data: Optional[dict]) -> dict:
    """
    Build a structured student profile for AI classification.
    
    Args:
        onboarding_data: Raw onboarding data from database
    
    Returns:
        Structured profile for AI classification
    """
    if not onboarding_data:
        return {
            "gpa": None,
            "education_level": "unknown",
            "target_degree": "unknown",
            "field_of_study": "unknown",
            "test_scores": {},
            "budget": "unknown"
        }
    
    profile = {}
    
    # Academic background
    if "academic_background" in onboarding_data:
        ab = onboarding_data["academic_background"]
        profile["gpa"] = ab.get("gpa")
        profile["education_level"] = ab.get("current_education_level", "unknown")
        profile["major"] = ab.get("degree_major", "unknown")
    
    # Study goals
    if "study_goal" in onboarding_data:
        sg = onboarding_data["study_goal"]
        profile["target_degree"] = sg.get("intended_degree", "unknown")
        profile["field_of_study"] = sg.get("field_of_study", "unknown")
        profile["target_intake"] = sg.get("target_intake_year")
        profile["preferred_countries"] = sg.get("preferred_countries", [])
    
    # Test scores
    if "exams_readiness" in onboarding_data:
        er = onboarding_data["exams_readiness"]
        profile["test_scores"] = {
            "ielts_toefl": er.get("ielts_toefl_score"),
            "gre_gmat": er.get("gre_gmat_score")
        }
    
    # Budget
    if "budget" in onboarding_data:
        profile["budget"] = onboarding_data["budget"].get("budget_range_per_year", "unknown")
    
    return profile
