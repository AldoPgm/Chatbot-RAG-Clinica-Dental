---
description: Guía paso a paso para configurar el Sandbox de WhatsApp en Twilio (Gratis)
---

# 📱 Configuración de Twilio Sandbox para WhatsApp

Sigue estos pasos para conectar tu chatbot (en Replit o local) a WhatsApp usando la cuenta gratuita de Twilio.

## 1. Crear/Entrar a tu cuenta Twilio
Ve a [console.twilio.com](https://console.twilio.com) e inicia sesión. Si es cuenta nueva, tendrás créditos de prueba gratuitos.

## 2. Activar el Sandbox
1. En el menú de la izquierda, ve a **Messaging** > **Try it out** > **Send a WhatsApp message**.
2. Verás un número de teléfono de Twilio (ej: `+1 415 523 8886`) y un código (ej: `join algo-algo`).
3. Desde tu celular, abre WhatsApp y envía ese código a ese número.
4. Twilio responderá confirmando que el Sandbox está activo. ✅

## 3. Conectar el Webhook (Tu Cerebro)
1. En la misma pantalla del Sandbox, busca la pestaña **"Sandbox Settings"** (al lado de tu número).
2. Busca el campo **"When a message comes in"**.
3. Pega la URL de tu servidor.
   - **Si usas Replit:** `https://tuchatbot.replit.co/webhook`
   - **Si usas Ngrok:** `https://tu-url-ngrok.app/webhook`
4. Asegúrate de que el método sea **POST**.
5. Dale clic a **Save**.

## 4. ¡Probar!
¡Listo! Ahora todo lo que escribas en ese chat de WhatsApp será enviado a tu servidor, procesado por la IA, y respondido automáticamente.

> **Nota:** En el modo Sandbox gratuito, solo puedes mensajear con números que se hayan unido previamente (enviando el código `join`). Para producción necesitas aprobar un número propio de WhatsApp Business.
