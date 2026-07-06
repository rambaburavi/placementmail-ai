import requests

from app.config.settings import settings


class WhatsAppService:

    GRAPH_URL = "https://graph.facebook.com/v25.0"

    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.recipient = settings.WHATSAPP_RECIPIENT_NUMBER

    def send(self, message: str):

        url = (
            f"{self.GRAPH_URL}/"
            f"{self.phone_number_id}/messages"
        )

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": self.recipient,
            "type": "text",
            "text": {
                "body": message,
            },
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
        )
        print("Status:", response.status_code)
        print(response.text)

        return response.json()