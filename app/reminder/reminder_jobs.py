from app.database.database import SessionLocal

from app.repositories.email_repository import EmailRepository
from app.repositories.reminder_repository import ReminderRepository

from app.services.notifications.notification_service import NotificationService


def send_reminder(reminder_id: int):

    db = SessionLocal()

    try:

        reminder_repo = ReminderRepository(db)
        email_repo = EmailRepository(db)

        reminder = reminder_repo.get_by_id(reminder_id)

        if reminder is None:
            return

        # Prevent duplicate notifications
        if reminder.status == "SENT":
            return

        email = email_repo.get_by_id(reminder.email_id)

        if email is None:
            return

        analysis = {
            "subject": f"⏰ Reminder: {email.subject}",
            "company": email.company,
            "priority": email.priority,
            "deadline": email.deadline,
            "summary": email.summary,
            "placement_related": email.placement_related,
            "notify_telegram": True,
            "notify_whatsapp": False,
        }

        try:
            NotificationService().notify(analysis)
            reminder_repo.mark_sent(reminder.id)

        except Exception:
            reminder_repo.mark_failed(reminder.id)
            raise

    finally:
        db.close()