"""
Database and Authentication Tests

Tests for Supabase database CRUD operations and auth verification.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from middleware.auth import verify_supabase_token
from models.onboarding import OnboardingData, AcademicBackground, StudyGoal, Budget, ExamsReadiness


class TestSupabaseAuth:
    """Tests for Supabase JWT authentication."""
    
    def test_missing_jwt_secret_raises_error(self):
        """Test that missing JWT secret raises 500 error."""
        with patch("middleware.auth.get_settings") as mock_settings:
            mock_settings.return_value.supabase_jwt_secret = ""
            
            with pytest.raises(HTTPException) as exc_info:
                verify_supabase_token("some_token")
            
            assert exc_info.value.status_code == 500
            assert "JWT secret not configured" in str(exc_info.value.detail)
    
    def test_expired_token_raises_401(self):
        """Test that expired tokens return 401."""
        import jwt as pyjwt
        from datetime import datetime, timedelta
        
        # Create an expired token
        secret = "test_secret"
        expired_payload = {
            "sub": "user_123",
            "aud": "authenticated",
            "exp": datetime.utcnow() - timedelta(hours=1),
        }
        expired_token = pyjwt.encode(expired_payload, secret, algorithm="HS256")
        
        with patch("middleware.auth.get_settings") as mock_settings:
            mock_settings.return_value.supabase_jwt_secret = secret
            
            with pytest.raises(HTTPException) as exc_info:
                verify_supabase_token(expired_token)
            
            assert exc_info.value.status_code == 401
            assert "expired" in str(exc_info.value.detail).lower()
    
    def test_invalid_audience_raises_401(self):
        """Test that wrong audience returns 401."""
        import jwt as pyjwt
        from datetime import datetime, timedelta
        
        secret = "test_secret"
        payload = {
            "sub": "user_123",
            "aud": "wrong_audience",
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        token = pyjwt.encode(payload, secret, algorithm="HS256")
        
        with patch("middleware.auth.get_settings") as mock_settings:
            mock_settings.return_value.supabase_jwt_secret = secret
            
            with pytest.raises(HTTPException) as exc_info:
                verify_supabase_token(token)
            
            assert exc_info.value.status_code == 401
    
    def test_valid_token_returns_user_data(self):
        """Test that valid tokens return correct user data."""
        import jwt as pyjwt
        from datetime import datetime, timedelta
        
        secret = "test_secret"
        payload = {
            "sub": "user_123",
            "email": "test@example.com",
            "aud": "authenticated",
            "exp": datetime.utcnow() + timedelta(hours=1),
            "user_metadata": {"full_name": "Test User"},
        }
        token = pyjwt.encode(payload, secret, algorithm="HS256")
        
        with patch("middleware.auth.get_settings") as mock_settings:
            mock_settings.return_value.supabase_jwt_secret = secret
            
            result = verify_supabase_token(token)
            
            assert result["user_id"] == "user_123"
            assert result["email"] == "test@example.com"
            assert result["full_name"] == "Test User"


class TestOnboardingModels:
    """Tests for onboarding data models."""
    
    def test_valid_onboarding_data(self):
        """Test creating valid onboarding data."""
        data = OnboardingData(
            academic_background=AcademicBackground(
                current_education_level="bachelors",
                degree_major="Computer Science",
                graduation_year=2024,
                gpa=3.5
            ),
            study_goal=StudyGoal(
                intended_degree="masters",
                field_of_study="Artificial Intelligence",
                target_intake_year=2025,
                preferred_countries=["USA", "UK"]
            ),
            budget=Budget(
                budget_range_per_year="20k_40k",
                funding_plan="self_funded"
            ),
            exams_readiness=ExamsReadiness(
                ielts_toefl_status="completed",
                ielts_toefl_score=7.5,
                gre_gmat_status="completed",
                gre_gmat_score=320,
                sop_status="draft"
            )
        )
        
        assert data.academic_background.current_education_level == "bachelors"
        assert data.study_goal.intended_degree == "masters"
        assert data.budget.budget_range_per_year == "20k_40k"
        assert data.exams_readiness.ielts_toefl_score == 7.5


class TestDatabaseModels:
    """Tests for SQLModel database models."""
    
    def test_user_db_model_creation(self):
        """Test UserDB model can be instantiated."""
        from models.db_models import UserDB
        
        user = UserDB(
            id="user_123",
            email="test@example.com",
            full_name="Test User",
        )
        
        assert user.id == "user_123"
        assert user.email == "test@example.com"
        assert user.onboarding_completed == False
        assert user.current_stage == 1
    
    def test_onboarding_db_model_creation(self):
        """Test OnboardingDB model can be instantiated."""
        from models.db_models import OnboardingDB
        
        onboarding = OnboardingDB(
            user_id="user_123",
            academic_background={"current_education_level": "bachelors"},
            study_goal={"intended_degree": "masters"},
            budget={"budget_range_per_year": "20k_40k"},
            exams_readiness={"ielts_toefl_status": "completed"},
        )
        
        assert onboarding.user_id == "user_123"
        assert onboarding.academic_background["current_education_level"] == "bachelors"
        assert onboarding.is_complete == False
    
    def test_shortlist_db_model_creation(self):
        """Test ShortlistDB model can be instantiated."""
        from models.db_models import ShortlistDB
        
        shortlist = ShortlistDB(
            user_id="user_123",
            university_name="MIT",
            country="USA",
            university_data={"name": "MIT", "country": "USA"},
            category="dream",
        )
        
        assert shortlist.university_name == "MIT"
        assert shortlist.category == "dream"
        assert shortlist.is_locked == False
