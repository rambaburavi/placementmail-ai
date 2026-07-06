from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):
        self.repository = DashboardRepository(db)

    def get_summary(self):
        return self.repository.summary()

    def get_recent(self):
        return self.repository.recent()

    def get_critical(self):
        return self.repository.critical()

    def get_upcoming_deadlines(self):
        return self.repository.upcoming_deadlines()

    def search(self, query: str):
        return self.repository.search(query)

    def get_email(self, email_id: int):
        return self.repository.get_email(email_id)