import pytest
from datetime import datetime
from interview_data_models import ApplicationStatus, InterviewPrep, ResumeVersion

class TestInterviewDataModels:
    def test_application_status_model(self):
        """Test ApplicationStatus model creation and validation"""
        status = ApplicationStatus(
            company="TestCorp",
            position="Data Scientist",
            application_date=datetime.now(),
            status="Applied",
            next_action="Follow up",
            priority=1,
            notes=["Initial application submitted"]
        )
        
        assert status.company == "TestCorp"
        assert status.position == "Data Scientist"
        assert status.status == "Applied"
        assert len(status.notes) == 1
        
    def test_resume_version_model(self):
        """Test ResumeVersion model creation and validation"""
        version = ResumeVersion(
            job_type="Data Science",
            skills_highlighted=["Python", "ML"],
            achievements=["Improved model accuracy by 20%"],
            version_date=datetime.now(),
            ats_score=0.85
        )
        
        assert version.job_type == "Data Science"
        assert len(version.skills_highlighted) == 2
        assert version.ats_score == 0.85
        
    def test_interview_prep_model(self):
        """Test InterviewPrep model creation and validation"""
        prep = InterviewPrep(
            company="TestCorp",
            tech_stack=["Python", "SQL"],
            practice_questions=["Explain ML models"],
            company_culture={"values": "Innovation"},
            salary_range=(100000, 150000)
        )
        
        assert prep.company == "TestCorp"
        assert len(prep.tech_stack) == 2
        assert isinstance(prep.salary_range, tuple) 