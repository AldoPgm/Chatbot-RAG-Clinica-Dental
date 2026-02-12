---
description: How to deploy the chatbot to production
---

# Deploy Chatbot

## Objective  
Deploy the WhatsApp chatbot to a production environment so it can receive messages 24/7.

## Required Inputs
- All `.env` variables configured with production values
- A hosting platform account (Replit, Railway, Render, or similar)

## Steps

1. **Prepare for deployment**  
   - Verify all environment variables are set in `.env`
   - Test locally with `python tools/receive_whatsapp_message.py`
   - Run health check: `curl http://localhost:5000/health`

2. **Choose a hosting platform**  
   - **Replit**: Good for quick deployment, always-on with paid plan
   - **Railway**: Easy deploy from GitHub, free tier available
   - **Render**: Auto-deploy from GitHub, free tier with sleep after inactivity
   - **VPS (DigitalOcean, etc.)**: Full control, recommended for production

3. **Deploy the application**  
   - Push code to GitHub (ensure `.env` and credentials are gitignored)
   - Connect the repository to your hosting platform
   - Set all environment variables in the platform's settings
   - Deploy and note the public URL

4. **Update Twilio webhook**  
   - Go to Twilio Console
   - Replace the ngrok URL with your production URL:
     ```
     https://your-production-url.com/webhook
     ```

5. **Verify deployment**  
   - Send a WhatsApp message to the bot
   - Monitor logs for errors
   - Confirm the response is received

## Edge Cases
- **Cold starts**: Some free platforms sleep after inactivity. First message may be slow.
- **SSL certificates**: Twilio requires HTTPS. Most platforms provide this automatically.
- **Environment variables**: Double-check that ALL keys are set in the platform—missing keys are the #1 deployment issue.

## Tools Used
- `tools/receive_whatsapp_message.py`
- `tools/send_whatsapp_message.py`
- `tools/generate_ai_response.py`
