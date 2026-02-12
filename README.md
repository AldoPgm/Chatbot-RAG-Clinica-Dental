# 🤖 WhatsApp Chatbot

Chatbot inteligente para WhatsApp construido con el **framework WAT** (Workflows, Agents, Tools).

## Arquitectura

```
WAT Framework
├── Workflows → Instrucciones (SOPs en Markdown)
├── Agents    → Decisiones inteligentes (AI)
└── Tools     → Ejecución determinista (Python scripts)
```

## Estructura del Proyecto

```
.
├── tools/                          # Scripts de ejecución
│   ├── send_whatsapp_message.py    # Enviar mensajes via Twilio
│   ├── receive_whatsapp_message.py # Webhook para recibir mensajes
│   ├── generate_ai_response.py     # Respuestas AI (Gemini/OpenAI)
│   └── google_sheets.py            # Integración con Google Sheets
├── workflows/                      # SOPs (Standard Operating Procedures)
│   ├── handle_incoming_message.md  # Flujo de mensajes entrantes
│   ├── setup_twilio_sandbox.md     # Configuración de Twilio
│   ├── deploy_chatbot.md           # Guía de deploy
│   └── export_to_sheets.md        # Exportación de datos
├── .tmp/                           # Archivos temporales (regenerables)
├── .env                            # Variables de entorno (NO commitear)
├── requirements.txt                # Dependencias Python
├── CLAUDE.md                       # Instrucciones del agente
└── README.md                       # Este archivo
```

## Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Edita `.env` con tus credenciales:

```env
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_NUMBER=+14155238886
GEMINI_API_KEY=tu_gemini_key
```

### 3. Configurar Twilio Sandbox

Sigue las instrucciones en `workflows/setup_twilio_sandbox.md`.

### 4. Iniciar el servidor

```bash
python tools/receive_whatsapp_message.py
```

### 5. Exponer el webhook (desarrollo)

```bash
ngrok http 5000
```

## Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| Mensajería | Twilio WhatsApp API |
| AI | Google Gemini / OpenAI GPT-4 |
| Backend | Python + Flask |
| Datos | Google Sheets API |

## Workflows Disponibles

| Workflow | Descripción |
|---------|-------------|
| `handle_incoming_message.md` | Flujo completo de recepción y respuesta |
| `setup_twilio_sandbox.md` | Configuración inicial de Twilio |
| `deploy_chatbot.md` | Deploy a producción |
| `export_to_sheets.md` | Exportar datos a Google Sheets |

## Licencia

Este proyecto es privado.
