import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class NotificationManager:
    def __init__(self):
        self.client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        self.twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
        self.my_phone = os.getenv("MY_PHONE_NUMBER")
        self.whatsapp_phone = f"whatsapp:{self.my_phone}"
        self.sms_phone = self.my_phone

    def send_sms(self, message_body):
        message = self.client.messages.create(
            body=message_body,
            from_=self.twilio_phone,
            to=self.sms_phone
        )
        print(f"SMS sent: {message.sid}")

    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            body=message_body,
            from_=f"whatsapp:{self.twilio_phone}",
            to=self.whatsapp_phone
        )
        print(f"WhatsApp message sent: {message.sid}")