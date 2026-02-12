"""
RAG Chatbot — Main Orchestrator
=================================
Ties everything together: retrieval, LLM generation with context,
conversational memory, source citation, and metrics tracking.
"""

from dataclasses import dataclass
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.retriever import RAGRetriever, RetrievalResponse
from src.embeddings_manager import EmbeddingsManager
from src.document_loader import DocumentLoader
from src.utils import (
    Config,
    ConversationLogger,
    MetricsTracker,
    logger,
    DATA_DIR,
)


# ─── System Prompt ──────────────────────────────────────
SYSTEM_PROMPT = """Eres un asistente virtual experto y amable de la **Clínica Dental Sonrisas**.
Tu objetivo es ayudar a los pacientes con información sobre tratamientos, precios, cuidados postoperatorios y horarios, basándote ÚNICAMENTE en los documentos proporcionados.

REGLAS ESTRICTAS:
1. Responde ÚNICAMENTE basándote en el contexto proporcionado abajo.
2. Si la información no está en el contexto, responde exactamente: "No tengo información sobre ese tema en mi base de conocimiento. ¿Puedo ayudarte con nuestros horarios o servicios?"
3. Sé conciso, profesional y empático (es un contexto médico).
4. Si el usuario saluda, preséntate como el Asistente de Dental Sonrisas.
5. Responde siempre en español.

CONTEXTO DE DOCUMENTOS:
{context}
"""

# ─── Response Model ─────────────────────────────────────
@dataclass
class ChatResponse:
    """Structured response from the chatbot."""

    answer: str
    sources: list[dict]
    confidence: float
    response_time: float
    docs_consulted: int
    is_confident: bool  # True if confidence >= threshold
    feedback: Optional[str] = None  # User feedback: 👍 or 👎


class RAGChatbot:
    """
    Production-ready RAG chatbot with:
    - Conversational memory (sliding window)
    - Source citation
    - Confidence scoring
    - Metrics tracking
    - Conversation logging

    Usage:
        chatbot = RAGChatbot()
        chatbot.load_sample_documents()
        response = chatbot.chat("¿Cómo instalo BillEasy en Windows?")
        print(response.answer)
        print(response.sources)
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

        # Core components
        self.doc_loader = DocumentLoader(self.config)
        self.em = EmbeddingsManager(self.config)
        self.retriever = RAGRetriever(self.em, self.config)

        # LLM
        self.llm = ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.openai_api_key,
        )

        # Memory — simple list of (role, content) limited to window size
        self.memory: list[dict] = []

        # Logging & metrics
        self.conv_logger = ConversationLogger()
        self.metrics = MetricsTracker()

        logger.info(
            "RAGChatbot initialized — model=%s, temp=%.1f, memory_window=%d",
            self.config.model_name,
            self.config.temperature,
            self.config.memory_window,
        )

    # ─── Chat ────────────────────────────────────────────

    def chat(self, user_message: str) -> ChatResponse:
        """
        Process a user message through the full RAG pipeline.

        Steps:
            1. Start metrics timer
            2. Retrieve relevant documents
            3. Build prompt with context + memory
            4. Generate LLM response
            5. Update memory
            6. Log interaction & record metrics
            7. Return structured response
        """
        # 1. Start timer
        self.metrics.start_timer()

        # 2. Retrieve context
        retrieval = self.retriever.retrieve(user_message)

        # 3. Build prompt
        context_text = retrieval.get_context_text()
        messages = self._build_messages(user_message, context_text)

        # 4. Generate response
        try:
            llm_response = self.llm.invoke(messages)
            answer = llm_response.content
        except Exception as e:
            logger.error("LLM generation failed: %s", e)
            answer = "Lo siento, hubo un error al procesar tu pregunta. Por favor, intenta nuevamente."

        # 5. Update memory
        self._update_memory(user_message, answer)

        # 6. Record metrics & log
        elapsed = self.metrics.elapsed()
        confidence = retrieval.avg_confidence
        sources = retrieval.get_sources_summary()
        docs_consulted = retrieval.docs_consulted

        self.metrics.record(elapsed, confidence, docs_consulted)
        self.conv_logger.log(
            user_message=user_message,
            assistant_response=answer,
            sources=sources,
            confidence=confidence,
            response_time=elapsed,
            docs_consulted=docs_consulted,
        )

        # 7. Build response
        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            response_time=elapsed,
            docs_consulted=docs_consulted,
            is_confident=confidence >= self.config.confidence_threshold,
        )

    # ─── Document Management ─────────────────────────────

    def load_sample_documents(self) -> int:
        """Load all documents from the data/sample_docs/ directory."""
        if not DATA_DIR.exists():
            logger.warning("Sample docs directory not found: %s", DATA_DIR)
            return 0

        chunks = self.doc_loader.load_directory(DATA_DIR)
        if chunks:
            return self.em.add_documents(chunks)
        return 0

    def load_documents_from_path(self, path: str) -> int:
        """Load documents from a custom directory path."""
        chunks = self.doc_loader.load_directory(path)
        if chunks:
            return self.em.add_documents(chunks)
        return 0

    def load_uploaded_file(self, file_content: bytes, filename: str) -> int:
        """Process an uploaded file (from Streamlit)."""
        chunks = self.doc_loader.load_uploaded_file(
            file_content, filename, DATA_DIR
        )
        if chunks:
            return self.em.add_documents(chunks)
        return 0

    # ─── Memory ──────────────────────────────────────────

    def _build_messages(self, user_message: str, context: str) -> list:
        """Build the full message list for the LLM."""
        messages = [
            SystemMessage(content=SYSTEM_PROMPT.format(context=context))
        ]

        # Add conversation history
        for msg in self.memory:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

        # Add current message
        messages.append(HumanMessage(content=user_message))
        return messages

    def _update_memory(self, user_message: str, assistant_response: str) -> None:
        """Add exchange to memory, trimming to window size."""
        self.memory.append({"role": "user", "content": user_message})
        self.memory.append({"role": "assistant", "content": assistant_response})

        # Keep only the last N exchanges (each exchange = 2 messages)
        max_messages = self.config.memory_window * 2
        if len(self.memory) > max_messages:
            self.memory = self.memory[-max_messages:]

    def clear_memory(self) -> None:
        """Reset conversation memory."""
        self.memory.clear()
        logger.info("Conversation memory cleared.")

    # ─── State ───────────────────────────────────────────

    def clear_all(self) -> None:
        """Reset memory, vector store, and metrics."""
        self.clear_memory()
        self.em.clear_collection()
        logger.info("All data cleared.")

    def get_status(self) -> dict:
        """Return current chatbot status and stats."""
        return {
            "documents_loaded": self.em.document_count,
            "memory_messages": len(self.memory),
            "config": self.config.to_dict(),
            "metrics": self.metrics.summary(),
            "collection_stats": self.em.get_collection_stats(),
        }

    def record_feedback(self, response: ChatResponse, feedback: str) -> None:
        """Record user feedback (👍/👎) for a response."""
        response.feedback = feedback
        logger.info("User feedback recorded: %s", feedback)
