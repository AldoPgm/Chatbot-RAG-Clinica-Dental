---
description: How to handle an incoming WhatsApp message end-to-end
---

# Handle Incoming WhatsApp Message

## Objective  
Receive an incoming WhatsApp message, process it with the AI model, and send back an intelligent response.

## Required Inputs
- Incoming message body (from Twilio webhook)
- Sender's WhatsApp number
- Conversation history (if available)

## Steps

1. **Receive the message**  
   - The Flask webhook in `tools/receive_whatsapp_message.py` handles the incoming POST from Twilio
   - Extract `Body` (message text) and `From` (sender number) from the request

2. **Load conversation context**  
   - Check if there's an existing conversation for this sender
   - Load the last N messages for context (recommended: last 10)
   - If no history exists, start a new conversation

3. **Generate AI response**  
   - Use `tools/generate_ai_response.py` with:
     - `user_message`: the incoming message text
     - `conversation_history`: previous messages
     - `system_prompt`: loaded from the business-specific prompt template
   - The tool tries Gemini first, falls back to OpenAI

4. **Send the response**  
   - Return the AI response via TwiML in the webhook response
   - For async responses, use `tools/send_whatsapp_message.py`

5. **Log the interaction**  
   - Store both the user message and AI response for conversation history
   - Log to `.tmp/` for debugging if needed

## Edge Cases
- **Empty message**: Respond with a default greeting
- **Media messages** (images, audio): Acknowledge receipt, note that media processing is not yet supported
- **Rate limiting**: If Twilio rate-limits, queue the response and retry after delay
- **AI failure**: If both Gemini and OpenAI fail, send a fallback message: "Estamos experimentando dificultades técnicas. Por favor, intenta nuevamente en unos minutos."

## Tools Used
- `tools/receive_whatsapp_message.py`
- `tools/generate_ai_response.py`
- `tools/send_whatsapp_message.py`
