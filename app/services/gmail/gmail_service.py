import base64

from googleapiclient.discovery import build

from .auth import authenticate


class GmailService:

    def __init__(self):
        credentials = authenticate()
        self.service = build("gmail", "v1", credentials=credentials)

    def get_profile(self):
        return self.service.users().getProfile(userId="me").execute()

    def list_messages(self, max_results=5):
        return (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=max_results)
            .execute()
        )

    def get_message(self, message_id):
        return (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )

    def decode_body(self, payload):
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part["body"].get("data")
                    if data:
                        return base64.urlsafe_b64decode(data).decode(
                            "utf-8",
                            errors="ignore",
                        )

        if payload.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode(
                "utf-8",
                errors="ignore",
            )

        return ""