from pydantic import BaseModel
from typing import List


class Attachment(BaseModel):
    filename: str
    mime_type: str


class EmailSchema(BaseModel):
    message_id: str
    thread_id: str

    sender: str
    subject: str
    timestamp: str

    plain_text: str
    html: str

    attachments: List[Attachment]

    links: List[str]