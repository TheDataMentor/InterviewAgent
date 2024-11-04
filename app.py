from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from application_tracker import ApplicationTracker, ApplicationStatus, ApplicationPriority
from interview_process_agents import InterviewProcessManager
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import uvicorn
from pathlib import Path
import logging
import sys

# Load environment variables
load_dotenv()

# Check for API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Print to console
        logging.FileHandler('app.log')      # Save to file
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(debug=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the current directory
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Create directories if they don't exist
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Initialize trackers
tracker = ApplicationTracker(user_tier="free")
interview_manager = InterviewProcessManager(openai_api_key=api_key)

class ApplicationRequest(BaseModel):
    company: str
    position: str
    job_link: Optional[str] = None
    priority: int = 2

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(str(STATIC_DIR / "favicon.ico"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        logger.info("Serving index.html")
        return templates.TemplateResponse(
            "index.html", 
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/applications/")
async def add_application(application: ApplicationRequest):
    try:
        app = tracker.add_application(
            company=application.company,
            position=application.position,
            job_link=application.job_link,
            priority=ApplicationPriority(application.priority)
        )
        return {"status": "success", "application_id": app.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/applications/")
async def get_applications():
    return {
        "applications": [app.dict() for app in tracker.applications.values()],
        "stats": tracker.get_application_stats()
    }

@app.post("/analyze-job/")
async def analyze_job(request: Request):
    try:
        # Parse the request body
        body = await request.json()
        job_description = body.get('job_description')
        
        if not job_description:
            raise HTTPException(status_code=400, detail="Job description is required")
            
        logger.info(f"Analyzing job description: {job_description[:100]}...")  # Log first 100 chars
        
        analysis = await interview_manager.analyze_job_description(job_description)
        logger.info("Analysis complete")
        
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error analyzing job: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/optimize-resume/")
async def optimize_resume(request: Request):
    try:
        body = await request.json()
        resume = body.get('resume')
        job_requirements = body.get('job_requirements')
        
        if not resume:
            raise HTTPException(status_code=400, detail="Resume is required")
            
        logger.info("Optimizing resume...")
        
        optimized = await interview_manager.optimize_resume(
            resume=resume,
            job_analysis={"requirements": job_requirements}
        )
        logger.info("Resume optimization complete")
        
        return {"optimized_resume": optimized}
    except Exception as e:
        logger.error(f"Error optimizing resume: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting server with:")
    logger.info(f"Static directory: {STATIC_DIR}")
    logger.info(f"Templates directory: {TEMPLATES_DIR}")
    
    # Verify files exist
    required_files = [
        STATIC_DIR / "styles.css",
        STATIC_DIR / "script.js",
        TEMPLATES_DIR / "index.html"
    ]
    
    for file in required_files:
        if not file.exists():
            logger.error(f"Missing required file: {file}")
        else:
            logger.info(f"Found required file: {file}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise

if __name__ == "__main__":
    print(f"Starting server...")
    print(f"Static files directory: {STATIC_DIR}")
    print(f"Templates directory: {TEMPLATES_DIR}")
    uvicorn.run(
        "app:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 