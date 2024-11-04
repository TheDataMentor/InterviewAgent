import pytest
from job_search_agent import JobSearchAgent

class TestJobSearchAgent:
    def test_search_jobs(self):
        """Test job search functionality"""
        agent = JobSearchAgent()
        jobs = agent.search_jobs("Data Scientist")
        assert isinstance(jobs, list)
        assert len(jobs) > 0
        assert "title" in jobs[0]
        assert "company" in jobs[0]
        
    def test_bookmark_management(self):
        """Test bookmark functionality"""
        agent = JobSearchAgent()
        job_link = "https://example.com/job/123"
        
        # Test adding bookmark
        agent.bookmark_job(job_link)
        bookmarks = agent.get_bookmarked_jobs()
        assert job_link in bookmarks
        
        # Test getting insights
        insights = agent.gather_job_insights(job_link)
        assert "job_description" in insights
        assert "salary_range" in insights
        assert "required_skills" in insights 