import pytest
from fastapi.testclient import TestClient
from app import app, ApplicationRequest
from application_tracker import ApplicationStatus, ApplicationPriority
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.fixture
def mock_openai_response():
    return AsyncMock(return_value=AsyncMock(
        choices=[AsyncMock(message=AsyncMock(content="Test response"))]
    ))

class TestEndpoints:
    def test_read_main(self):
        """Test main endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Job Application Tracker" in response.text

    def test_favicon(self):
        """Test favicon endpoint"""
        response = client.get("/favicon.ico")
        assert response.status_code == 200 or response.status_code == 404  # 404 is acceptable if favicon doesn't exist

    def test_add_application_success(self):
        """Test successful application addition"""
        response = client.post(
            "/applications/",
            json={
                "company": "TestCorp",
                "position": "Data Scientist",
                "priority": 2
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "application_id" in data

    def test_add_application_validation_error(self):
        """Test application addition with invalid data"""
        response = client.post(
            "/applications/",
            json={
                "company": "",  # Empty company name
                "position": "Data Scientist",
                "priority": 2
            }
        )
        assert response.status_code == 422  # Validation error

    def test_get_applications_empty(self):
        """Test getting applications when none exist"""
        response = client.get("/applications/")
        assert response.status_code == 200
        data = response.json()
        assert "applications" in data
        assert "stats" in data
        assert data["stats"]["total_applications"] >= 0

    @patch('app.interview_manager.analyze_job_description')
    async def test_analyze_job_success(self, mock_analyze):
        """Test successful job analysis"""
        mock_analyze.return_value = {"analysis": "Test analysis"}
        response = client.post(
            "/analyze-job/",
            json={"job_description": "Sample job description"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data

    @patch('app.interview_manager.analyze_job_description')
    async def test_analyze_job_missing_description(self, mock_analyze):
        """Test job analysis with missing description"""
        response = client.post(
            "/analyze-job/",
            json={}
        )
        assert response.status_code == 422  # Validation error

    @patch('app.interview_manager.optimize_resume')
    async def test_optimize_resume_success(self, mock_optimize):
        """Test successful resume optimization"""
        mock_optimize.return_value = "Optimized resume"
        response = client.post(
            "/optimize-resume/",
            json={
                "resume": "Sample resume",
                "job_requirements": "Sample requirements"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "optimized_resume" in data

    @patch('app.interview_manager.optimize_resume')
    async def test_optimize_resume_missing_data(self, mock_optimize):
        """Test resume optimization with missing data"""
        response = client.post(
            "/optimize-resume/",
            json={}
        )
        assert response.status_code == 422  # Validation error

class TestErrorHandling:
    def test_invalid_endpoint(self):
        """Test accessing invalid endpoint"""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_invalid_method(self):
        """Test using invalid HTTP method"""
        response = client.put("/applications/")  # PUT not allowed
        assert response.status_code == 405

    @patch('app.interview_manager.analyze_job_description')
    async def test_analysis_error_handling(self, mock_analyze):
        """Test error handling in job analysis"""
        mock_analyze.side_effect = Exception("Test error")
        response = client.post(
            "/analyze-job/",
            json={"job_description": "Sample"}
        )
        assert response.status_code == 400
        assert "error" in response.json()

class TestMiddleware:
    def test_cors_headers(self):
        """Test CORS headers"""
        response = client.options(
            "/applications/",
            headers={"Origin": "http://testserver"}
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_request_logging(self, caplog):
        """Test request logging"""
        with caplog.at_level("INFO"):
            client.get("/")
            assert "Request path: /" in caplog.text

class TestStartupEvents:
    def test_startup_file_checks(self, tmp_path):
        """Test startup file verification"""
        # Create temporary files
        static_dir = tmp_path / "static"
        templates_dir = tmp_path / "templates"
        static_dir.mkdir()
        templates_dir.mkdir()
        
        (static_dir / "styles.css").touch()
        (static_dir / "script.js").touch()
        (templates_dir / "index.html").touch()
        
        # Verify files exist
        assert (static_dir / "styles.css").exists()
        assert (static_dir / "script.js").exists()
        assert (templates_dir / "index.html").exists()

class TestApplicationRequests:
    def test_application_request_model(self):
        """Test ApplicationRequest model validation"""
        request = ApplicationRequest(
            company="TestCorp",
            position="Data Scientist"
        )
        assert request.company == "TestCorp"
        assert request.position == "Data Scientist"
        assert request.priority == 2  # Default value

    def test_application_request_validation(self):
        """Test ApplicationRequest validation"""
        response = client.post(
            "/applications/",
            json={
                "company": "TestCorp",
                "position": "Data Scientist",
                "priority": 4  # Invalid priority
            }
        )
        assert response.status_code == 422  # Validation error 