from app.database.init_db import init_db
from app.database.database import SessionLocal
from app.repositories.state_repository import StateRepository

# Create tables
init_db()

db = SessionLocal()

repo = StateRepository(db)

state = repo.save_state(
    history_id="563288",
    expiration="1783240665866",
)

print(state.latest_history_id)
print(state.watch_expiration)

db.close()