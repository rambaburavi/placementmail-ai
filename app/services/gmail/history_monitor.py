from app.database.database import SessionLocal
from app.repositories.state_repository import StateRepository
from app.services.gmail.history_service import HistoryService
from app.services.gmail.gmail_service import GmailService


class HistoryMonitor:

    def run(self):

        from app.workflows.email_workflow import EmailWorkflow

        db = SessionLocal()

        try:

            state_repo = StateRepository(db)

            state = state_repo.get_state()

            # ---------------------------------------------
            # First startup on a fresh deployment
            # ---------------------------------------------
            if state is None:

                print("⚠ No Gmail history state found.")
                print("🔄 Initializing Gmail history...")

                gmail = GmailService()

                profile = (
                    gmail.service.users()
                    .getProfile(userId="me")
                    .execute()
                )

                history_id = profile["historyId"]

                state_repo.save_state(
                    history_id=history_id,
                    expiration=""
                )

                print(f"✅ Gmail history initialized: {history_id}")

                return

            print("🔍 Checking Gmail history...")

            history_service = HistoryService()

            result = history_service.get_new_messages(
    state.latest_history_id
)

            message_ids = result["message_ids"]

            latest_history_id = result["history_id"]

            if not message_ids:

                print("📭 No new emails.")

                return

            print(f"📨 Found {len(message_ids)} new email(s)")

            workflow = EmailWorkflow(db)

            for message_id in message_ids:

                try:

                    workflow.process_email(message_id)

                except Exception as e:

                    print(f"❌ Email processing failed: {e}")

            # ---------------------------------------------
            # Update latest history id
            # ---------------------------------------------
            state_repo.update_history_id(
    latest_history_id
)

            print("✅ Gmail history updated.")

        finally:

            db.close()