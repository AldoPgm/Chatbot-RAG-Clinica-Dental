---
description: How to set up and configure the Twilio WhatsApp Sandbox for development
---

# Setup Twilio WhatsApp Sandbox

## Objective  
Configure the Twilio Sandbox so you can send and receive WhatsApp messages during development.

## Required Inputs
- Twilio account (free tier works)
- A phone with WhatsApp installed

## Steps

1. **Get Twilio credentials**  
   - Log in to [Twilio Console](https://console.twilio.com/)
   - Copy your **Account SID** and **Auth Token** from the dashboard
   - Paste them into `.env`:
     ```
     TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     TWILIO_AUTH_TOKEN=your_auth_token_here
     ```

2. **Activate the WhatsApp Sandbox**  
   - Go to **Messaging > Try it Out > Send a WhatsApp message**
   - Follow Twilio's instructions to send the activation message from your phone
   - Note the sandbox number and add it to `.env`:
     ```
     TWILIO_WHATSAPP_NUMBER=+14155238886
     ```

3. **Configure the webhook URL**  
   - Start the local server: `python tools/receive_whatsapp_message.py`
   - Expose it publicly using ngrok: `ngrok http 5000`
   - Copy the ngrok HTTPS URL
   - In Twilio Console > Sandbox Settings, set:
     - **When a message comes in**: `https://your-ngrok-url.ngrok.io/webhook`
     - Method: POST

4. **Test the integration**  
   - Send a WhatsApp message to the sandbox number
   - Verify the message appears in your terminal logs
   - Verify you receive a response back on WhatsApp

## Edge Cases
- **ngrok session expires**: Free tier sessions last 2 hours. Restart ngrok and update the webhook URL
- **Sandbox deactivation**: If you haven't interacted in 72 hours, you may need to resend the activation message
- **Multiple testers**: Each person must send the sandbox activation message individually

## Tools Used
- `tools/receive_whatsapp_message.py`
