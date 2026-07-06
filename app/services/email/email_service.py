from app.repositories.email_repository import EmailRepository


class EmailService:

    def __init__(self, db):
        self.repository = EmailRepository(db)

    def get_all(self):
        return self.repository.get_all()