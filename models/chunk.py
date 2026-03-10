from dataclasses import dataclass
from typing import Dict, Optional
from langchain_core.documents import Document


@dataclass
class Chunk:
    # Đại diện cho một đoạn văn bản nhỏ (chunk) được tách ra từ RawDocument.
    doc_id: str
    chunk_id: str
    chunk_index: Optional[int] = None

    content: str
    source: Optional[str] = None
    title: Optional[str] = None

    metadata: Optional[Dict] = None

    def to_langchain_document(self) -> Document:
        # Chuyển đổi Chunk thành Document của LangChain

        meta = {
            "doc_id": self.doc_id,
            "chunk_id": self.chunk_id,
            "chunk_index": self.chunk_index,
            "source": self.source,
            "title": self.title,
        }

        # Nếu có metadata riêng của chunk, gộp vào meta chung
        if self.metadata:
            meta.update(self.metadata) # metadata bây giờ có thêm các trường như date, language, type (web/pdf/markdown) của doc gốc

        return Document(
            page_content=self.content,
            metadata=meta
        )