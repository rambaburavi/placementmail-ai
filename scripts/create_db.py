from app.database.database import engine
from app.database.base import Base

# Import all models
from app.models.email import Email

Base.metadata.create_all(bind=engine)

print("Database created successfully.")