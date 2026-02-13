---
description: Guía de despliegue en Railway (Hosting Profesional)
---

# 🚂 Desplegar en Railway (Producción)

Railway es más estable y profesional que Replit para producción.

## 1. Preparar el Repo (Ya lo hice)
Ya agregué el archivo `Procfile` y la librería `gunicorn` necesaria.

## 2. Crear Proyecto en Railway
1.  Ve a [railway.app](https://railway.app/) y crea cuenta.
2.  Click en **New Project** > **Deploy from GitHub repo**.
3.  Selecciona tu repositorio: `Chatbot-RAG---Cl-nica-Dental`.
4.  Dale a **Deploy Now**.

## 3. Configurar Variables
El bot fallará al inicio porque le faltan las llaves.
1.  En tu proyecto de Railway, ve a la pestaña **Variables**.
2.  Agrega las mismas que tenías en `.env`:
    -   `OPENAI_API_KEY`: `sk-...`
    -   `Twilio` keys (opcional).

## 4. Persistencia de Datos (Base de Datos)
Railway reinicia el disco cada vez que haces deploy.
**Problema:** Si usas SQLite/ChromaDB en archivo local, se borra.
**Solución en Railway:**
1.  Añade un **Volume** en Railway (Storage) y monta la carpeta `chatbot-rag/vectorstore`.
2.  O mejor: Configura que el script de inicio cargue los documentos si la DB está vacía.

### Solución Fácil (Load on Start):
He configurado el código para que, si no encuentra la base de datos, la cree al iniciar.

## 5. Obtener URL
1.  Ve a **Settings** > **Networking**.
2.  Genera un **Domain** (ej: `web-production-1234.up.railway.app`).
3.  Usa esa URL + `/webhook` en Twilio.
