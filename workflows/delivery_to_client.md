---
description: Guía de modelos de entrega y conexión para clientes reales
---

# 🤝 Cómo entregar este proyecto a tu Cliente (La Clínica)

Tienes el código y el bot funcionando. Ahora, ¿cómo se lo conectas a la clínica y quién paga qué?

Existen dos modelos principales:

## Opción A: Modelo "Agencia" (Recomendado)
**Tú eres el proveedor de servicio completo.**
1.  **Cuentas:** Tú mantienes el código en tu Replit/GitHub y usas tu cuenta de Twilio.
2.  **Cobro:** Tú le cobras una mensualidad a la clínica (ej: $50 - $200 USD/mes) que incluya:
    -   El hosting del bot.
    -   El alquiler del número ($1 USD).
    -   El soporte técnico.
    -   Un margen de ganancia sobre los mensajes de WhatsApp.
3.  **Ventaja:** Generas ingreso recurrente y el cliente no toca nada técnico.

## Opción B: Modelo "Híbrido / Profesional" (Tu Idea) - **MUY RECOMENDADO**
**El cliente paga los costos, tú cobras el servicio.**
1.  **Cuentas:** Le ayudas a crear SUS propias cuentas de Twilio y OpenAI (con SU tarjeta).
2.  **Cobro:**
    -   **Directo:** Ellos pagan las facturas de Twilio/OpenAI ($10-$20/mes).
    -   **A ti:** Les cobras una mensualidad por **Mantenimiento y Soporte** (ej: $50 - $100 USD).
3.  **Ventaja:**
    -   **Transparencia:** Ellos saben que pagan lo justo por uso.
    -   **Seguridad:** Si un mes envían 1 millón de mensajes, lo pagan ellos, no tú.
    -   **Valor:** Tú cobras por mantener el bot inteligente (actualizar precios, promociones), no por revender mensajes.

## Opción C: Modelo "Entrega y Adiós"
**Le entregas el sistema al cliente.**
1.  **Cuentas:** Creas una cuenta de Twilio y Replit a nombre del cliente (con su tarjeta de crédito).
2.  **Cobro:** Le cobras un pago único por el desarrollo e instalación (ej: $500 - $1,500 USD).

3.  **Ventaja:** Te desentiendes de los pagos mensuales y facturas de Twilio.

---

## 📞 ¿Qué número usar?

Este es el punto más crítico con el cliente. Tienes 3 opciones:

### 1. Número Nuevo (La más fácil)
Compras un número nuevo en Twilio (con lada local) por ~$1 USD/mes.
-   **Pro:** No afectas el WhatsApp personal del doctor. Se usa solo para el Bot.
-   **Contra:** Tienen que dar a conocer el nuevo número.

### 2. Línea Fija de la Clínica
Si la clínica tiene teléfono fijo (landline), puedes usar ese número en WhatsApp Business API.
-   **Pro:** Es el número que ya conocen los pacientes.
-   **Cómo:** Twilio te llamará (voz) para darte el código de verificación de WhatsApp.

### 3. Su Celular Actual (Cuidado ⚠️)
Si usan un celular con WhatsApp Business App.
-   **Pro:** Mantienen el número.
-   **Contra:** Para activar el Bot, deben **borrar su cuenta de WhatsApp en el celular**. El número pasa a vivir en la nube (API). **Perderán su historial de chats** si no lo respaldan, y ya no podrán contestar desde el celular (a menos que programes un panel de chat híbrido).

## 🚀 Paso a Paso para la Conexión

1.  **Pídeles sus Papeles:** Pide el Acta Constitutiva o Constancia Fiscal de la clínica.
2.  **Verifica en Facebook:** Entra a su Business Manager (o crea uno) y verifica el negocio.
3.  **Conecta Twilio:** Vincula ese Business Manager con tu cuenta de Twilio.
4.  **Activa el Número:** Elige una de las 3 opciones de arriba.
5.  **Cambia el Webhook:** En Twilio, pon la URL de tu Replit.
6.  **¡Bot Vivo!**: El bot contestará todas las llamadas.
