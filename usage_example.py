import asyncio
from interview_process_agents import InterviewProcessManager

async def main():
    # Initialize the interview process manager
    manager = InterviewProcessManager(openai_api_key="your_openai_key")
    
    # Sample job description
    job_description = """
    Senior Data Scientist position requiring 5+ years experience in machine learning,
    Python, SQL, and experience with big data technologies. Must have strong 
    background in statistical analysis and deep learning frameworks.
    """
    
    # Step 1: Analyze job description
    job_analysis = await manager.analyze_job_description(job_description)
    print("Job Analysis Complete:", job_analysis)
    
    # Step 2: Optimize resume
    resume = "Your resume content here..."
    optimized_resume = await manager.optimize_resume(resume, job_analysis)
    print("Resume Optimized:", optimized_resume)
    
    # Step 3: Generate technical questions
    technical_questions = await manager.prepare_technical_questions(job_analysis)
    print("Technical Questions Generated:", technical_questions)
    
    # Step 4: Generate behavioral scenarios
    behavioral_scenarios = await manager.generate_behavioral_scenarios("Senior")
    print("Behavioral Scenarios Generated:", behavioral_scenarios)
    
    # Step 5: Create mock interview
    mock_interview = await manager.create_mock_interview(
        technical_questions, 
        behavioral_scenarios
    )
    print("Mock Interview Created:", mock_interview)

if __name__ == "__main__":
    asyncio.run(main()) 