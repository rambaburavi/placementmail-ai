from sqlalchemy.orm import Session

from app.models.gmail_state import GmailState


class StateRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_state(self):
        return self.db.query(GmailState).first()

    def save_state(
        self,
        history_id: str,
        expiration: str,
    ):
        state = self.get_state()

        if state:
            state.latest_history_id = history_id
            state.watch_expiration = expiration
        else:
            state = GmailState(
                latest_history_id=history_id,
                watch_expiration=expiration,
            )
            self.db.add(state)

        self.db.commit()
        self.db.refresh(state)

        return state