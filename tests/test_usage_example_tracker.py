import pytest
from usage_example_tracker import ApplicationTracker
from datetime import datetime

class TestUsageExampleTracker:
    def test_tracker_initialization(self):
        """Test tracker initialization"""
        tracker = ApplicationTracker()
        assert tracker is not None
        
    def test_add_application(self):
        """Test adding an application"""
        tracker = ApplicationTracker()
        app = tracker.add_application(
            company="TestCorp",
            position="Data Scientist",
            date=datetime.now()
        )
        assert app is not None
        assert app.company == "TestCorp"
        
    def test_update_status(self):
        """Test updating application status"""
        tracker = ApplicationTracker()
        app = tracker.add_application(
            company="TestCorp",
            position="Data Scientist",
            date=datetime.now()
        )
        updated = tracker.update_status(app.id, "Interview")
        assert updated.status == "Interview"
        
    def test_get_statistics(self):
        """Test getting application statistics"""
        tracker = ApplicationTracker()
        stats = tracker.get_statistics()
        assert isinstance(stats, dict)
        assert "total_applications" in stats 