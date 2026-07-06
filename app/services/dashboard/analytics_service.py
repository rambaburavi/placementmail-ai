from app.repositories.dashboard_repository import DashboardRepository


class AnalyticsService:

    def __init__(self, db):

        self.repository = DashboardRepository(db)

    def categories(self):
        return self.repository.category_distribution()

    def priorities(self):
        return self.repository.priority_distribution()

    def companies(self):
        return self.repository.company_distribution()

    def placement(self):
        return self.repository.placement_statistics()

    def trend(self):
        return self.repository.daily_trend()

    def analytics(self):

        return {
            "categories": self.categories(),
            "priorities": self.priorities(),
            "companies": self.companies(),
            "placement": self.placement(),
            "trend": self.trend(),
        }