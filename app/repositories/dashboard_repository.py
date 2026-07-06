from datetime import datetime, timedelta

from sqlalchemy import func

from app.models.email import Email


class DashboardRepository:

    def __init__(self, db):
        self.db = db

    # --------------------------------------------------
    # Dashboard Summary
    # --------------------------------------------------

    def summary(self):

        today = datetime.now().date()

        return {
            "total_emails": self.db.query(Email).count(),

            "today_emails":
                self.db.query(Email)
                .filter(func.date(Email.created_at) == today)
                .count(),

            "placement_emails":
                self.db.query(Email)
                .filter(Email.placement_related == True)
                .count(),

            "critical_emails":
                self.db.query(Email)
                .filter(
                    Email.priority.in_(["Critical", "High"])
                )
                .count(),
        }

    # --------------------------------------------------
    # Recent Emails
    # --------------------------------------------------

    def recent(self, limit=20):

        return (
            self.db.query(Email)
            .order_by(Email.created_at.desc())
            .limit(limit)
            .all()
        )

    # --------------------------------------------------
    # Today's Emails
    # --------------------------------------------------

    def today_emails(self):

        today = datetime.now().date()

        return (
            self.db.query(Email)
            .filter(
                func.date(Email.created_at) == today
            )
            .order_by(Email.created_at.desc())
            .all()
        )

    # --------------------------------------------------
    # Critical Emails
    # --------------------------------------------------

    def critical(self, limit=20):

        return (
            self.db.query(Email)
            .filter(
                Email.priority.in_(["Critical", "High"])
            )
            .order_by(Email.created_at.desc())
            .limit(limit)
            .all()
        )

    # --------------------------------------------------
    # Upcoming Deadlines
    # --------------------------------------------------

    def upcoming_deadlines(self, days=7):

        now = datetime.now()

        future = now + timedelta(days=days)

        return (
            self.db.query(Email)
            .filter(
                Email.deadline_at != None,
                Email.deadline_at >= now,
                Email.deadline_at <= future,
            )
            .order_by(Email.deadline_at)
            .all()
        )

    # --------------------------------------------------
    # Search Emails
    # --------------------------------------------------

    def search(self, q):

        query = f"%{q}%"

        return (
            self.db.query(Email)
            .filter(
                Email.subject.ilike(query)
                | Email.company.ilike(query)
                | Email.sender.ilike(query)
                | Email.category.ilike(query)
            )
            .order_by(Email.created_at.desc())
            .all()
        )

    # --------------------------------------------------
    # Get Email
    # --------------------------------------------------

    def get_email(self, email_id):

        return (
            self.db.query(Email)
            .filter(Email.id == email_id)
            .first()
        )

    # --------------------------------------------------
    # Analytics
    # --------------------------------------------------

    def category_distribution(self):

        results = (
            self.db.query(
                Email.category,
                func.count(Email.id)
            )
            .group_by(Email.category)
            .all()
        )

        return [
            {
                "category": category,
                "count": count,
            }
            for category, count in results
        ]

    def priority_distribution(self):

        results = (
            self.db.query(
                Email.priority,
                func.count(Email.id)
            )
            .group_by(Email.priority)
            .all()
        )

        return [
            {
                "priority": priority,
                "count": count,
            }
            for priority, count in results
        ]

    def company_distribution(self):

        results = (
            self.db.query(
                Email.company,
                func.count(Email.id)
            )
            .filter(Email.company != None)
            .group_by(Email.company)
            .order_by(func.count(Email.id).desc())
            .limit(10)
            .all()
        )

        return [
            {
                "company": company,
                "count": count,
            }
            for company, count in results
        ]

    def placement_statistics(self):

        placement = (
            self.db.query(Email)
            .filter(
                Email.placement_related == True
            )
            .count()
        )

        total = self.db.query(Email).count()

        return {
            "placement": placement,
            "non_placement": total - placement,
            "total": total,
        }

    def daily_trend(self):

        results = (
            self.db.query(
                func.date(Email.created_at),
                func.count(Email.id)
            )
            .group_by(func.date(Email.created_at))
            .order_by(func.date(Email.created_at))
            .all()
        )

        return [
            {
                "date": str(date),
                "count": count,
            }
            for date, count in results
        ]

    # --------------------------------------------------
    # Telegram Assistant
    # --------------------------------------------------

    def total_processed(self):

        return self.db.query(Email).count()

    def placement_count(self):

        return (
            self.db.query(Email)
            .filter(
                Email.placement_related == True
            )
            .count()
        )

    def critical_count(self):

        return (
            self.db.query(Email)
            .filter(
                Email.priority.in_(["Critical", "High"])
            )
            .count()
        )

    def interviews(self):

        return (
            self.db.query(Email)
            .filter(
                Email.category == "Interview"
            )
            .order_by(Email.created_at.desc())
            .all()
        )

    def internships(self):

        return (
            self.db.query(Email)
            .filter(
                Email.category == "Internship"
            )
            .order_by(Email.created_at.desc())
            .all()
        )

    def companies(self):

        return (
            self.db.query(Email.company)
            .distinct()
            .all()
        )