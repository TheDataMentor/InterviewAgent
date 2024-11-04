from typing import List, Dict

class JobSearchAgent:
    def __init__(self):
        self.job_listings = []

    def search_jobs(self, keywords: str) -> List[Dict]:
        # Simulated job search results
        return [
            {
                "title": "Senior Data Scientist",
                "company": "Tech Corp",
                "location": "Remote",
                "salary": "$120,000 - $150,000"
            }
        ]

    def bookmark_job(self, job_link: str):
        self.job_listings.append(job_link)

    def get_bookmarked_jobs(self) -> List[str]:
        return self.job_listings

    def gather_job_insights(self, job_link: str) -> Dict:
        return {
            "job_description": "Sample job description",
            "salary_range": "$80,000 - $120,000",
            "required_skills": ["Python", "ML"]
        } 