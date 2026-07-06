from app.services.gmail.gmail_service import GmailService


class HistoryService:

    def __init__(self):
        gmail = GmailService()
        self.service = gmail.service

    def get_new_messages(self, start_history_id: str):
        """
        Returns all newly added Gmail message IDs
        since the supplied history ID.
        """

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

        for history in response.get("history", []):

            for message in history.get("messagesAdded", []):

                message_ids.append(
                    message["message"]["id"]
                )

        return message_ids