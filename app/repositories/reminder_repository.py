from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.email_reminder import EmailReminder


class ReminderRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_reminder(self, reminder: EmailReminder) -> EmailReminder:
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def get_by_id(self, reminder_id: int) -> EmailReminder | None:
        return (
            self.db.query(EmailReminder)
            .filter(EmailReminder.id == reminder_id)
            .first()
        )

    def get_by_job_id(self, job_id: str) -> EmailReminder | None:
        return (
            self.db.query(EmailReminder)
            .filter(EmailReminder.job_id == job_id)
            .first()
        )

    def exists(self, job_id: str) -> bool:
        return (
            self.db.query(EmailReminder)
            .filter(EmailReminder.job_id == job_id)
            .first()
            is not None
        )

    def get_email_reminders(self, email_id: int) -> list[EmailReminder]:
        return (
            self.db.query(EmailReminder)
            .filter(EmailReminder.email_id == email_id)
            .order_by(EmailReminder.reminder_time)
            .all()
        )

    def get_pending_reminders(self) -> list[EmailReminder]:
        now = datetime.now()

        return (
            self.db.query(EmailReminder)
            .filter(
                EmailReminder.status.in_(["PENDING", "SCHEDULED"]),
                EmailReminder.reminder_time > now,
            )
            .order_by(EmailReminder.reminder_time)
            .all()
        )

    def get_failed_reminders(self) -> list[EmailReminder]:
        return (
            self.db.query(EmailReminder)
            .filter(EmailReminder.status == "FAILED")
            .all()
        )

    def mark_pending(self, reminder_id: int):
        reminder = self.get_by_id(reminder_id)

        if reminder:
            reminder.status = "PENDING"
            reminder.updated_at = datetime.now()
            self.db.commit()

    def mark_scheduled(self, reminder_id: int):
        reminder = self.get_by_id(reminder_id)

        if reminder:
            reminder.status = "SCHEDULED"
            reminder.updated_at = datetime.now()
            self.db.commit()

    def mark_sent(self, reminder_id: int):
        reminder = self.get_by_id(reminder_id)

        if reminder:
            reminder.status = "SENT"
            reminder.sent_at = datetime.now()
            reminder.updated_at = datetime.now()
            self.db.commit()

    def mark_failed(self, reminder_id: int):
        reminder = self.get_by_id(reminder_id)

        if reminder:
            reminder.status = "FAILED"
            reminder.updated_at = datetime.now()
            self.db.commit()

    def delete_completed(self):

        cutoff = datetime.now() - timedelta(days=30)

        reminders = (
            self.db.query(EmailReminder)
            .filter(
                EmailReminder.status == "SENT",
                EmailReminder.reminder_time < cutoff,
            )
            .all()
        )

        deleted = len(reminders)

        for reminder in reminders:
            self.db.delete(reminder)

        self.db.commit()

        return deleted