from app.services.gmail.gmail_service import GmailService


class GmailWatchService:
    def __init__(self):
        gmail = GmailService()
        self.service = gmail.service

    def start_watch(self, topic_name: str):
        """
        Starts Gmail Push Notification watch.

        Args:
            topic_name: Full Pub/Sub topic name.
            Example:
            projects/my-project/topics/gmail-placement-watch
        """

        request = {
            "topicName": topic_name,
            "labelIds": ["INBOX"],
            "labelFilterBehavior": "INCLUDE",
        }

        response = (
            self.service.users()
            .watch(
                userId="me",
                body=request,
            )
            .execute()
        )

        return response

    def renew_watch(self, topic_name: str):
        """
        Gmail watch expires automatically.
        Renewal is simply another watch request.
        """
        return self.start_watch(topic_name)

    def stop_watch(self):
        """
        Stops Gmail Push notifications.
        """

        response = (
            self.service.users()
            .stop(userId="me")
            .execute()
        )

        return response