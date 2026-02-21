"""
Multimodal ingestor with Google Gemini.

Extracts text from scanned PDFs using Google's Gemini model
for OCR via computer vision (multimodal).
"""

import io
import base64
from typing import List, Optional

import fitz
from PIL import Image
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from rag.multimodal_model import ocr_client
from rag.prompts import PROMPT_IMAGES_TO_TEXT
from rag.services.save_md_doc import save_md_doc

from utils.config import settings


class GoogleVisionIngestor():
    """Ingestor that uses Google Gemini for multimodal OCR.

    Renders each PDF page as an image and uses the Google
    Gemini 2.5 Flash model to transcribe the text via computer
    vision using the `ocr_client` singleton.
    """

    def ingest(self, file_path: str) -> str:
        """Extracts text from a PDF using multimodal OCR with Gemini.

        Each page is rendered as a 300 DPI PNG image and sent
        to the Gemini model for text transcription using LangChain's HumanMessage.

        Args:
            file_path: Path to the PDF file to process.

        Returns:
            str: The text transcribed by Gemini.

        Raises:
            RuntimeError: If communication with the Google API fails.
        """
        text: str = ""

        try:
            doc = fitz.open(file_path)
        except Exception as e:
            raise RuntimeError(f"Error opening PDF '{file_path}': {e}") from e

        try:
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)
                img_bytes: bytes = pix.tobytes("png")
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")

                message = HumanMessage(
                    content=[
                        {"type": "text", "text": PROMPT_IMAGES_TO_TEXT},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                    ]
                )

                try:
                    response = ocr_client.invoke([message])
                    text += str(response.content) + "\n\n"
                except Exception as e:
                    raise RuntimeError(
                        f"OCR error with Google Vision on page {page_num + 1}: {e}"
                    ) from e
        finally:
            doc.close()

        return text
