# tests/test_renew.py

from app.services.gmail.watch_service import GmailWatchService

TOPIC = "projects/placementmail-ai/topics/gmail_placement_watch"

watch = GmailWatchService()

response = watch.renew_watch(TOPIC)

print(response)