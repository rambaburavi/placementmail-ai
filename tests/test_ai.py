from app.services.gmail.gmail_service import GmailService
from app.agents.parser.parser_agent import ParserAgent
from app.agents.analyzer.analyzer_agent import AnalyzerAgent

gmail = GmailService()

parser = ParserAgent()

ai = AnalyzerAgent()

messages = gmail.list_messages(1)

message = gmail.get_message(
    messages["messages"][0]["id"]
)

parsed = parser.parse(
    message
)

analysis = ai.analyze(
    parsed
)

print(analysis)