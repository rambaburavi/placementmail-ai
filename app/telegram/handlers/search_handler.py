from app.services.telegram.telegram_command_service import TelegramCommandService


class SearchHandler:

    def __init__(self, db):
        self.service = TelegramCommandService(db)

    def handle(self, query: str):

        if not query:
            return (
                "Usage:\n"
                "/search Qualcomm"
            )

        return self.service.search(query)