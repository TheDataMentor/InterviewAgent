from typing import Dict, List
from openai import AsyncOpenAI
from datetime import datetime
from pydantic import BaseModel

class InterviewProcessManager:
    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        
    async def get_completion(self, messages: List[Dict], model="gpt-4-turbo-preview"):
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def analyze_job_description(self, job_description: str):
        """Step 1: Analyze job description and extract key requirements"""
        messages = [
            {"role": "system", "content": "You are an expert data professional job analyzer. Extract key technical requirements, experience levels, and desired skills from job descriptions."},
            {"role": "user", "content": f"Analyze this job description and extract key requirements: {job_description}"}
        ]
        
        analysis = await self.get_completion(messages)
        return analysis

    async def optimize_resume(self, resume: str, job_analysis: dict):
        """Step 2: Optimize resume based on job requirements"""
        messages = [
            {"role": "system", "content": "You are an expert resume optimizer for data professionals. Customize resumes to match job requirements while maintaining authenticity."},
            {"role": "user", "content": f"Optimize this resume based on the job analysis: {resume}\n\nJob Analysis: {job_analysis}"}
        ]
        
        optimized_resume = await self.get_completion(messages)
        return optimized_resume

    async def prepare_technical_questions(self, job_analysis: dict):
        """Step 3: Generate relevant technical interview questions"""
        messages = [
            {"role": "system", "content": "You are an expert technical interviewer for data positions. Generate relevant technical questions based on job requirements."},
            {"role": "user", "content": f"Generate technical interview questions based on this job analysis: {job_analysis}"}
        ]
        
        questions = await self.get_completion(messages)
        return questions

    async def generate_behavioral_scenarios(self, position_level: str):
        """Step 4: Generate behavioral interview scenarios"""
        messages = [
            {"role": "system", "content": "You are an expert in behavioral interviewing. Generate relevant scenarios for data professionals."},
            {"role": "user", "content": f"Generate behavioral interview scenarios for a {position_level} data position"}
        ]
        
        scenarios = await self.get_completion(messages)
        return scenarios

    async def create_mock_interview(self, technical_questions: list, behavioral_scenarios: list):
        """Step 5: Create a complete mock interview simulation"""
        messages = [
            {"role": "system", "content": "You are an expert interview simulator. Create a realistic mock interview experience combining technical and behavioral questions."},
            {"role": "user", "content": f"Create a mock interview using these questions:\nTechnical: {technical_questions}\nBehavioral: {behavioral_scenarios}"}
        ]
        
        mock_interview = await self.get_completion(messages)
        return mock_interview 