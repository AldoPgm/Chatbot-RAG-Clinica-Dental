"""
Tool: Send WhatsApp Message via Twilio
========================================
Sends a WhatsApp message to a specified recipient using the Twilio API.

Inputs:
    - to_number (str): Recipient's WhatsApp number in E.164 format (e.g., +5491123456789)
    - message_body (str): The text content to send

Outputs:
    - dict: { "success": bool, "sid": str | None, "error": str | None }

Requirements:
    - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER in .env
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def send_whatsapp_message(to_number: str, message_body: str) -> dict:
    """Send a WhatsApp message using Twilio."""
    try:
        from twilio.rest import Client

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        if not all([account_sid, auth_token, from_number]):
            return {
                "success": False,
                "sid": None,
                "error": "Missing Twilio credentials in .env"
            }

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message_body,
            from_=f"whatsapp:{from_number}",
            to=f"whatsapp:{to_number}"
        )

        return {
            "success": True,
            "sid": message.sid,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "sid": None,
            "error": str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_whatsapp_message.py <to_number> <message>")
        sys.exit(1)

    result = send_whatsapp_message(sys.argv[1], sys.argv[2])
    print(result)
