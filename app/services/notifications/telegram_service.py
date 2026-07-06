import requests

from app.config.settings import settings


class TelegramService:

    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID

    # ------------------------------------------
    # Send to default chat
    # ------------------------------------------

    def send(self, message: str):
        return self.send_message(self.chat_id, message)

    # ------------------------------------------
    # Send to any chat
    # ------------------------------------------

    def send_message(self, chat_id: str, message: str):

        url = (
            f"https://api.telegram.org/bot{self.token}/sendMessage"
        )

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
        }

        response = requests.post(
            url,
            json=payload,
            timeout=15,
        )

        response.raise_for_status()

        return response.json()

    # ------------------------------------------
    # Get Telegram Updates
    # ------------------------------------------

    def get_updates(self, offset=None):

        url = (
            f"https://api.telegram.org/bot{self.token}/getUpdates"
        )

        params = {
            "timeout": 30,
        }

        if offset is not None:
            params["offset"] = offset

        response = requests.get(
            url,
            params=params,
            timeout=35,
        )

        response.raise_for_status()

        return response.json()