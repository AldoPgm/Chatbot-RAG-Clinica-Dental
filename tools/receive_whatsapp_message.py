"""
Tool: Receive WhatsApp Message Webhook
========================================
Flask webhook endpoint that receives incoming WhatsApp messages from Twilio.

Inputs:
    - Incoming HTTP POST request from Twilio with message data

Outputs:
    - Processes the incoming message and returns a TwiML response

Requirements:
    - TWILIO_AUTH_TOKEN in .env (for request validation)
    - Flask running on APP_PORT
"""

import os
from dotenv import load_dotenv
from flask import Flask, request
import sys
from twilio.twiml.messaging_response import MessagingResponse

# Add chatbot-rag to python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAG_DIR = os.path.join(BASE_DIR, "chatbot-rag")
if RAG_DIR not in sys.path:
    sys.path.append(RAG_DIR)

try:
    from src.chatbot import RAGChatbot
    rag_chatbot = RAGChatbot()
    print("✅ RAG Chatbot initialized for WhatsApp")
except Exception as e:
    print(f"⚠️ Failed to initialize RAG Chatbot: {e}")
    rag_chatbot = None

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming WhatsApp messages from Twilio."""
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    print(f"[INCOMING] From: {sender} | Message: {incoming_msg}")

    # Process the message (connect to AI agent here)
    response_text = process_message(incoming_msg, sender)

    # Build TwiML response
    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)


def process_message(message: str, sender: str) -> str:
    """
    Process an incoming message and generate a response.
    This is where the AI agent logic connects.

    Args:
        message: The incoming message text
        sender: The sender's WhatsApp number

    Returns:
        Response text to send back
    """
    if rag_chatbot:
        try:
            # 1. Get response from RAG
            response = rag_chatbot.chat(message)
            
            # 2. Format response for WhatsApp
            text = response.answer
            
            # Add sources if available/relevant
            # if response.sources and response.confidence >= 0.7:
            #     sources_text = "\n\n📄 *Fuentes:*\n" + "\n".join(
            #         [f"- {s['source']} ({s['relevance']:.0%})" for s in response.sources[:2]]
            #     )
            #     text += sources_text
                
            return text
        except Exception as e:
            print(f"Error generating RAG response: {e}")
            return "Lo siento, tuve un problema procesando tu mensaje. Intenta nuevamente."
    
    return "El sistema RAG no está disponible en este momento."


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "whatsapp-chatbot"}


if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("APP_ENV") == "development")
