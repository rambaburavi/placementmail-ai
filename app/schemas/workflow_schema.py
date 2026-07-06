from pydantic import BaseModel


class WorkflowResponse(BaseModel):
    status: str
    gmail_message_id: str
    subject: str
    sender: str
    category: str
    priority: str
    placement_related: bool
    company: str
    summary: str