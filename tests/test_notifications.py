from app.services.notifications.notification_service import NotificationService

notification = NotificationService()

notification.notify(
    {
        "notify_telegram": True,
        "notify_whatsapp": False,
        "placement_related": True,
        "company": "Qualcomm",
        "subject": "Interview Invitation",
        "priority": "Critical",
        "deadline": "Tomorrow",
        "summary": "You have been shortlisted.",
        "action_required": "Attend Online Assessment",
    }
)

print("Done")