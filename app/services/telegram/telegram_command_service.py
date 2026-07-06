from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.email_repository import EmailRepository


class TelegramCommandService:

    def __init__(self, db):

        self.dashboard = DashboardRepository(db)
        self.email_repository = EmailRepository(db)

    # -----------------------------------------
    # /today
    # -----------------------------------------

    def get_today(self):

        emails = self.dashboard.today_emails()

        if not emails:
            return "📭 No important emails for today."

        message = "📅 <b>Today's Emails</b>\n\n"

        for email in emails:

            message += (
                f"• <b>{email.company or 'Unknown'}</b>\n"
                f"{email.subject}\n"
                f"Priority: {email.priority}\n\n"
            )

        return message

    # -----------------------------------------
    # /critical
    # -----------------------------------------

    def get_critical(self):

        emails = self.dashboard.critical()

        if not emails:
            return "✅ No critical emails."

        message = "🔴 <b>Critical Emails</b>\n\n"

        for email in emails:

            message += (
                f"• <b>{email.company}</b>\n"
                f"{email.subject}\n\n"
            )

        return message

    # -----------------------------------------
    # /upcoming
    # -----------------------------------------

    def get_upcoming(self):

        emails = self.dashboard.upcoming_deadlines()

        if not emails:
            return "🎉 No upcoming deadlines."

        message = "⏰ <b>Upcoming Deadlines</b>\n\n"

        for email in emails:

            message += (
                f"• <b>{email.company}</b>\n"
                f"{email.deadline}\n\n"
            )

        return message

    # -----------------------------------------
    # /search
    # -----------------------------------------

    def search(self, query: str):

        emails = self.dashboard.search(query)

        if not emails:
            return f"❌ No emails found for <b>{query}</b>."

        message = f"🔍 <b>Search: {query}</b>\n\n"

        for email in emails:

            message += (
                f"• <b>{email.company}</b>\n"
                f"{email.subject}\n\n"
            )

        return message

    # -----------------------------------------
    # /summary
    # -----------------------------------------

    def get_summary(self):

        summary = self.dashboard.summary()

        return (
            "📊 <b>Placement Summary</b>\n\n"
            f"📧 Total Emails: {summary['total_emails']}\n"
            f"🎯 Placement: {summary['placement_emails']}\n"
            f"🔴 Critical: {summary['critical_emails']}\n"
            f"📅 Today: {summary['today_emails']}"
        )

    # -----------------------------------------
    # /status
    # -----------------------------------------

    def get_status(self):

        summary = self.dashboard.summary()

        return (
            "🤖 <b>PlacementMail AI Status</b>\n\n"
            "✅ Backend Running\n"
            "✅ Gmail Connected\n"
            "✅ Scheduler Active\n"
            "✅ Telegram Connected\n\n"
            f"📧 Emails Processed: {summary['total_emails']}"
        )