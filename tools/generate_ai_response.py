"""
Tool: Generate AI Response
========================================
Generates an AI-powered response using Google Gemini (or OpenAI as fallback).

Inputs:
    - user_message (str): The user's message to respond to
    - conversation_history (list[dict]): Previous messages for context
    - system_prompt (str): Instructions for the AI's behavior

Outputs:
    - dict: { "success": bool, "response": str | None, "error": str | None }

Requirements:
    - GEMINI_API_KEY or OPENAI_API_KEY in .env
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_response_gemini(
    user_message: str,
    conversation_history: list[dict] = None,
    system_prompt: str = ""
) -> dict:
    """Generate a response using Google Gemini."""
    try:
        import google.generativeai as genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {
                "success": False,
                "response": None,
                "error": "GEMINI_API_KEY not found in .env"
            }

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")

        # Build the prompt with context
        full_prompt = ""
        if system_prompt:
            full_prompt += f"System: {system_prompt}\n\n"

        if conversation_history:
            for msg in conversation_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                full_prompt += f"{role.capitalize()}: {content}\n"

        full_prompt += f"User: {user_message}\nAssistant:"

        response = model.generate_content(full_prompt)

        return {
            "success": True,
            "response": response.text,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "response": None,
            "error": str(e)
        }


def generate_response_openai(
    user_message: str,
    conversation_history: list[dict] = None,
    system_prompt: str = ""
) -> dict:
    """Generate a response using OpenAI (fallback)."""
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "success": False,
                "response": None,
                "error": "OPENAI_API_KEY not found in .env"
            }

        client = OpenAI(api_key=api_key)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        return {
            "success": True,
            "response": response.choices[0].message.content,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "response": None,
            "error": str(e)
        }


def generate_response(
    user_message: str,
    conversation_history: list[dict] = None,
    system_prompt: str = ""
) -> dict:
    """
    Generate an AI response, trying Gemini first, then OpenAI as fallback.
    """
    # Try Gemini first
    if os.getenv("GEMINI_API_KEY"):
        result = generate_response_gemini(user_message, conversation_history, system_prompt)
        if result["success"]:
            return result

    # Fallback to OpenAI
    if os.getenv("OPENAI_API_KEY"):
        result = generate_response_openai(user_message, conversation_history, system_prompt)
        if result["success"]:
            return result

    return {
        "success": False,
        "response": None,
        "error": "No AI API keys configured. Set GEMINI_API_KEY or OPENAI_API_KEY in .env"
    }


if __name__ == "__main__":
    result = generate_response("Hola, ¿qué servicios ofrecen?")
    print(result)
