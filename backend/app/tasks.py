from celery import Celery

# celery uses redis as the broker
celery = Celery(
    "placement",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


@celery.task
def daily_report():
    """Placeholder daily report task - counts everything in the portal.

    In a real app this would email the report to the admin. For now it
    just builds the summary and prints it so we can see the task ran.
    """
    from app import create_app
    from app.models import Student, Company, Drive, Application

    app = create_app()

    with app.app_context():
        summary = {
            "students": Student.query.count(),
            "companies": Company.query.count(),
            "drives": Drive.query.count(),
            "applications": Application.query.count(),
        }

    print("Daily report:", summary)
    return summary


# run the report once a day
celery.conf.beat_schedule = {
    "daily-report": {
        "task": "app.tasks.daily_report",
        "schedule": 86400.0,
    }
}
