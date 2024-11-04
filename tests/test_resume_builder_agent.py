import pytest
from resume_builder_agent import ResumeBuilderAgent
from unittest.mock import patch, AsyncMock

@pytest.fixture
async def resume_agent():
    return ResumeBuilderAgent(openai_api_key="test_key")

@pytest.mark.asyncio
class TestResumeBuilderAgent:
    async def test_create_resume(self, resume_agent):
        """Test creating a resume from user data"""
        user_data = {
            "name": "John Doe",
            "experience": ["Data Scientist at Company X"],
            "skills": ["Python", "Machine Learning"]
        }
        
        with patch.object(resume_agent.client.chat.completions, 'create', 
                         new=AsyncMock()) as mock_create:
            mock_create.return_value.choices[0].message.content = "Generated Resume"
            resume = await resume_agent.create_resume(user_data)
            assert isinstance(resume, str)
            assert len(resume) > 0
            
    async def test_tailor_resume(self, resume_agent):
        """Test tailoring resume to job description"""
        resume = "Original Resume"
        job_description = "Job requires Python and ML"
        
        with patch.object(resume_agent.client.chat.completions, 'create', 
                         new=AsyncMock()) as mock_create:
            mock_create.return_value.choices[0].message.content = "Tailored Resume"
            tailored = await resume_agent.tailor_resume(resume, job_description)
            assert isinstance(tailored, str)
            assert tailored != resume 