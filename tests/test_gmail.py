from app.services.gmail.gmail_service import GmailService
from app.agents.parser_agent import ParserAgent

gmail = GmailService()

parser = ParserAgent()

messages = gmail.list_messages(1)

message_id = messages["messages"][0]["id"]

message = gmail.get_message(message_id)

parsed = parser.parse(message)

print(parsed)