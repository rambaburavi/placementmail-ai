from app.services.gmail.history_service import HistoryService

history = HistoryService()

messages = history.get_new_messages("563288")

print(messages)