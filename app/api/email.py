from fastapi import APIRouter
from app.services.email.email_service import EmailService
from app.services.gmail.gmail_service import GmailService
from app.agents.parser.parser_agent import ParserAgent
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.workflows.email_workflow import EmailWorkflow
router = APIRouter()

gmail = GmailService()
parser = ParserAgent()


@router.get("/latest")
def latest_email():

    messages = gmail.list_messages(1)

    message_id = messages["messages"][0]["id"]

    message = gmail.get_message(message_id)

    return parser.parse(message)

@router.post("/process/{message_id}")
def process_email(
    message_id: str,
    db: Session = Depends(get_db)
):
    workflow = EmailWorkflow(db)

    return workflow.process_email(message_id)

@router.post("/process-latest")
def process_latest_email(
    db: Session = Depends(get_db)
):
    gmail = GmailService()

    messages = gmail.list_messages(1)

    message_id = messages["messages"][0]["id"]

    workflow = EmailWorkflow(db)

    return workflow.process_email(message_id)

@router.get("/")
def get_all_emails(
    db: Session = Depends(get_db)
):
    service = EmailService(db)

    emails = service.get_all()

    return [
        {
            "id": email.id,
            "company": email.company,
            "subject": email.subject,
            "priority": email.priority,
            "category": email.category,
            "deadline": email.deadline,
            "created_at": email.created_at,
        }
        for email in emails
    ]
    
@router.post("/process-all")
def process_all_emails(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    gmail = GmailService()

    workflow = EmailWorkflow(db)

    messages = gmail.list_messages(limit)

    if "messages" not in messages:
        return {
            "processed": 0,
            "duplicates": 0,
            "failed": 0,
        }

    processed = 0
    duplicates = 0
    failed = 0

    for message in messages["messages"]:

        try:

            result = workflow.process_email(
                message["id"]
            )

            if result["status"] == "processed":
                processed += 1
            else:
                duplicates += 1

        except Exception as e:

            failed += 1

            print(
                f"Failed {message['id']} : {e}"
            )

    return {
        "processed": processed,
        "duplicates": duplicates,
        "failed": failed,
        "total": len(messages["messages"]),
    }