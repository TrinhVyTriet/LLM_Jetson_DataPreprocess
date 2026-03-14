from typing import List

from models.raw_document import RawDocument


class TextLoader:

    def __init__(self, file_path: str):
        self.file_path = file_path


    def load(self) -> List[RawDocument]:
        # Đọc file TXT và trích xuất văn bản.
        with open(self.file_path, "r", encoding="utf-8") as f:
            text = f.read()

        doc = RawDocument(
            source=self.file_path,
            title=self.file_path.split("/")[-1],
            content=text,
        )

        return [doc]