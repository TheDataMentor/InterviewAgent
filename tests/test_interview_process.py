import pytest
from interview_process_agents import InterviewProcessManager
from unittest.mock import patch, AsyncMock

@pytest.fixture
def interview_manager():
    """Create an interview manager instance for testing"""
    return InterviewProcessManager(openai_api_key="test_key")

@pytest.mark.asyncio
class TestInterviewProcess:
    async def test_analyze_job_description(self, interview_manager):
        """Test job description analysis"""
        job_description = """
        Senior Data Scientist position requiring Python, SQL, and ML expertise.
        """
        
        # Create mock response
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = {
            "technical_requirements": ["Python", "SQL", "ML"],
            "experience_level": "Senior",
            "required_skills": ["Data Science", "Machine Learning"]
        }
        
        # Create async mock for create method
        mock_create = AsyncMock(return_value=mock_response)
        
        # Patch the create method
        with patch.object(interview_manager.client.chat.completions, 'create', 
                         new=mock_create):
            analysis = await interview_manager.analyze_job_description(job_description)
            assert isinstance(analysis, (str, dict))
            assert "Python" in str(analysis)
            
    async def test_optimize_resume(self, interview_manager):
        """Test resume optimization"""
        resume = "Sample resume content"
        job_analysis = {"technical_requirements": ["Python"]}
        
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Optimized resume content"
        
        mock_create = AsyncMock(return_value=mock_response)
        
        with patch.object(interview_manager.client.chat.completions, 'create', 
                         new=mock_create):
            optimized = await interview_manager.optimize_resume(resume, job_analysis)
            assert isinstance(optimized, str)
            assert len(optimized) > 0
            
    async def test_prepare_technical_questions(self, interview_manager):
        """Test technical question generation"""
        job_analysis = {
            "technical_requirements": ["Python", "SQL"],
            "experience_level": "Senior"
        }
        
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = [
            {"question": "Explain Python decorators"},
            {"question": "Write a complex SQL query"}
        ]
        
        mock_create = AsyncMock(return_value=mock_response)
        
        with patch.object(interview_manager.client.chat.completions, 'create', 
                         new=mock_create):
            questions = await interview_manager.prepare_technical_questions(job_analysis)
            assert "question" in str(questions)
            
    async def test_generate_behavioral_scenarios(self, interview_manager):
        """Test behavioral scenario generation"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = [
            {"scenario": "Describe a challenging project"},
            {"scenario": "Handle a conflict situation"}
        ]
        
        mock_create = AsyncMock(return_value=mock_response)
        
        with patch.object(interview_manager.client.chat.completions, 'create', 
                         new=mock_create):
            scenarios = await interview_manager.generate_behavioral_scenarios("Senior")
            assert "scenario" in str(scenarios)
            
    async def test_create_mock_interview(self, interview_manager):
        """Test mock interview creation"""
        technical_questions = [{"question": "Technical Q1"}]
        behavioral_scenarios = [{"scenario": "Behavioral S1"}]
        
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = {
            "interview_flow": ["Introduction", "Technical", "Behavioral"],
            "estimated_duration": 60
        }
        
        mock_create = AsyncMock(return_value=mock_response)
        
        with patch.object(interview_manager.client.chat.completions, 'create', 
                         new=mock_create):
            mock_interview = await interview_manager.create_mock_interview(
                technical_questions,
                behavioral_scenarios
            )
            assert "interview_flow" in str(mock_interview)