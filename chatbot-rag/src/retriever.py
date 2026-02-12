"""
RAG Retriever — Semantic Search with Relevance Scoring
========================================================
Wraps the EmbeddingsManager to provide structured retrieval
results with confidence evaluation and source metadata.
"""

from dataclasses import dataclass
from typing import Optional

from langchain_core.documents import Document

from src.embeddings_manager import EmbeddingsManager
from src.utils import Config, logger


@dataclass
class RetrievalResult:
    """A single retrieval result with metadata."""

    content: str
    source_file: str
    chunk_index: int
    total_chunks: int
    similarity_score: float
    is_relevant: bool  # True if score >= confidence_threshold

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "source_file": self.source_file,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "similarity_score": round(self.similarity_score, 4),
            "is_relevant": self.is_relevant,
        }


@dataclass
class RetrievalResponse:
    """Full retrieval response with aggregated metadata."""

    results: list[RetrievalResult]
    query: str
    avg_confidence: float
    has_relevant_results: bool
    docs_consulted: int

    def get_context_text(self) -> str:
        """Format results into a context string for the LLM."""
        if not self.results:
            return "No se encontraron documentos relevantes."

        context_parts = []
        for i, r in enumerate(self.results, 1):
            context_parts.append(
                f"[Fuente {i}: {r.source_file} — Fragmento {r.chunk_index + 1}/{r.total_chunks}]\n"
                f"{r.content}"
            )
        return "\n\n---\n\n".join(context_parts)

    def get_sources_summary(self) -> list[dict]:
        """Return a concise list of source citations."""
        return [
            {
                "source": r.source_file,
                "chunk": f"{r.chunk_index + 1}/{r.total_chunks}",
                "relevance": round(r.similarity_score, 2),
            }
            for r in self.results
            if r.is_relevant
        ]


class RAGRetriever:
    """
    Orchestrates semantic search over the vector store with
    relevance evaluation and structured output.

    Usage:
        retriever = RAGRetriever(embeddings_manager, config)
        response = retriever.retrieve("¿Cómo instalo BillEasy?")

        if response.has_relevant_results:
            context = response.get_context_text()
            sources = response.get_sources_summary()
    """

    def __init__(
        self,
        embeddings_manager: EmbeddingsManager,
        config: Optional[Config] = None,
    ):
        self.em = embeddings_manager
        self.config = config or Config()

    def retrieve(
        self, query: str, top_k: Optional[int] = None
    ) -> RetrievalResponse:
        """
        Search the vector store and return structured results.

        Args:
            query: The user's question.
            top_k: Number of results to return (defaults to config).

        Returns:
            RetrievalResponse with results, confidence info, and context.
        """
        k = top_k or self.config.top_k

        # Perform similarity search
        raw_results = self.em.similarity_search(query, k=k)

        if not raw_results:
            logger.info("No results found for query: '%s'", query[:60])
            return RetrievalResponse(
                results=[],
                query=query,
                avg_confidence=0.0,
                has_relevant_results=False,
                docs_consulted=0,
            )

        # Build structured results
        results: list[RetrievalResult] = []
        for doc, score in raw_results:
            results.append(
                RetrievalResult(
                    content=doc.page_content,
                    source_file=doc.metadata.get("source_file", "unknown"),
                    chunk_index=doc.metadata.get("chunk_index", 0),
                    total_chunks=doc.metadata.get("total_chunks", 1),
                    similarity_score=score,
                    is_relevant=score >= self.config.confidence_threshold,
                )
            )

        # Aggregate metrics
        scores = [r.similarity_score for r in results]
        avg_confidence = sum(scores) / len(scores) if scores else 0.0
        has_relevant = any(r.is_relevant for r in results)

        logger.info(
            "Retrieved %d results — avg_confidence=%.3f, relevant=%s",
            len(results),
            avg_confidence,
            has_relevant,
        )

        return RetrievalResponse(
            results=results,
            query=query,
            avg_confidence=avg_confidence,
            has_relevant_results=has_relevant,
            docs_consulted=len(results),
        )
