"""
Embeddings Manager — Vector Store with ChromaDB
=================================================
Manages document embeddings using OpenAI's text-embedding-3-small
and persists them in a ChromaDB collection.
"""

from pathlib import Path
from typing import Optional

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.utils import Config, logger, VECTORSTORE_DIR


class EmbeddingsManager:
    """
    Wraps ChromaDB + OpenAI embeddings for storing and querying
    document vectors.

    Usage:
        manager = EmbeddingsManager(config)
        manager.add_documents(chunks)
        results = manager.similarity_search("query", k=4)
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

        # Ensure persist directory exists
        persist_dir = Path(self.config.persist_directory)
        persist_dir.mkdir(parents=True, exist_ok=True)

        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model=self.config.embedding_model,
            openai_api_key=self.config.openai_api_key,
        )

        # Initialize ChromaDB
        self.vectorstore = Chroma(
            collection_name=self.config.collection_name,
            embedding_function=self.embeddings,
            persist_directory=str(persist_dir),
        )

        logger.info(
            "EmbeddingsManager initialized — model=%s, collection=%s, docs=%d",
            self.config.embedding_model,
            self.config.collection_name,
            self.document_count,
        )

    # ─── Public API ──────────────────────────────────────

    def add_documents(self, documents: list[Document]) -> int:
        """
        Embed and store a list of Document chunks.

        Args:
            documents: LangChain Document objects to embed.

        Returns:
            Number of documents added.
        """
        if not documents:
            logger.warning("No documents to add.")
            return 0

        self.vectorstore.add_documents(documents)
        count = len(documents)

        logger.info(
            "Added %d chunks to collection '%s' (total: %d)",
            count,
            self.config.collection_name,
            self.document_count,
        )
        return count

    def similarity_search(
        self, query: str, k: Optional[int] = None
    ) -> list[tuple[Document, float]]:
        """
        Perform similarity search and return documents with scores.

        Args:
            query: Search query string.
            k: Number of results (defaults to config.top_k).

        Returns:
            List of (Document, similarity_score) tuples,
            sorted by relevance (highest first).
        """
        k = k or self.config.top_k
        results = self.vectorstore.similarity_search_with_relevance_scores(
            query, k=k
        )

        logger.info(
            "Search for '%s' → %d results (top score: %.3f)",
            query[:60],
            len(results),
            results[0][1] if results else 0.0,
        )
        return results

    def clear_collection(self) -> None:
        """Delete all documents from the current collection."""
        self.vectorstore.delete_collection()

        # Re-create the empty collection
        persist_dir = Path(self.config.persist_directory)
        self.vectorstore = Chroma(
            collection_name=self.config.collection_name,
            embedding_function=self.embeddings,
            persist_directory=str(persist_dir),
        )
        logger.info("Collection '%s' cleared.", self.config.collection_name)

    @property
    def document_count(self) -> int:
        """Number of document chunks currently stored."""
        try:
            return self.vectorstore._collection.count()
        except Exception:
            return 0

    def get_collection_stats(self) -> dict:
        """Return stats about the vector store."""
        return {
            "collection_name": self.config.collection_name,
            "document_count": self.document_count,
            "embedding_model": self.config.embedding_model,
            "persist_directory": self.config.persist_directory,
        }

    def get_retriever(self, k: Optional[int] = None):
        """
        Return a LangChain retriever interface for use in chains.

        Args:
            k: Number of documents to retrieve.

        Returns:
            LangChain VectorStoreRetriever.
        """
        k = k or self.config.top_k
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )
