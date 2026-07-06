from sqlalchemy.orm import Session

from app.models.gmail_state import GmailState


class StateRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_state(self):
        return self.db.query(GmailState).first()

    def get_history_id(self):
        state = self.get_state()

        if state:
            return state.latest_history_id

        return None

    def get_watch_expiration(self):
        state = self.get_state()

        if state:
            return state.watch_expiration

        return None

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

    def update_history_id(self, history_id: str):

        state = self.get_state()

        if state is None:
            return None

        state.latest_history_id = history_id

        self.db.commit()

        self.db.refresh(state)

        return state

    def update_watch_expiration(
        self,
        expiration: str,
    ):

        state = self.get_state()

        if state is None:
            return None

        state.watch_expiration = expiration

        self.db.commit()

        self.db.refresh(state)

        return state