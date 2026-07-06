from app.services.notifications.telegram_service import TelegramService

telegram = TelegramService()

response = telegram.send(
    "✅ PlacementMail AI Telegram integration successful!"
)

print(response)