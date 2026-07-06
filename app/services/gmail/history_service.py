from app.services.gmail.gmail_service import GmailService


class HistoryService:

    def __init__(self):
        gmail = GmailService()
        self.service = gmail.service

    def get_new_messages(self, start_history_id: str):

        response = (
            self.service.users()
            .history()
            .list(
                userId="me",
                startHistoryId=start_history_id,
                historyTypes=["messageAdded"],
            )
            .execute()
        )

        message_ids = []

        seen = set()

        for history in response.get("history", []):

            for message in history.get("messagesAdded", []):

                message_id = message["message"]["id"]

                if message_id not in seen:
                    seen.add(message_id)
                    message_ids.append(message_id)

        latest_history_id = response.get(
            "historyId",
            start_history_id,
        )

        return {
            "message_ids": message_ids,
            "history_id": latest_history_id,
        }