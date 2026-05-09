"""
PDF chat — extract text from PDF and answer questions via LLM.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from loki.core.brain import LokiBrain

logger = logging.getLogger(__name__)

try:
    import fitz  # PyMuPDF
    FITZ_AVAILABLE = True
except ImportError:
    FITZ_AVAILABLE = False
    logger.warning("PyMuPDF not available: pip install PyMuPDF")


class PDFChat:
    """Chat with PDF documents using LLM."""

    MAX_CHARS = 8000

    def __init__(self, brain: Optional["LokiBrain"] = None):
        self._brain = brain
        self._cache: Dict[str, str] = {}

    def ask(self, path: str, question: str) -> Dict[str, Any]:
        if not FITZ_AVAILABLE:
            return {"success": False, "message": "PyMuPDF not installed: pip install PyMuPDF"}
        if not path or not question:
            return {"success": False, "message": "Specify both a PDF path and a question."}

        pdf_path = Path(path).expanduser().resolve()
        if not pdf_path.exists():
            return {"success": False, "message": f"PDF not found: {pdf_path}"}
        if pdf_path.suffix.lower() != ".pdf":
            return {"success": False, "message": "Only PDF files are supported."}

        text = self._extract_text(str(pdf_path))
        if not text:
            return {"success": False, "message": "Could not extract text from PDF. It may be scanned/image-based."}

        if not self._brain:
            return {"success": True, "message": f"PDF loaded ({len(text)} chars). No LLM available to answer questions."}

        prompt = (
            f"The following is the content of a PDF document. "
            f"Answer this question based ONLY on the document content: '{question}'\n\n"
            f"Document content:\n{text[:self.MAX_CHARS]}"
        )

        try:
            answer = "".join(self._brain.ask(prompt))
            return {"success": True, "message": answer, "data": {"path": str(pdf_path), "pages": self._page_count}}
        except Exception as e:
            return {"success": False, "message": f"LLM query failed: {e}"}

    def _extract_text(self, path: str) -> str:
        if path in self._cache:
            return self._cache[path]
        try:
            doc = fitz.open(path)
            self._page_count = len(doc)
            pages = []
            for page in doc:
                pages.append(page.get_text())
            text = "\n".join(pages)
            self._cache[path] = text
            return text
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            self._page_count = 0
            return ""
