import base64
import json
import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.state_repository import StateRepository
from app.services.gmail.history_service import HistoryService
from app.workflows.email_workflow import EmailWorkflow

router = APIRouter()


@router.post("/gmail")
async def gmail_webhook(
    payload: dict,
    db: Session = Depends(get_db),
):
    """
    Receives Gmail Push Notifications from Google Pub/Sub.
    """

    try:

        # --------------------------------------------------
        # Validate Pub/Sub payload
        # --------------------------------------------------

        if "message" not in payload:
            return {"status": "ignored"}

        pubsub_message = payload["message"]

        encoded_data = pubsub_message.get("data")

        if not encoded_data:
            return {"status": "no_data"}

        decoded = json.loads(
            base64.b64decode(encoded_data).decode("utf-8")
        )

        latest_history_id = decoded["historyId"]

        # --------------------------------------------------
        # Load previous Gmail state
        # --------------------------------------------------

        state_repository = StateRepository(db)

        state = state_repository.get_state()

        if state is None:
            raise HTTPException(
                status_code=500,
                detail="Gmail state not initialized.",
            )

        # --------------------------------------------------
        # Fetch new Gmail messages
        # --------------------------------------------------

        history_service = HistoryService()

        message_ids = history_service.get_new_messages(
            state.latest_history_id
        )

        # --------------------------------------------------
        # Process each email
        # --------------------------------------------------

        workflow = EmailWorkflow(db)

        processed = []

        for message_id in message_ids:

            print(f"📨 Processing Gmail Message: {message_id}")

            result = workflow.process_email(message_id)

            processed.append(result)

        # --------------------------------------------------
        # Save latest history id
        # --------------------------------------------------

        state_repository.save_state(
            history_id=latest_history_id,
            expiration=state.watch_expiration,
        )

        return {
            "status": "success",
            "processed_count": len(processed),
            "processed": processed,
        }

    except Exception as e:

        print("\n" + "=" * 80)
        print("❌ WEBHOOK ERROR")
        print("=" * 80)

        traceback.print_exc()

        print("=" * 80)
        print(f"Exception: {e}")
        print("=" * 80 + "\n")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )