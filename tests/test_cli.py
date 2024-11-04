import pytest
from datetime import datetime
from application_tracker import ApplicationTracker, ApplicationStatus, ApplicationPriority
from interview_process_agents import InterviewProcessManager
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def cli_tracker():
    return ApplicationTracker(user_tier="free")

@pytest.fixture
def cli_interview_manager():
    return InterviewProcessManager(openai_api_key=os.getenv('OPENAI_API_KEY'))

class TestCLIFunctionality:
    def test_add_application(self, cli_tracker):
        app = cli_tracker.add_application(
            company="TestCorp",
            position="Data Scientist"
        )
        assert app.company == "TestCorp"
        assert app.position == "Data Scientist"

    def test_update_status(self, cli_tracker):
        app = cli_tracker.add_application(
            company="TestCorp",
            position="Data Scientist"
        )
        updated = cli_tracker.update_status(
            app_id=app.id,
            status=ApplicationStatus.APPLIED
        )
        assert updated.status == ApplicationStatus.APPLIED

    def test_view_stats(self, cli_tracker):
        stats = cli_tracker.get_application_stats()
        assert isinstance(stats, dict)
        assert "total_applications" in stats

    @pytest.mark.asyncio
    async def test_analyze_job(self, cli_interview_manager):
        analysis = await cli_interview_manager.analyze_job_description(
            "Sample job description"
        )
        assert analysis is not None 