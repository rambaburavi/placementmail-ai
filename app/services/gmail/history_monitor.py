from app.database.database import SessionLocal

from app.repositories.state_repository import StateRepository

from app.services.gmail.history_service import HistoryService


class HistoryMonitor:

    def run(self):
        from app.workflows.email_workflow import EmailWorkflow
        db = SessionLocal()

        try:

            state_repo = StateRepository(db)

            state = state_repo.get_state()

            if state is None:

                print("⚠ No Gmail history state found.")

                return

            history_service = HistoryService()

            message_ids = history_service.get_new_messages(
                state.latest_history_id
            )

            if not message_ids:
                return

            workflow = EmailWorkflow(db)

            for message_id in message_ids:

                try:

                    workflow.process_email(message_id)

                except Exception as e:

                    print(
                        f"Email processing failed: {e}"
                    )

            latest = message_ids[-1]

            gmail = workflow.gmail

            message = gmail.get_message(latest)

            history_id = message["historyId"]

            state_repo.update_history_id(history_id)

            print(
                f"Processed {len(message_ids)} new email(s)"
            )

        finally:

            db.close()