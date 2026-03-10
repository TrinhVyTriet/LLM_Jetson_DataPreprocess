from dataclasses import dataclass, asdict, field
from typing import Optional, Dict
import hashlib
import datetime


@dataclass
class RawDocument:
    """
    Đại diện cho một tài liệu gốc sau khi load từ:
    - Web
    - PDF
    - TXT
    - Markdown
    """
    
    doc_id: Optional[str] = None    # ID duy nhất của tài liệu, có thể tự sinh nếu không cung cấp
    source: str                     # URL hoặc file path
    content: str                    # Nội dung full text
    title: Optional[str] = None

    # metadata sẽ chứa thông tin mở rộng
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self):
        # Nếu doc_id chưa được cung cấp, tự sinh dựa trên source
        if self.doc_id is None:
            self.doc_id = self.generate_id()
        # Đảm bảo metadata được thiết lập đầy đủ
        self.set_metadata()

    def set_metadata(self):
        if self.metadata is None:
            self.metadata = {}

        self.metadata.setdefault(
            "date",
            datetime.datetime.now().strftime("%Y-%m-%d")
        )

        self.metadata.setdefault("language", "vi")

        if "type" not in self.metadata:
            self.metadata["type"] = self.detect_type()

    def generate_id(self) -> str:
        # Sinh doc_id bằng cách hash source.
        return hashlib.md5(self.source.encode("utf-8")).hexdigest()

    def detect_type(self) -> str:
        # Xác định loại tài liệu từ source.
        s = self.source.lower()

        if s.startswith("http"):
            return "web"
        if s.endswith(".pdf"):
            return "pdf"
        if s.endswith(".md"):
            return "markdown"
        if s.endswith(".txt"):
            return "text"
        return "unknown"

    def to_dict(self) -> dict:
        # Convert object thành dict để lưu JSON.
        return asdict(self)

    def to_json_serializable(self) -> dict:
        # Convert object thành dict JSON-safe.
        return {
            "doc_id": self.doc_id,
            "source": self.source,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata
        }