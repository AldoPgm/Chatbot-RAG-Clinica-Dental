"""
Document Loader — Multi-format Ingestion & Chunking
=====================================================
Loads PDF, TXT, DOCX, and Markdown files, then splits them into
semantically coherent chunks for embedding.
"""

from pathlib import Path
from typing import Optional

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.utils import Config, logger

# Mapping of file extension → LangChain loader class
LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".docx": Docx2txtLoader,
    ".md": TextLoader,  # MD is plain text, no need for heavy unstructured dep
}

SUPPORTED_EXTENSIONS = set(LOADER_MAP.keys())


class DocumentLoader:
    """
    Loads documents from disk, enriches them with metadata,
    and splits them into chunks ready for embedding.

    Usage:
        loader = DocumentLoader(config)
        chunks = loader.load_file("path/to/doc.pdf")
        # or
        chunks = loader.load_directory("path/to/docs/")
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True,
        )
        logger.info(
            "DocumentLoader initialized — chunk_size=%d, overlap=%d",
            self.config.chunk_size,
            self.config.chunk_overlap,
        )

    # ─── Public API ──────────────────────────────────────

    def load_file(self, file_path: str | Path) -> list[Document]:
        """
        Load a single file, enrich metadata, and split into chunks.

        Args:
            file_path: Path to the document.

        Returns:
            List of Document chunks with metadata.

        Raises:
            ValueError: If the file extension is unsupported.
            FileNotFoundError: If the file does not exist.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = file_path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported format '{ext}'. "
                f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

        logger.info("Loading file: %s", file_path.name)

        # Load raw documents
        loader_cls = LOADER_MAP[ext]
        try:
            # TextLoader needs explicit UTF-8 on Windows (default is cp1252)
            if loader_cls == TextLoader:
                loader = loader_cls(str(file_path), encoding="utf-8")
            else:
                loader = loader_cls(str(file_path))
            raw_docs = loader.load()
        except Exception as e:
            logger.error("Failed to load %s: %s", file_path.name, e)
            raise

        # Enrich metadata
        for doc in raw_docs:
            doc.metadata.update({
                "source_file": file_path.name,
                "file_type": ext.lstrip("."),
                "file_path": str(file_path.resolve()),
            })

        # Split into chunks
        chunks = self.text_splitter.split_documents(raw_docs)

        # Add chunk indices
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)

        logger.info(
            "Loaded %s → %d raw docs → %d chunks",
            file_path.name,
            len(raw_docs),
            len(chunks),
        )
        return chunks

    def load_directory(self, dir_path: str | Path) -> list[Document]:
        """
        Load all supported files from a directory (non-recursive).

        Args:
            dir_path: Path to the directory.

        Returns:
            Combined list of Document chunks from all files.
        """
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")

        all_chunks: list[Document] = []
        files = sorted(
            f for f in dir_path.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        )

        if not files:
            logger.warning("No supported files found in %s", dir_path)
            return all_chunks

        logger.info(
            "Loading %d files from %s",
            len(files),
            dir_path.name,
        )

        for file in files:
            try:
                chunks = self.load_file(file)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error("Skipping %s: %s", file.name, e)

        logger.info(
            "Directory load complete — %d files → %d total chunks",
            len(files),
            len(all_chunks),
        )
        return all_chunks

    def load_uploaded_file(
        self, file_content: bytes, filename: str, save_dir: str | Path
    ) -> list[Document]:
        """
        Save an uploaded file to disk, then load and chunk it.
        Used by the Streamlit interface.

        Args:
            file_content: Raw bytes of the uploaded file.
            filename: Original filename.
            save_dir: Directory to save the file in.

        Returns:
            List of Document chunks.
        """
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / filename
        file_path.write_bytes(file_content)
        logger.info("Saved uploaded file: %s", filename)

        return self.load_file(file_path)

    @staticmethod
    def supported_formats() -> list[str]:
        """Return list of supported file extensions."""
        return sorted(SUPPORTED_EXTENSIONS)
