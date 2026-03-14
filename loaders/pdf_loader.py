from typing import List
from pypdf import PdfReader
from models.raw_document import RawDocument

class PDFLoader:

    def __init__(self, file_path: str):
        self.file_path = file_path


    def load(self) -> List[RawDocument]:
        # Đọc file PDF và trích xuất văn bản từ tất cả các trang.
        reader = PdfReader(self.file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        doc = RawDocument(
            source=self.file_path,
            title=self.file_path.split("/")[-1],
            content=text,
        )

        return [doc]