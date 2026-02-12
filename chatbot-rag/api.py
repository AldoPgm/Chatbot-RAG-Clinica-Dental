"""
BillEasy RAG Chatbot — FastAPI Backend
========================================
REST API for the RAG chatbot with endpoints for chat,
document management, and system status.

Run:
    uvicorn api:app --reload --port 8000

Docs:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from src.chatbot import RAGChatbot
from src.utils import Config

# ─── App Setup ───────────────────────────────────────────
app = FastAPI(
    title="BillEasy RAG Chatbot API",
    description="API REST para el asistente de soporte técnico de BillEasy, "
                "basado en Retrieval-Augmented Generation (RAG).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Singleton Chatbot ──────────────────────────────────
chatbot = RAGChatbot()


# ─── Pydantic Models ────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")

    model_config = {"json_schema_extra": {"examples": [{"message": "¿Cómo instalo BillEasy en Windows?"}]}}


class SourceInfo(BaseModel):
    source: str
    chunk: str
    relevance: float


class ChatResponseModel(BaseModel):
    answer: str
    sources: list[SourceInfo]
    confidence: float
    response_time_ms: float
    docs_consulted: int
    is_confident: bool


class StatusResponse(BaseModel):
    documents_loaded: int
    memory_messages: int
    metrics: dict
    collection_stats: dict


class FeedbackRequest(BaseModel):
    message: str = Field(..., description="The original user message")
    feedback: str = Field(..., pattern="^(positive|negative)$", description="positive or negative")


# ─── Endpoints ───────────────────────────────────────────

@app.get("/", tags=["General"])
async def root():
    """Health check and API info."""
    return {
        "service": "BillEasy RAG Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "documents_loaded": chatbot.em.document_count,
    }


@app.post("/chat", response_model=ChatResponseModel, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Send a message and receive an AI-generated response based on the knowledge base.

    The response includes:
    - The answer text with source citations
    - Confidence score (0-1)
    - List of source documents used
    - Response time in milliseconds
    """
    if chatbot.em.document_count == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents loaded. Use POST /documents/load-samples or upload documents first.",
        )

    response = chatbot.chat(request.message)

    return ChatResponseModel(
        answer=response.answer,
        sources=[
            SourceInfo(
                source=s["source"],
                chunk=s["chunk"],
                relevance=s["relevance"],
            )
            for s in response.sources
        ],
        confidence=round(response.confidence, 4),
        response_time_ms=round(response.response_time * 1000, 2),
        docs_consulted=response.docs_consulted,
        is_confident=response.is_confident,
    )


@app.post("/documents/upload", tags=["Documents"])
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to the knowledge base.
    Supported formats: PDF, TXT, DOCX, MD.
    """
    allowed = {".pdf", ".txt", ".docx", ".md"}
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{ext}'. Allowed: {', '.join(sorted(allowed))}",
        )

    content = await file.read()
    count = chatbot.load_uploaded_file(content, file.filename)

    return {
        "success": True,
        "filename": file.filename,
        "chunks_created": count,
        "total_documents": chatbot.em.document_count,
    }


@app.post("/documents/load-samples", tags=["Documents"])
async def load_sample_documents():
    """Load the built-in BillEasy sample documents."""
    count = chatbot.load_sample_documents()
    return {
        "success": True,
        "chunks_loaded": count,
        "total_documents": chatbot.em.document_count,
    }


@app.get("/documents", tags=["Documents"])
async def list_documents():
    """Get information about loaded documents."""
    return chatbot.em.get_collection_stats()


@app.delete("/documents", tags=["Documents"])
async def clear_documents():
    """Clear all documents from the knowledge base."""
    chatbot.em.clear_collection()
    return {"success": True, "message": "All documents cleared."}


@app.delete("/history", tags=["Chat"])
async def clear_history():
    """Clear conversation memory."""
    chatbot.clear_memory()
    return {"success": True, "message": "Conversation history cleared."}


@app.get("/status", response_model=StatusResponse, tags=["System"])
async def get_status():
    """Get system status, metrics, and configuration."""
    status = chatbot.get_status()
    return StatusResponse(
        documents_loaded=status["documents_loaded"],
        memory_messages=status["memory_messages"],
        metrics=status["metrics"],
        collection_stats=status["collection_stats"],
    )


@app.post("/feedback", tags=["Chat"])
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback (👍 positive / 👎 negative) for a response."""
    return {
        "success": True,
        "feedback": request.feedback,
        "message": "Feedback recorded. Thank you!",
    }
