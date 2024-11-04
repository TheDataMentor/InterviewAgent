from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class ApplicationStatus(str, Enum):
    IDENTIFIED = "identified"
    APPLIED = "applied"
    PHONE_SCREEN = "phone_screen"
    TECHNICAL = "technical"
    ONSITE = "onsite"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class ApplicationPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Application(BaseModel):
    id: str
    company: str
    position: str
    status: ApplicationStatus
    priority: ApplicationPriority
    created_at: datetime
    updated_at: datetime
    next_action_date: Optional[datetime] = None
    notes: Optional[str] = None
    salary_range: Optional[str] = None
    location: Optional[str] = None
    job_link: Optional[str] = None
    is_remote: Optional[bool] = None

class ApplicationTracker:
    def __init__(self, user_tier: str = "free"):
        self.user_tier = user_tier
        self.applications: Dict[str, Application] = {}
        
    def add_application(self, 
                       company: str, 
                       position: str, 
                       job_link: Optional[str] = None,
                       priority: ApplicationPriority = ApplicationPriority.MEDIUM) -> Application:
        """Add a new job application to track (Available in Free Tier)"""
        app_id = f"{len(self.applications) + 1}"
        application = Application(
            id=app_id,
            company=company,
            position=position,
            status=ApplicationStatus.IDENTIFIED,
            priority=priority,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            job_link=job_link
        )
        self.applications[app_id] = application
        return application

    def update_status(self, 
                     app_id: str, 
                     status: ApplicationStatus,
                     notes: Optional[str] = None) -> Application:
        """Update application status (Available in Free Tier)"""
        if app_id not in self.applications:
            raise ValueError(f"Application {app_id} not found")
            
        application = self.applications[app_id]
        application.status = status
        application.updated_at = datetime.now()
        if notes:
            application.notes = notes
        return application

    def get_application_stats(self) -> Dict:
        """Get basic application statistics (Available in Free Tier)"""
        stats = {
            "total_applications": len(self.applications),
            "status_breakdown": {status: 0 for status in ApplicationStatus},
            "active_applications": 0
        }
        
        for app in self.applications.values():
            stats["status_breakdown"][app.status] += 1
            if app.status not in [ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN]:
                stats["active_applications"] += 1
                
        return stats

    def get_upcoming_actions(self) -> List[Dict]:
        """Get upcoming actions (Available in Free Tier)"""
        upcoming = []
        for app in self.applications.values():
            if app.next_action_date and app.status not in [ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN]:
                upcoming.append({
                    "company": app.company,
                    "position": app.position,
                    "action_date": app.next_action_date,
                    "status": app.status
                })
        return sorted(upcoming, key=lambda x: x["action_date"])

    # Premium Features
    def set_reminder(self, 
                    app_id: str, 
                    reminder_date: datetime, 
                    reminder_note: str) -> bool:
        """Set reminder for application (Premium Feature)"""
        if self.user_tier != "premium":
            raise PermissionError("This feature is only available in the premium tier")
            
        if app_id not in self.applications:
            raise ValueError(f"Application {app_id} not found")
            
        application = self.applications[app_id]
        application.next_action_date = reminder_date
        application.notes = f"{application.notes}\nReminder: {reminder_note}" if application.notes else f"Reminder: {reminder_note}"
        return True

    def _calculate_success_rate(self) -> float:
        """Calculate application success rate"""
        total = len(self.applications)
        if total == 0:
            return 0.0
        offers = sum(1 for app in self.applications.values() if app.status == ApplicationStatus.OFFER)
        return (offers / total) * 100

    def _calculate_avg_time_to_offer(self) -> float:
        """Calculate average time to offer"""
        offer_times = []
        for app in self.applications.values():
            if app.status == ApplicationStatus.OFFER:
                time_to_offer = (app.updated_at - app.created_at).days
                offer_times.append(time_to_offer)
        return sum(offer_times) / len(offer_times) if offer_times else 0

    def _analyze_application_channels(self) -> Dict:
        """Analyze which application channels are most successful"""
        return {"direct": 60, "referral": 30, "recruiter": 10}  # Example data

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on application history"""
        return ["Focus on referrals", "Follow up more frequently"]

    def generate_insights(self) -> Dict:
        """Generate advanced insights (Premium Feature)"""
        if self.user_tier != "premium":
            raise PermissionError("This feature is only available in the premium tier")
            
        return {
            "success_rate": self._calculate_success_rate(),
            "average_time_to_offer": self._calculate_avg_time_to_offer(),
            "best_performing_channels": self._analyze_application_channels(),
            "recommendations": self._generate_recommendations()
        }

    def export_applications(self, format: str = "csv") -> str:
        """Export applications data (Premium Feature)"""
        if self.user_tier != "premium":
            raise PermissionError("This feature is only available in the premium tier")
        raise NotImplementedError("Export functionality not implemented yet")