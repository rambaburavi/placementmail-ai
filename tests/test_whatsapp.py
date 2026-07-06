from app.services.notifications.whatsapp_service import WhatsAppService

service = WhatsAppService()

response = service.send(
    "✅ PlacementMail AI WhatsApp integration successful!"
)

print(response)