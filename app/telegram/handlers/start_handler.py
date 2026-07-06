from app.services.telegram.telegram_command_service import TelegramCommandService


class StartHandler:

    def __init__(self, db):
        self.service = TelegramCommandService(db)

    def handle(self):

        return (
            "👋 <b>Welcome to PlacementMail AI</b>\n\n"
            "Your AI Placement Assistant.\n\n"
            "Available Commands:\n\n"
            "📅 /today\n"
            "🔴 /critical\n"
            "⏰ /upcoming\n"
            "🔍 /search Qualcomm\n"
            "📊 /summary\n"
            "⚙️ /status\n"
            "❓ /help"
        )