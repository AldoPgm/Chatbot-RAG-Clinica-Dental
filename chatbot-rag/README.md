# 🦷 Asistente AI - Clínica Dental Sonrisas

> **Chatbot RAG Inteligente** para atención a pacientes, citas y dudas frecuentes.

Este proyecto implementa un chatbot de Inteligencia Artificial que utiliza **RAG (Retrieval Augmented Generation)** para responder preguntas sobre **tratamientos dentales, precios, cuidados postoperatorios y horarios**, basándose exclusivamente en la documentación interna de la clínica.
ita sus fuentes, evalúa la confianza de cada respuesta y maneja preguntas fuera de alcance de forma elegante.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange?logo=openai)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.6-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42-red?logo=streamlit)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                     Streamlit UI                         │
│              (Chat + Upload + Metrics)                   │
├───────────────────────┬─────────────────────────────────┤
│                       │                                  │
│    FastAPI REST API   │     streamlit_app.py             │
│    (api.py)           │                                  │
├───────────────────────┴─────────────────────────────────┤
│                                                          │
│                    RAGChatbot                             │
│              (src/chatbot.py)                            │
│         ┌──────────┼──────────┐                          │
│         ▼          ▼          ▼                           │
│   DocumentLoader  RAGRetriever  ConversationMemory       │
│   (Carga docs)   (Búsqueda)    (Últimos 5 msgs)         │
│         │          │                                     │
│         ▼          ▼                                     │
│   EmbeddingsManager (ChromaDB + OpenAI Embeddings)       │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  Utils: Config | ConversationLogger | MetricsTracker     │
└──────────────────────────────────────────────────────────┘
```

### Flujo de una pregunta

1. El usuario envía una pregunta
2. `RAGRetriever` busca los fragmentos más relevantes en ChromaDB
3. Se evalúa la confianza de los resultados (umbral: 0.7)
4. Se construye un prompt con el contexto + historial de conversación
5. `GPT-4o-mini` genera una respuesta citando las fuentes
6. Se registran métricas y logs de la interacción

---

## 📁 Estructura del Proyecto

```
chatbot-rag/
├── src/                            # Módulos core
│   ├── __init__.py
│   ├── utils.py                    # Config, logging, métricas
│   ├── document_loader.py          # Carga PDF, TXT, DOCX, MD + chunking
│   ├── embeddings_manager.py       # ChromaDB + OpenAI embeddings
│   ├── retriever.py                # Búsqueda semántica + scoring
│   └── chatbot.py                  # Orquestador RAG principal
├── data/
│   └── sample_docs/                # Documentación demo de BillEasy
│       ├── 01_instalacion.md       # Guía de instalación
│       ├── 02_funcionalidades.md   # Features principales
│       ├── 03_troubleshooting.md   # Solución de problemas
│       ├── 04_precios.md           # Planes y precios
│       └── 05_faq.md               # Preguntas frecuentes
├── vectorstore/                    # ChromaDB persistido (auto-generado)
├── .tmp/                           # Logs y métricas (auto-generado)
├── streamlit_app.py                # Interfaz de chat Streamlit
├── api.py                          # API REST con FastAPI
├── requirements.txt                # Dependencias Python
├── .env.example                    # Template de variables de entorno
├── Dockerfile                      # Contenedor Docker
├── .gitignore
└── README.md
```

---

## 🚀 Instalación

### Requisitos previos
- Python 3.10 o superior
- Una API key de OpenAI ([obtener aquí](https://platform.openai.com/api-keys))

### Paso a paso

```bash
# 1. Clonar o navegar al proyecto
cd chatbot-rag

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Edita .env y pega tu OPENAI_API_KEY
```

### Con Docker

```bash
# Construir imagen
docker build -t billeasy-chatbot .

# Ejecutar
docker run -p 8501:8501 --env-file .env billeasy-chatbot
```

---

## 💬 Uso

### Interfaz Streamlit (Recomendado)

```bash
streamlit run streamlit_app.py
```

Abre http://localhost:8501 en tu navegador.

**Pasos:**
1. Haz clic en **"📥 Cargar Documentos de Demo"** en el sidebar
2. Escribe tu pregunta en el chat
3. Revisa las fuentes en el desplegable bajo cada respuesta
4. Usa 👍/👎 para dar feedback

**También puedes subir tus propios documentos** (PDF, TXT, DOCX, MD) desde el sidebar.

### API REST (FastAPI)

```bash
uvicorn api:app --reload --port 8000
```

Documentación interactiva en http://localhost:8000/docs

**Ejemplo con cURL:**

```bash
# Cargar documentos de demo
curl -X POST http://localhost:8000/documents/load-samples

