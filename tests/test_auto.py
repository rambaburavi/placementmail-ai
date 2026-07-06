from datetime import datetime, timedelta

from app.scheduler.scheduler import scheduler
from app.reminder.reminder_scheduler import ReminderScheduler

# Start APScheduler
scheduler.start()

reminder = ReminderScheduler()

reminder.schedule(
    email_id=1,
    label="test",
    reminder_time=datetime.now() + timedelta(seconds=30),
)

print("Waiting for reminder...")
input()