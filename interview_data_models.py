from typing import List, Dict, Tuple, Optional
from datetime import datetime
from pydantic import BaseModel

class JobAnalysis(BaseModel):
    technical_requirements: List[str]
    experience_level: str
    required_skills: List[str]
    preferred_skills: List[str]
    company_tech_stack: List[str]
    
class TechnicalQuestion(BaseModel):
    question: str
    category: str
    difficulty: str
    expected_concepts: List[str]
    sample_answer: str
    
class BehavioralScenario(BaseModel):
    scenario: str
    target_competency: str
    ideal_response_points: List[str]
    follow_up_questions: List[str]
    
class MockInterview(BaseModel):
    interview_flow: List[Dict]
    estimated_duration: int
    difficulty_level: str
    preparation_tips: List[str]
    evaluation_criteria: Dict 

class ApplicationStatus(BaseModel):
    company: str
    position: str
    application_date: datetime
    status: str
    next_action: str
    priority: int
    notes: List[str]

class ResumeVersion(BaseModel):
    job_type: str
    skills_highlighted: List[str]
    achievements: List[str]
    version_date: datetime
    ats_score: float

class InterviewPrep(BaseModel):
    company: str
    tech_stack: List[str]
    practice_questions: List[str]
    company_culture: Dict
    salary_range: Tuple[int, int]