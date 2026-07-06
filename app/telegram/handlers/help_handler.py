from app.services.telegram.telegram_command_service import TelegramCommandService


class HelpHandler:

    def __init__(self, db):
        self.service = TelegramCommandService(db)

    def handle(self):

        return (
            "<b>PlacementMail AI Commands</b>\n\n"
            "/today - Today's emails\n"
            "/critical - Critical emails\n"
            "/upcoming - Upcoming deadlines\n"
            "/search <keyword> - Search emails\n"
            "/summary - Dashboard summary\n"
            "/status - System status\n"
            "/help - Show this message"
        )