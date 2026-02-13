---
description: Guía para mover tu bot de Sandbox a Producción (WhatsApp Business API)
---

# 🚀 Pasando a Producción: WhatsApp Business API

El Sandbox de Twilio es solo para pruebas. Para chatear con cualquier persona sin que tenga que enviar un código `join`, necesitas una cuenta oficial.

Este proceso puede tomar desde **2 días hasta 2 semanas** dependiendo de la verificación de Meta (Facebook).

## Paso 1: Tener una cuenta comercial de Meta (Facebook)
Necesitas un **Meta Business Manager**. Si tu clínica ya tiene página de Facebook/Instagram, probablemente ya tengas uno.
- Entra a [business.facebook.com](https://business.facebook.com/) y asegúrate de tener acceso de administrador.

## Paso 2: Soliciar acceso en Twilio
1. En la consola de Twilio, ve a **Messaging > Senders > WhatsApp Senders**.
2. Haz clic en **"Sign up for WhatsApp"** o "New Sender".
3. Twilio te pedirá conectar tu cuenta de Facebook. Esto vinculará tu Twilio con tu Meta Business Manager.

## Paso 3: Verificar tu Negocio
Meta te pedirá documentos para probar que "Clínica Dental Sonrisas" es un negocio real.
- **Documentos comunes:** Acta constitutiva, recibo de luz/teléfono a nombre de la empresa, constancia fiscal.
- **Sitio Web:** Debe funcionar y mostrar el nombre legal del negocio.
- **Estado:** Una vez enviados, Meta tardará unos días en verificar tu negocio.

## Paso 4: Obtener un Número
Una vez verificado:
1. Compra un número nuevo en Twilio (aprox $1-2 USD/mes) O...
2. Trae tu propio número (Portabilidad). *Nota: Si usas tu número actual de WhatsApp Business App, se borrará tu historial de chats de la app, ya que el número pasará a ser controlado por la API.*

## Paso 5: Configurar el Webhook (Igual que en Sandbox)
1. Ve al número que acabas de activar en Twilio (Messaging > Senders > WhatsApp Senders).
2. Busca la sección **Webhook**.
3. Pega la misma URL de Replit: `https://tu-proyecto.replit.co/webhook`.
4. Método: **POST**.

## 🧬 Costos Importantes
A diferencia del Sandbox (gratis), WhatsApp cobra por **conversación** (sesiones de 24h):
- **Iniciada por usuario (Service):** Aprox $0.03 USD.
- **Iniciada por negocio (Utility/Marketing):** Aprox $0.05 USD (requiere plantillas pre-aprobadas).
- **Twilio:** Cobra una pequeña tarifa adicional por mensaje ($0.005 USD).

## ⚠️ Regla de las 24 Horas
Tu bot puede responder libremente dentro de las 24 horas siguientes al último mensaje del usuario. Si pasan 24h, **NO** puedes escribirle nada libre (como "Hola, ¿sigues ahí?"). Para re-iniciar la charla, debes usar una **Plantilla (Template)** aprobada por WhatsApp.
