from app.database.database import SessionLocal
from app.repositories.state_repository import StateRepository
from app.services.gmail.watch_service import GmailWatchService

TOPIC_NAME = "projects/placementmail-ai/topics/gmail_placement_watch"

db = SessionLocal()

try:
    watch = GmailWatchService()

    response = watch.start_watch(TOPIC_NAME)

    repo = StateRepository(db)

    repo.save_state(
        history_id=response["historyId"],
        expiration=response["expiration"],
    )

    print("State initialized successfully!")
    print(response)

finally:
    db.close()