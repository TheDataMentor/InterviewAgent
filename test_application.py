import pytest
from application_tracker import ApplicationTracker, ApplicationStatus, ApplicationPriority

@pytest.fixture
def free_tracker():
    return ApplicationTracker(user_tier="free")

@pytest.fixture
def premium_tracker():
    return ApplicationTracker(user_tier="premium")

@pytest.fixture
def sample_application(free_tracker):
    """Create a sample application for testing"""
    application = free_tracker.add_application(
        company="TestCorp",
        position="Data Scientist",
        job_link="https://test.com/job",
        priority=ApplicationPriority.HIGH
    )
    return application

class TestFreeFeatures:
    def test_add_application(self, free_tracker):
        """Test adding a new application"""
        application = free_tracker.add_application(
            company="TestCorp",
            position="Data Scientist"
        )
        
        assert application.id == "1"
        assert application.company == "TestCorp"
        assert application.position == "Data Scientist"
        assert application.status == ApplicationStatus.IDENTIFIED
        assert application.priority == ApplicationPriority.MEDIUM

    def test_update_application_status(self, free_tracker, sample_application):
        """Test updating application status"""
        updated_app = free_tracker.update_status(
            app_id=sample_application.id,
            status=ApplicationStatus.APPLIED
        )
        
        assert updated_app.status == ApplicationStatus.APPLIED

    # Add more test methods as needed...