from sqlalchemy.orm import Session

from app.models.email import Email


class EmailRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_message_id(self, gmail_message_id: str):

        return (
            self.db.query(Email)
            .filter(
                Email.gmail_message_id == gmail_message_id
            )
            .first()
        )

    def save(self, email: Email):

        self.db.add(email)

        self.db.commit()

        self.db.refresh(email)

        return email
    
    def get_by_id(self, email_id):
    
        return (
        self.db.query(Email)
        .filter(
            Email.id == email_id
        )
        .first()
    )
        
    def update(self, email):
    
        self.db.commit()
        self.db.refresh(email)

        return email
    
    def get_all(self):
    
        return (
        self.db.query(Email)
        .order_by(Email.created_at.desc())
        .all()
    )