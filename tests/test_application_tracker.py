import pytest
from datetime import datetime, timedelta
from application_tracker import (
    ApplicationTracker, 
    ApplicationStatus, 
    ApplicationPriority,
    Application
)

@pytest.fixture
def free_tracker():
    return ApplicationTracker(user_tier="free")

@pytest.fixture
def premium_tracker():
    return ApplicationTracker(user_tier="premium")

@pytest.fixture
def sample_application(free_tracker):
    """Create a sample application for testing"""
    return free_tracker.add_application(
        company="TestCorp",
        position="Data Scientist",
        job_link="https://test.com/job",
        priority=ApplicationPriority.HIGH
    )

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
        
    def test_update_status(self, free_tracker, sample_application):
        """Test updating application status"""
        updated_app = free_tracker.update_status(
            app_id=sample_application.id,
            status=ApplicationStatus.APPLIED,
            notes="Test note"
        )
        
        assert updated_app.status == ApplicationStatus.APPLIED
        assert updated_app.notes == "Test note"
        assert updated_app.updated_at > updated_app.created_at
        
    def test_get_application_stats(self, free_tracker, sample_application):
        """Test getting application statistics"""
        # Add another application with different status
        app2 = free_tracker.add_application(
            company="AnotherCorp",
            position="ML Engineer"
        )
        free_tracker.update_status(app2.id, ApplicationStatus.REJECTED)
        
        stats = free_tracker.get_application_stats()
        
        assert stats["total_applications"] == 2
        assert stats["status_breakdown"][ApplicationStatus.IDENTIFIED] == 1
        assert stats["status_breakdown"][ApplicationStatus.REJECTED] == 1
        assert stats["active_applications"] == 1
        
    def test_get_upcoming_actions(self, free_tracker, sample_application):
        """Test getting upcoming actions"""
        # Add application with next action date
        app2 = free_tracker.add_application(
            company="FutureCorp",
            position="Data Engineer"
        )
        app2.next_action_date = datetime.now() + timedelta(days=1)
        
        actions = free_tracker.get_upcoming_actions()
        
        assert len(actions) == 1
        assert actions[0]["company"] == "FutureCorp"
        
    def test_invalid_application_id(self, free_tracker):
        """Test handling invalid application ID"""
        with pytest.raises(ValueError):
            free_tracker.update_status(
                app_id="999",
                status=ApplicationStatus.APPLIED
            )

class TestPremiumFeatures:
    def test_set_reminder_premium(self, premium_tracker):
        """Test setting reminder in premium tier"""
        app = premium_tracker.add_application(
            company="PremiumCorp",
            position="Senior Data Scientist"
        )
        
        reminder_date = datetime.now() + timedelta(days=7)
        result = premium_tracker.set_reminder(
            app_id=app.id,
            reminder_date=reminder_date,
            reminder_note="Follow up"
        )
        
        assert result is True
        assert premium_tracker.applications[app.id].next_action_date == reminder_date
        assert "Follow up" in premium_tracker.applications[app.id].notes
        
    def test_set_reminder_free(self, free_tracker, sample_application):
        """Test setting reminder in free tier (should fail)"""
        with pytest.raises(PermissionError):
            free_tracker.set_reminder(
                app_id=sample_application.id,
                reminder_date=datetime.now() + timedelta(days=7),
                reminder_note="Follow up"
            )
            
    def test_generate_insights_premium(self, premium_tracker):
        """Test generating insights in premium tier"""
        insights = premium_tracker.generate_insights()
        
        assert "success_rate" in insights
        assert "average_time_to_offer" in insights
        assert "best_performing_channels" in insights
        assert "recommendations" in insights
        
    def test_generate_insights_free(self, free_tracker):
        """Test generating insights in free tier (should fail)"""
        with pytest.raises(PermissionError):
            free_tracker.generate_insights()
            
    def test_export_applications_premium(self, premium_tracker):
        """Test exporting applications in premium tier"""
        with pytest.raises(NotImplementedError):
            premium_tracker.export_applications()
            
    def test_export_applications_free(self, free_tracker):
        """Test exporting applications in free tier (should fail)"""
        with pytest.raises(PermissionError):
            free_tracker.export_applications()

class TestApplicationModel:
    def test_application_creation(self):
        """Test Application model creation and validation"""
        app = Application(
            id="1",
            company="TestCorp",
            position="Data Scientist",
            status=ApplicationStatus.IDENTIFIED,
            priority=ApplicationPriority.MEDIUM,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        assert isinstance(app.created_at, datetime)
        assert app.notes is None
        assert app.salary_range is None
        assert app.is_remote is None
        
    def test_application_optional_fields(self):
        """Test Application model with optional fields"""
        app = Application(
            id="1",
            company="TestCorp",
            position="Data Scientist",
            status=ApplicationStatus.IDENTIFIED,
            priority=ApplicationPriority.MEDIUM,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            salary_range="100k-120k",
            location="Remote",
            is_remote=True,
            notes="Test notes"
        )
        
        assert app.salary_range == "100k-120k"
        assert app.location == "Remote"
        assert app.is_remote is True
        assert app.notes == "Test notes"

class TestEdgeCases:
    def test_duplicate_application_ids(self, free_tracker):
        """Test handling of application IDs"""
        app1 = free_tracker.add_application(
            company="Company1",
            position="Position1"
        )
        app2 = free_tracker.add_application(
            company="Company2",
            position="Position2"
        )
        
        assert app1.id != app2.id
        
    def test_status_transitions(self, free_tracker, sample_application):
        """Test various status transitions"""
        statuses = [
            ApplicationStatus.APPLIED,
            ApplicationStatus.PHONE_SCREEN,
            ApplicationStatus.TECHNICAL,
            ApplicationStatus.ONSITE,
            ApplicationStatus.OFFER
        ]
        
        for status in statuses:
            updated_app = free_tracker.update_status(
                app_id=sample_application.id,
                status=status
            )
            assert updated_app.status == status 

class TestApplicationTracker:
    def test_premium_features(self):
        """Test premium features access"""
        tracker = ApplicationTracker(user_tier="free")
        
        # Test set_reminder
        with pytest.raises(PermissionError):
            tracker.set_reminder("1", datetime.now(), "Test reminder")
            
        # Test generate_insights
        with pytest.raises(PermissionError):
            tracker.generate_insights()
            
        # Test export_applications
        with pytest.raises(PermissionError):
            tracker.export_applications()
            
    def test_premium_tracker(self):
        """Test premium tracker functionality"""
        tracker = ApplicationTracker(user_tier="premium")
        
        # Add application
        app = tracker.add_application(
            company="TestCorp",
            position="Data Scientist"
        )
        
        # Test reminder
        reminder_date = datetime.now() + timedelta(days=7)
        result = tracker.set_reminder(app.id, reminder_date, "Follow up")
        assert result is True
        assert tracker.applications[app.id].next_action_date == reminder_date
        
        # Test insights
        insights = tracker.generate_insights()
        assert "success_rate" in insights
        assert "average_time_to_offer" in insights
        assert "best_performing_channels" in insights
        assert "recommendations" in insights
        
        # Test export
        with pytest.raises(NotImplementedError):
            tracker.export_applications()