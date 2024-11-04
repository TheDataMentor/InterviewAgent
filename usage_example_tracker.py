from application_tracker import ApplicationTracker, ApplicationStatus, ApplicationPriority
from datetime import datetime, timedelta

def main():
    # Initialize tracker (Free Tier)
    tracker = ApplicationTracker(user_tier="free")
    
    # Free Tier Features
    
    # 1. Add new applications
    app1 = tracker.add_application(
        company="TechCorp",
        position="Senior Data Scientist",
        job_link="https://techcorp.com/jobs/123",
        priority=ApplicationPriority.HIGH
    )
    
    app2 = tracker.add_application(
        company="DataInc",
        position="ML Engineer",
        priority=ApplicationPriority.MEDIUM
    )
    
    # 2. Update application status
    tracker.update_status(
        app_id=app1.id,
        status=ApplicationStatus.APPLIED,
        notes="Applied through company website"
    )
    
    # 3. Get basic stats
    stats = tracker.get_application_stats()
    print("Application Stats:", stats)
    
    # 4. Get upcoming actions
    actions = tracker.get_upcoming_actions()
    print("Upcoming Actions:", actions)
    
    try:
        # Attempt to use premium features in free tier
        tracker.set_reminder(
            app_id=app1.id,
            reminder_date=datetime.now() + timedelta(days=7),
            reminder_note="Follow up on application"
        )
    except PermissionError as e:
        print(f"Premium feature not available: {str(e)}")
        
    # Initialize Premium Tier
    premium_tracker = ApplicationTracker(user_tier="premium")
    
    # Use premium features
    premium_tracker.add_application(
        company="AI Solutions",
        position="Data Engineer"
    )
    
    # Set reminders
    premium_tracker.set_reminder(
        app_id="1",
        reminder_date=datetime.now() + timedelta(days=7),
        reminder_note="Follow up on application"
    )
    
    # Generate insights
    insights = premium_tracker.generate_insights()
    print("Application Insights:", insights)

if __name__ == "__main__":
    main() 