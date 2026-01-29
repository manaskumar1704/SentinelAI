"""
AI Engine Tests

Tests for AI prompts, AI Classification pipeline, and Groq integration.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock


class TestAIEngineClient:
    """Tests for AI engine client."""
    
    def test_model_is_correct(self):
        """Verify client uses llama-3.3-70b-versatile model."""
        from ai_engine import client
        
        # Read the source file and verify model name
        import inspect
        source = inspect.getsource(client.generate_response)
        assert "llama-3.3-70b-versatile" in source
    
    def test_get_groq_client_requires_api_key(self):
        """Test that missing API key raises error."""
        from ai_engine.client import get_groq_client
        
        with patch("ai_engine.client.get_settings") as mock_settings:
            mock_settings.return_value.groq_api_key = ""
            
            # Reset the global client
            import ai_engine.client
            ai_engine.client._client = None
            
            with pytest.raises(ValueError) as exc_info:
                get_groq_client()
            
            assert "GROQ_API_KEY not set" in str(exc_info.value)


class TestPrompts:
    """Tests for prompt templates."""
    
    def test_get_system_prompt(self):
        """Test system prompt formatting."""
        from ai_engine.prompts import get_system_prompt
        
        profile = {
            "gpa": 3.5,
            "major": "Computer Science",
            "target_degree": "Masters"
        }
        
        prompt = get_system_prompt(profile, "university_selection")
        
        assert "SentinelAI Counsellor" in prompt
        assert "gpa" in prompt.lower()
        assert "3.5" in prompt
        assert "university_selection" in prompt
    
    def test_get_classifier_prompt(self):
        """Test university classifier prompt formatting."""
        from ai_engine.prompts import get_classifier_prompt
        
        student = {"gpa": 3.5, "target_degree": "Masters"}
        university = {"name": "MIT", "country": "USA"}
        
        prompt = get_classifier_prompt(student, university)
        
        assert "Dream" in prompt
        assert "Target" in prompt
        assert "Safe" in prompt
        assert "MIT" in prompt
    
    def test_get_timeline_prompt(self):
        """Test timeline advisor prompt formatting."""
        from ai_engine.prompts import get_timeline_prompt
        
        prompt = get_timeline_prompt(
            target_intake="Fall 2027",
            current_date="January 2026",
            exams_status={"gre": "not_started"},
            documents_status={"sop": "draft"}
        )
        
        assert "Fall 2027" in prompt
        assert "January 2026" in prompt
    
    def test_get_sop_review_prompt(self):
        """Test SOP review prompt formatting."""
        from ai_engine.prompts import get_sop_review_prompt
        
        prompt = get_sop_review_prompt(
            student_profile={"major": "CS"},
            target_program="MS Computer Science at Stanford",
            sop_content="Ever since I was a child..."
        )
        
        assert "Stanford" in prompt
        assert "Ever since" in prompt


class TestAIClassificationPipeline:
    """Tests for AI Classification pipeline."""
    
    def test_build_student_profile_for_classification_empty(self):
        """Test profile building with empty data."""
        from ai_engine.rag_pipeline import build_student_profile_for_classification
        
        profile = build_student_profile_for_classification(None)
        
        assert profile["gpa"] is None
        assert profile["education_level"] == "unknown"
    
    def test_build_student_profile_for_classification_full(self):
        """Test profile building with full data."""
        from ai_engine.rag_pipeline import build_student_profile_for_classification
        
        onboarding_data = {
            "academic_background": {
                "gpa": 3.5,
                "current_education_level": "bachelors",
                "degree_major": "Computer Science"
            },
            "study_goal": {
                "intended_degree": "masters",
                "field_of_study": "AI",
                "target_intake_year": 2027,
                "preferred_countries": ["USA", "UK"]
            },
            "exams_readiness": {
                "ielts_toefl_score": 7.5,
                "gre_gmat_score": 320
            },
            "budget": {
                "budget_range_per_year": "40k_60k"
            }
        }
        
        profile = build_student_profile_for_classification(onboarding_data)
        
        assert profile["gpa"] == 3.5
        assert profile["education_level"] == "bachelors"
        assert profile["target_degree"] == "masters"
        assert profile["field_of_study"] == "AI"
        assert profile["test_scores"]["ielts_toefl"] == 7.5
        assert profile["budget"] == "40k_60k"
    
    @pytest.mark.asyncio
    async def test_classify_university_with_ai_mock(self):
        """Test university classification with mocked Groq client."""
        from ai_engine.rag_pipeline import classify_university_with_ai
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"category": "target", "confidence": 0.7, "reasons": ["Good fit"], "risks": []}'
        
        with patch("ai_engine.rag_pipeline.get_async_groq_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client
            
            result = await classify_university_with_ai(
                student_profile={"gpa": 3.5},
                university_data={"name": "Test University"}
            )
            
            assert result["category"] == "target"
            assert result["confidence"] == 0.7
            assert "Good fit" in result["reasons"]
    
    @pytest.mark.asyncio
    async def test_classify_university_fallback_on_json_error(self):
        """Test fallback classification when JSON parsing fails."""
        from ai_engine.rag_pipeline import classify_university_with_ai
        
        # Response with malformed JSON but contains "dream"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a DREAM university for you!"
        
        with patch("ai_engine.rag_pipeline.get_async_groq_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client
            
            result = await classify_university_with_ai(
                student_profile={"gpa": 3.5},
                university_data={"name": "MIT"}
            )
            
            # Should fallback to parsing keywords
            assert result["category"] == "dream"


class TestGroqService:
    """Tests for Groq service integration."""
    
    def test_groq_service_uses_correct_model(self):
        """Verify services/groq_client.py uses llama-3.3-70b-versatile."""
        from services import groq_client
        
        import inspect
        source = inspect.getsource(groq_client.chat_with_counsellor)
        assert "llama-3.3-70b-versatile" in source
    
    def test_build_user_context_empty(self):
        """Test context building with no profile data."""
        from services.groq_client import build_user_context
        
        context = build_user_context(None)
        
        assert "No profile data available" in context
    
    def test_build_user_context_full(self):
        """Test context building with full profile data."""
        from services.groq_client import build_user_context
        
        profile_data = {
            "academic_background": {
                "current_education_level": "bachelors",
                "degree_major": "Computer Science",
                "graduation_year": 2024,
                "gpa": 3.5
            },
            "study_goal": {
                "intended_degree": "masters",
                "field_of_study": "AI",
                "target_intake_year": 2025,
                "preferred_countries": ["USA", "UK"]
            }
        }
        
        context = build_user_context(profile_data)
        
        assert "bachelors" in context
        assert "Computer Science" in context
        assert "3.5" in context
        assert "masters" in context
