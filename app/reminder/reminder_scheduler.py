from datetime import datetime

from app.scheduler.scheduler import scheduler
from app.reminder.reminder_jobs import send_reminder


class ReminderScheduler:

    def schedule(
    self,
    reminder_id: int,
    email_id: int,
    label: str,
    reminder_time: datetime,
) -> bool:

        reminder_time = reminder_time.replace(tzinfo=None)

        # Skip reminders in the past
        if reminder_time <= datetime.now():
            return False

        job_id = f"{email_id}_{label}"

        # Skip if already scheduled
        if scheduler.get_job(job_id):
            return False

        scheduler.add_job(
            func=send_reminder,
            trigger="date",
            run_date=reminder_time,
            args=[reminder_id],
            id=job_id,
            replace_existing=False,
        )

        return True