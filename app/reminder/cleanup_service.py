from app.repositories.reminder_repository import ReminderRepository


class ReminderCleanupService:

    def __init__(self, db):
        self.repository = ReminderRepository(db)

    def cleanup(self):

        deleted = self.repository.delete_completed()

        print(f"🧹 Cleaned up {deleted} reminder(s)")