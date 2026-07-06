from apscheduler.schedulers.background import BackgroundScheduler

from app.database.database import SessionLocal

from app.repositories.state_repository import StateRepository
from app.services.gmail.watch_service import GmailWatchService

from app.reminder.retry_service import ReminderRetryService
from app.reminder.cleanup_service import ReminderCleanupService


TOPIC_NAME = (
    "projects/placementmail-ai/topics/gmail_placement_watch"
)

scheduler = BackgroundScheduler()


def renew_gmail_watch():

    db = SessionLocal()

    try:

        watch = GmailWatchService()

        response = watch.renew_watch(TOPIC_NAME)

        repository = StateRepository(db)

        repository.save_state(
            history_id=response["historyId"],
            expiration=response["expiration"],
        )

        print("✅ Gmail Watch Renewed")

    except Exception as e:

        print(f"Watch Renewal Failed: {e}")

    finally:

        db.close()


def retry_failed():

    db = SessionLocal()

    try:

        ReminderRetryService(db).retry_failed()

    except Exception as e:

        print(f"Retry Failed: {e}")

    finally:

        db.close()


def cleanup():

    db = SessionLocal()

    try:

        ReminderCleanupService(db).cleanup()

    except Exception as e:

        print(f"Cleanup Failed: {e}")

    finally:

        db.close()


def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(
        renew_gmail_watch,
        trigger="interval",
        hours=24,
        id="gmail_watch_renewal",
        replace_existing=True,
    )

    scheduler.add_job(
        retry_failed,
        trigger="interval",
        minutes=5,
        id="retry_failed_reminders",
        replace_existing=True,
    )

    scheduler.add_job(
        cleanup,
        trigger="interval",
        hours=12,
        id="cleanup_reminders",
        replace_existing=True,
    )

    scheduler.start()

    print("✅ Scheduler Started")