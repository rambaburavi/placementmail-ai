from app.services.notifications.formatter import NotificationFormatter
from app.services.notifications.telegram_service import TelegramService
from app.services.notifications.whatsapp_service import WhatsAppService


class NotificationService:

    def __init__(self):
        self.telegram = TelegramService()
        self.whatsapp = WhatsAppService()

    def notify(self, analysis: dict):

        message = NotificationFormatter.format(analysis)

        # Always send Telegram
        if analysis.get("notify_telegram", True):
            try:
                self.telegram.send(message)
                print("✅ Telegram notification sent")
            except Exception as e:
                print(f"❌ Telegram Error: {e}")

        # WhatsApp is optional
        if analysis.get("notify_whatsapp", False):
            try:
                self.whatsapp.send(message)
                print("✅ WhatsApp notification sent")
            except Exception as e:
                print(f"⚠️ WhatsApp skipped: {e}")