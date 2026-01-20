import pdfplumber
import os
import re


class PDFTextExtractor:
    """
    Responsible only for extracting and cleaning text from text-based PDFs.
    No printing. No CLI logic.
    """

    def extract_text(self, pdf_path: str) -> str:
        """
        Extracts and returns cleaned text from a PDF file.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")

        raw_text = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(layout=True)
                if page_text:
                    raw_text.append(page_text)

        combined_text = "\n".join(raw_text)
        return self._clean_text(combined_text)

    def _clean_text(self, text: str) -> str:
        """
        Internal text cleaning logic.
        """
        if not text:
            return ""

        # Normalize spaces and tabs
        text = re.sub(r"[ \t]+", " ", text)

        # Limit excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip each line
        lines = [line.strip() for line in text.splitlines()]
        text = "\n".join(lines)

        return text.strip()
