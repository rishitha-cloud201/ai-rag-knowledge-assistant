import hashlib
from pathlib import Path

from fastapi import UploadFile
from pypdf import PdfReader

from app.config import get_settings


class DocumentService:
    supported_extensions = {".txt", ".md", ".pdf"}

    def __init__(self) -> None:
        self.settings = get_settings()
        self.upload_directory = Path("data/uploads")
        self.upload_directory.mkdir(parents=True, exist_ok=True)

    async def save_and_extract(
        self,
        uploaded_file: UploadFile,
    ) -> tuple[str, str, str]:
        filename = uploaded_file.filename or "uploaded-document"
        extension = Path(filename).suffix.lower()

        if extension not in self.supported_extensions:
            supported = ", ".join(sorted(self.supported_extensions))
            raise ValueError(
                f"Unsupported file type '{extension}'. "
                f"Supported types: {supported}"
            )

        content = await uploaded_file.read()

        if not content:
            raise ValueError("Uploaded file is empty.")

        document_id = hashlib.sha256(content).hexdigest()[:16]
        saved_path = self.upload_directory / f"{document_id}{extension}"
        saved_path.write_bytes(content)

        extracted_text = self._extract_text(saved_path, extension)

        if not extracted_text.strip():
            raise ValueError("No readable text was found in the document.")

        return document_id, filename, extracted_text

    def create_chunks(self, text: str) -> list[str]:
        normalized_text = " ".join(text.split())

        chunk_size = self.settings.chunk_size
        overlap = self.settings.chunk_overlap

        if chunk_size <= overlap:
            raise ValueError("Chunk size must be greater than chunk overlap.")

        chunks: list[str] = []
        start = 0

        while start < len(normalized_text):
            end = min(start + chunk_size, len(normalized_text))
            chunk = normalized_text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end == len(normalized_text):
                break

            start = end - overlap

        return chunks

    @staticmethod
    def _extract_text(path: Path, extension: str) -> str:
        if extension in {".txt", ".md"}:
            return path.read_text(encoding="utf-8", errors="ignore")

        if extension == ".pdf":
            reader = PdfReader(str(path))
            return "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        raise ValueError(f"Unsupported extension: {extension}")