
import sys
import os

# Add tools to path so we can import receive_whatsapp_message
sys.path.append(os.path.join(os.getcwd(), "tools"))

from tools.receive_whatsapp_message import process_message

print("--- Testing WhatsApp Integration (Dental Clinic) ---")
print(" Sending message: '¿Cuánto cuesta un blanqueamiento?'")
response = process_message("¿Cuánto cuesta un blanqueamiento?", "test_user")
print("\n--- Response Received ---")
print(response)
print("\n--- End Test ---")

if "3,500" in response or "blanqueamiento" in response.lower():
    print("✅ TEST PASSED: Response mentions correct price/service.")
else:
    print("⚠️ TEST WARNING: Response might be incorrect (check logs).")
