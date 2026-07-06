from app.services.telegram.telegram_command_service import TelegramCommandService


class TodayHandler:

    def __init__(self, db):
        self.service = TelegramCommandService(db)

    def handle(self):
        return self.service.get_today()