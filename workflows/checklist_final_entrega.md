---
description: Lista maestra de pasos para entregar y cobrar el proyecto
---

# 📋 Checklist Maestro: Entrega a Clínica Dental (Modelo Híbrido)

Usa esta lista para no olvidar ningún paso al entregar el proyecto y asegurar tu cobro mensual.

## 🤝 Fase 1: Reunión con el Cliente (Administrativa)
- [ ] **Acuerdo de Mantenimiento**: Firmar un contrato simple donde se estipule tu tarifa mensual (ej: $100 USD) por mantener el bot.
- [ ] **Tarjetas de Crédito**: Obtener la tarjeta de crédito de la clínica para configurar los pagos automáticos de Twilio y OpenAI. (O hacerlo con ellos en Zoom).
- [ ] **Documentos Legales**: Pedirles PDF de:
    - [ ] Acta Constitutiva o Constancia de Situación Fiscal.
    - [ ] Comprobante de domicilio (Luz/Agua/Teléfono) a nombre de la empresa.
    - [ ] Sitio Web activo (debe mostrar el nombre legal y dirección).

## 🏢 Fase 2: Configuración de Cuentas (Propiedad del Cliente)
- [ ] **Crear Gmail del Bot**: Ej: `bot.clinica@gmail.com` (para no usar correos personales).
- [ ] **Cuenta OpenAI**:
    - [ ] Crear cuenta en [platform.openai.com](https://platform.openai.com).
    - [ ] Agregar tarjeta de crédito (Billing).
    - [ ] Generar `OPENAI_API_KEY` y guardarla.
- [ ] **Cuenta Twilio**:
    - [ ] Crear cuenta en [twilio.com](https://www.twilio.com).
    - [ ] Actualizar a cuenta pagada (Upgrade Project) + Agregar tarjeta.

## ✅ Fase 3: Verificación de Meta (La parte lenta)
*Dentro de la consola de Twilio > WhatsApp Senders:*
- [ ] **Iniciar "New Sender"**: Elegir WhatsApp.
- [ ] **Vincular Meta Business**: Loguearse con el Facebook del dueño de la clínica.
- [ ] **Verificación de Negocio**: Subir los documentos de la Fase 1 a Meta.
- [ ] **Esperar Verificación**: (2-5 días hábiles). Revisar status en [business.facebook.com](https://business.facebook.com).

## 📞 Fase 4: El Número de Teléfono
*Una vez verificado el negocio en Meta:*
- [ ] **Opción A (Nuevo)**: Comprar número local en Twilio (~$1 USD).
- [ ] **Opción B (Portar)**: Iniciar trámite para usar su número actual (OJO: Borrar WA App antes de activar).
- [ ] **Aprobar el Sender**: El número debe aparecer como "Approved" en Twilio.

## 🛠️ Fase 5: Despliegue Técnico (En Railway)
- [ ] **GitHub**: Subir el código final al GitHub (Privado).
- [ ] **Railway**:
    - [ ] Crear proyecto "Deploy from GitHub".
    - [ ] Configurar Variables (`OPENAI_API_KEY`, etc).
- [ ] **Conectar Webhook**:
    - [ ] En Twilio (Sender > Webhook), pegar: `https://tu-proyecto.up.railway.app/webhook`.
    - [ ] Método POST.


## 🚀 Fase 6: Lanzamiento y Cobro
- [ ] **Prueba Final**: Escribir al número real desde un celular personal.
- [ ] **Anuncio**: Que la clínica ponga un botón "Agenda tu Cita" en su web/Facebook que lleve al link de WhatsApp (`wa.me/numerodelbot`).
- [ ] **¡COBRAR!**: Envía tu primera factura de mantenimiento. 💸
