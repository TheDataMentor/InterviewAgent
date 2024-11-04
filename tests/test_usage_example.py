import pytest
from datetime import datetime
from application_tracker import ApplicationTracker, ApplicationStatus, ApplicationPriority

class TestApplicationManager:
    def test_manager_initialization(self):
        """Test manager initialization"""
        tracker = ApplicationTracker()
        assert tracker is not None
        assert tracker.user_tier == "free"
        
    def test_add_application(self):
        """Test adding application"""
        tracker = ApplicationTracker()
        app = tracker.add_application(
            company="TestCorp",
            position="Data Scientist"
        )
        assert app.company == "TestCorp"
        assert app.position == "Data Scientist"
        assert app.status == ApplicationStatus.IDENTIFIED
        
    def test_update_status(self):
        """Test updating application status"""
        tracker = ApplicationTracker()
        app = tracker.add_application(
            company="TestCorp",
            position="Data Scientist"
        )
        updated = tracker.update_status(
            app_id=app.id,
            status=ApplicationStatus.APPLIED
        )
        assert updated.status == ApplicationStatus.APPLIED
        
    def test_get_stats(self):
        """Test getting application statistics"""
        tracker = ApplicationTracker()
        stats = tracker.get_application_stats()
        assert isinstance(stats, dict)
        assert "total_applications" in stats
        assert "active_applications" in stats 