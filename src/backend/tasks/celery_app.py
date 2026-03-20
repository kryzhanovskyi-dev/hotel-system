from celery import Celery

from backend.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "backend.tasks.tasks",
    ]
)

celery_instance.conf.beat_schedule = {
    "bookings": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}

# export PYTHONPATH=$PYTHONPATH:./src
# celery --app=backend.tasks.celery_app:celery_instance worker --loglevel=info -B
