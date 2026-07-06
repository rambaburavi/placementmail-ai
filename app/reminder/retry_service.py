from app.repositories.reminder_repository import ReminderRepository
from app.repositories.email_repository import EmailRepository

from app.services.notifications.notification_service import NotificationService


class ReminderRetryService:

    def __init__(self, db):
        self.reminder_repository = ReminderRepository(db)
        self.email_repository = EmailRepository(db)

    def retry_failed(self):

        reminders = self.reminder_repository.get_failed_reminders()

        retried = 0

        for reminder in reminders:

            email = self.email_repository.get_by_id(reminder.email_id)

            if email is None:
                continue

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

                self.reminder_repository.mark_sent(reminder.id)

                retried += 1

            except Exception:

                # Keep it FAILED so it will be retried later
                pass

        print(f"✅ Retried {retried} failed reminder(s)")