# Hacer una pregunta
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo instalo BillEasy en Windows?"}'

# Subir un documento
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@mi_documento.pdf"

# Ver estado del sistema
curl http://localhost:8000/status
```

---

## ❓ Ejemplos de Preguntas

El chatbot puede responder preguntas como:

| Pregunta | Tipo |
|----------|------|
| ¿Cómo instalo BillEasy en Windows? | Instalación |
| ¿Qué incluye el plan Profesional? | Precios |
| ¿Cómo creo una factura recurrente? | Funcionalidades |
| BillEasy se pone lento, ¿qué hago? | Troubleshooting |
| ¿Mis datos están seguros? | FAQ / Seguridad |
| ¿Se integra con QuickBooks? | Integraciones |
| ¿Cuál es la capital de Francia? | ❌ Fuera de scope |

---

## ⚙️ Configuración

Parámetros ajustables desde el sidebar de Streamlit o modificando `Config` en `src/utils.py`:

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `chunk_size` | 1000 | Tamaño de cada fragmento de texto |
| `chunk_overlap` | 200 | Solapamiento entre fragmentos |
| `top_k` | 4 | Documentos a recuperar por query |
| `confidence_threshold` | 0.7 | Umbral mínimo de relevancia |
| `temperature` | 0.3 | Creatividad del modelo (0=preciso, 1=creativo) |
| `model_name` | gpt-4o-mini | Modelo de OpenAI para respuestas |
| `embedding_model` | text-embedding-3-small | Modelo para embeddings |
| `memory_window` | 5 | Número de intercambios en memoria |

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
|-----------|-----------|-----------|
| Orquestación | LangChain 0.3 | Pipeline RAG |
| LLM | OpenAI GPT-4o-mini | Generación de respuestas |
| Embeddings | text-embedding-3-small | Vectorización de texto |
| Vector DB | ChromaDB | Almacenamiento y búsqueda de vectores |
| Frontend | Streamlit | Interfaz de chat |
| API | FastAPI | Endpoints REST |
| Contenedor | Docker | Deployment |

---

## 📊 Métricas y Logging

El sistema registra automáticamente:

- **Tiempo de respuesta** por consulta
- **Score de confianza** promedio
- **Documentos consultados** por query
- **Consultas con baja confianza** (< 0.7)
- **Historial completo** de conversaciones en `.tmp/conversation_logs/`

---

## 🔮 Mejoras Futuras

- [ ] Soporte para imágenes y tablas en documentos
- [ ] Re-ranking con un modelo cross-encoder
- [ ] Caché de respuestas frecuentes
- [ ] Autenticación de usuarios
- [ ] Dashboard de analytics avanzado
- [ ] Integración con WhatsApp (Twilio)
- [ ] Soporte multi-idioma
- [ ] Fine-tuning del modelo con feedback de usuarios
- [ ] Tests unitarios y de integración
- [ ] RAG evaluation metrics (precision, recall, F1)

---


## ☁️ Despliegue en Replit

Este proyecto está configurado para desplegarse fácilmente en [Replit](https://replit.com).

### Variables de Entorno (Secrets)
Para que funcione en producción, debes configurar las siguientes variables en la sección **Secrets** de Replit:

| Variable | Descripción | Requerida |
|---|---|---|
| `OPENAI_API_KEY` | Tu llave de OpenAI (debe comenzar con `sk-proj...`) | **SÍ** |
| `TWILIO_AUTH_TOKEN` | Token de autenticación de Twilio (si usas validación) | Opcional |
| `APP_PORT` | Puerto del servidor (por defecto 5000) | No |

### Pasos
1. Haz fork de este repositorio.
2. En Replit, selecciona **"Import from GitHub"**.
3. Replit detectará automáticamente `.replit` y `replit.nix`.
4. Configura los **Secrets**.
5. Presiona **Run**.
## 📄 Licencia

Proyecto demostrativo. BillEasy es una empresa ficticia creada con fines educativos.
