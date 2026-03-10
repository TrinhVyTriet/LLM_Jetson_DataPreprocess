import re
import unicodedata
from typing import List
from models.raw_document import RawDocument

class DocumentCleaner:

    def clean(self, documents: List[RawDocument]) -> List[RawDocument]:

        cleaned_docs = []

        for doc in documents:

            text = doc.content
            doc_type = doc.metadata["type"] if doc.metadata and "type" in doc.metadata else "unknown"

            text = self.normalize_unicode(text)

            if doc_type == "web":
                text = self.clean_web(text)

            elif doc_type == "pdf":
                text = self.clean_pdf(text)

            elif doc_type == "markdown":
                text = self.clean_markdown(text)

            elif doc_type == "text":
                text = self.clean_txt(text)

            text = self.normalize_whitespace(text)

            doc.content = text.strip()
            cleaned_docs.append(doc)

        return cleaned_docs


    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFC", text)

    def normalize_whitespace(self, text: str) -> str:

        text = re.sub(r"\n+", "\n", text)   # Thay thế nhiều xuống dòng liên tiếp bằng một xuống dòng duy nhất
        text = re.sub(r"[ \t]+", " ", text) # Thay thế nhiều khoảng trắng hoặc tab liên tiếp bằng một khoảng trắng duy nhất

        return text

    # =====================
    # WEB CLEAN
    # =====================

    def clean_web(self, text: str) -> str:

        text = self.remove_html(text)
        text = self.remove_urls(text)
        text = self.remove_boilerplate(text)

        return text

    def remove_html(self, text: str) -> str:
        return re.sub(r"<.*?>", "", text)

    def remove_urls(self, text: str) -> str:
        return re.sub(r"https?://\S+", "", text)

    def remove_boilerplate(self, text: str) -> str:
        # Loại bỏ các đoạn văn bản thường xuất hiện trên nhiều trang như "Trang chủ", "Liên hệ", "Chính sách", v.v.
        boilerplate_patterns = [
            r"Trang chủ",
            r"Liên hệ",
            r"Chính sách",
            r"Cookie",
            r"Facebook",
            r"Instagram"
        ]

        lines = text.split("\n")

        filtered = []

        for line in lines:
            if not any(re.search(p, line, re.IGNORECASE) for p in boilerplate_patterns):
                filtered.append(line)

        return "\n".join(filtered)

    # =====================
    # PDF CLEAN
    # =====================

    def clean_pdf(self, text: str) -> str:
        # remove page numbers
        text = re.sub(r"\n\d+\n", "\n", text)

        # remove repeated headers
        text = re.sub(r"Page \d+", "", text)

        return text

    # =====================
    # MARKDOWN CLEAN
    # =====================

    def clean_markdown(self, text: str) -> str:
        # remove markdown links
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

        # remove code blocks
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

        return text

    # =====================
    # TXT CLEAN
    # =====================

    def clean_txt(self, text: str) -> str:
        return text