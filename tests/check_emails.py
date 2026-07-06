from app.database.database import SessionLocal
from app.models.email import Email

db = SessionLocal()

emails = db.query(Email).order_by(Email.id.desc()).all()

for email in emails:
    print(email.id, email.subject, email.sender)

db.close()