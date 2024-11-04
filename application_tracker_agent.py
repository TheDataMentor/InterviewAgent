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

class ApplicationTrackerAgent:
    def __init__(self, user_tier: str = "free"):
        self.user_tier = user_tier
        self.applications: Dict[str, Application] = {}
        
    def add_application(self, company: str, position: str, job_link: Optional[str] = None,
                       priority: ApplicationPriority = ApplicationPriority.MEDIUM) -> Application:
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

    def get_job_insights(self, job_link: str) -> Dict:
        return {
            "job_description": "Sample job description",
            "salary_range": "$80,000 - $120,000",
            "required_skills": ["Python", "Machine Learning", "Data Analysis"],
            "company_info": "Company XYZ is a leading firm in data science."
        }

    def analyze_job_market(self, position: str) -> Dict:
        return {
            "market_demand": "High",
            "average_salary": "$100,000",
            "top_skills": ["Python", "SQL", "Machine Learning"],
            "growing_companies": ["Tech Corp", "Data Inc"]
        } 