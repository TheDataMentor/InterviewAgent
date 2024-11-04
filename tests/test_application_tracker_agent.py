import pytest
from datetime import datetime
from typing import Dict
from application_tracker_agent import ApplicationTrackerAgent, Application, ApplicationStatus, ApplicationPriority

@pytest.fixture
def tracker_agent():
    return ApplicationTrackerAgent(user_tier="free")

class TestApplicationTrackerAgent:
    def test_add_application(self, tracker_agent):
        """Test adding a new application with job insights"""
        application = tracker_agent.add_application(
            company="TestCorp",
            position="Data Scientist",
            job_link="https://test.com/job/123",
            priority=ApplicationPriority.HIGH
        )
        
        assert application.id == "1"
        assert application.company == "TestCorp"
        assert application.position == "Data Scientist"
        assert application.job_link == "https://test.com/job/123"
        
    def test_get_job_insights(self, tracker_agent):
        """Test gathering insights about a job"""
        job_link = "https://test.com/job/123"
        insights = tracker_agent.get_job_insights(job_link)
        
        assert isinstance(insights, Dict)
        assert "job_description" in insights
        assert "salary_range" in insights
        assert "required_skills" in insights
        assert "company_info" in insights
        
    def test_job_market_analysis(self, tracker_agent):
        """Test analyzing job market trends"""
        analysis = tracker_agent.analyze_job_market("Data Scientist")
        
        assert "market_demand" in analysis
        assert "average_salary" in analysis
        assert "top_skills" in analysis
        assert "growing_companies" in analysis 