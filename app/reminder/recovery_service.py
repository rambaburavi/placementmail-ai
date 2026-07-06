from app.repositories.reminder_repository import ReminderRepository
from app.reminder.reminder_scheduler import ReminderScheduler


class ReminderRecoveryService:

    def __init__(self, db):
        self.repository = ReminderRepository(db)
        self.scheduler = ReminderScheduler()

    def restore(self):

        reminders = self.repository.get_pending_reminders()

        restored = 0

        for reminder in reminders:

            label = reminder.job_id.split("_")[-1]

            scheduled = self.scheduler.schedule(
                reminder_id=reminder.id,
                email_id=reminder.email_id,
                label=label,
                reminder_time=reminder.reminder_time,
            )

            if scheduled:
                restored += 1

        print(f"✅ Restored {restored} reminder(s)")