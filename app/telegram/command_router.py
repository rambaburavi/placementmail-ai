from app.telegram.handlers.start_handler import StartHandler
from app.telegram.handlers.help_handler import HelpHandler
from app.telegram.handlers.today_handler import TodayHandler
from app.telegram.handlers.critical_handler import CriticalHandler
from app.telegram.handlers.upcoming_handler import UpcomingHandler
from app.telegram.handlers.search_handler import SearchHandler
from app.telegram.handlers.summary_handler import SummaryHandler
from app.telegram.handlers.status_handler import StatusHandler


class CommandRouter:

    def __init__(self, db):

        self.handlers = {
            "/start": StartHandler(db),
            "/help": HelpHandler(db),
            "/today": TodayHandler(db),
            "/critical": CriticalHandler(db),
            "/upcoming": UpcomingHandler(db),
            "/summary": SummaryHandler(db),
            "/status": StatusHandler(db),
        }

        self.search_handler = SearchHandler(db)

    def route(self, text: str):

        if not text:
            return "❌ Empty command."

        parts = text.strip().split(maxsplit=1)

        command = parts[0].lower()

        if command == "/search":

            query = parts[1] if len(parts) > 1 else ""

            return self.search_handler.handle(query)

        handler = self.handlers.get(command)

        if handler:
            return handler.handle()

        return (
            "❌ Unknown command.\n\n"
            "Type /help to see available commands."
        )