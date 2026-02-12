"""
Utils Module — Configuration, Logging & Metrics
=================================================
Central configuration, structured logging, conversation logging,
and performance metrics tracking for the RAG chatbot.
"""

import os
import json
import time
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# ─── Paths ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "sample_docs"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
LOGS_DIR = BASE_DIR / ".tmp" / "conversation_logs"
METRICS_DIR = BASE_DIR / ".tmp" / "metrics"


# ─── Configuration ──────────────────────────────────────
@dataclass
class Config:
    """Tunable parameters for the RAG pipeline."""

    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Retrieval
    top_k: int = 4
    confidence_threshold: float = 0.7

    # LLM
    model_name: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0.3
    max_tokens: int = 1024

    # Memory
    memory_window: int = 5

    # ChromaDB
    collection_name: str = "billeasy_docs"
    persist_directory: str = str(VECTORSTORE_DIR)

    # API Key
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    def to_dict(self) -> dict:
        """Serialize config (hiding the API key)."""
        d = asdict(self)
        d["openai_api_key"] = "***" if d["openai_api_key"] else ""
        return d


# ─── Logging Setup ──────────────────────────────────────
def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure structured logging for the application."""
    logger = logging.getLogger("rag_chatbot")
    if logger.handlers:
        return logger

    logger.setLevel(level)

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    # File handler
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(
        LOGS_DIR / "app.log", encoding="utf-8"
    )
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()


# ─── Conversation Logger ────────────────────────────────
class ConversationLogger:
    """Persists every user↔assistant exchange to a JSONL file for analysis."""

    def __init__(self, log_dir: Path = LOGS_DIR):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "conversations.jsonl"

    def log(
        self,
        user_message: str,
        assistant_response: str,
        sources: list[dict],
        confidence: float,
        response_time: float,
        docs_consulted: int,
    ) -> None:
        """Append a single interaction to the JSONL log."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "assistant_response": assistant_response,
            "sources": sources,
            "confidence": round(confidence, 4),
            "response_time_ms": round(response_time * 1000, 2),
            "docs_consulted": docs_consulted,
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        logger.info(
            "Logged interaction — confidence=%.2f, time=%.0fms, docs=%d",
            confidence,
            response_time * 1000,
            docs_consulted,
        )

    def get_history(self, last_n: int = 50) -> list[dict]:
        """Read the last N logged interactions."""
        if not self.log_file.exists():
            return []
        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [json.loads(line) for line in lines[-last_n:]]


# ─── Metrics Tracker ────────────────────────────────────
class MetricsTracker:
    """Tracks performance metrics across sessions."""

    def __init__(self, metrics_dir: Path = METRICS_DIR):
        self.metrics_dir = metrics_dir
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self._start_time: Optional[float] = None
        self.metrics_file = self.metrics_dir / "metrics.json"
        self._load()

    def _load(self) -> None:
        """Load persisted metrics."""
        if self.metrics_file.exists():
            with open(self.metrics_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "total_queries": 0,
                "avg_response_time_ms": 0,
                "avg_confidence": 0,
                "avg_docs_consulted": 0,
                "low_confidence_count": 0,
            }

    def _save(self) -> None:
        """Persist metrics to disk."""
        with open(self.metrics_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def start_timer(self) -> None:
        """Mark the start of a query."""
        self._start_time = time.perf_counter()

    def elapsed(self) -> float:
        """Seconds since start_timer was called."""
        if self._start_time is None:
            return 0.0
        return time.perf_counter() - self._start_time

    def record(
        self, response_time: float, confidence: float, docs_consulted: int
    ) -> None:
        """Record metrics for one query, updating running averages."""
        n = self.data["total_queries"]
        self.data["total_queries"] = n + 1

        # Running averages
        self.data["avg_response_time_ms"] = (
            (self.data["avg_response_time_ms"] * n + response_time * 1000)
            / (n + 1)
        )
        self.data["avg_confidence"] = (
            (self.data["avg_confidence"] * n + confidence) / (n + 1)
        )
        self.data["avg_docs_consulted"] = (
            (self.data["avg_docs_consulted"] * n + docs_consulted) / (n + 1)
        )
        if confidence < 0.7:
            self.data["low_confidence_count"] += 1

        self._save()

    def summary(self) -> dict:
        """Return a copy of current metrics."""
        return {k: round(v, 2) if isinstance(v, float) else v for k, v in self.data.items()}
