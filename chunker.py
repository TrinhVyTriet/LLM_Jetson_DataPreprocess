from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.raw_document import RawDocument
from models.chunk import Chunk

class Chunker:
    # Chia RawDocument thành các Chunk nhỏ để phục vụ embedding và retrieval.
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk_document(self, doc: RawDocument) -> List[Chunk]:
        # Chia một RawDocument thành nhiều Chunk.
        text_chunks = self.splitter.split_text(doc.content)

        chunks: List[Chunk] = []

        for idx, text in enumerate(text_chunks):
            # Tạo chunk_id bằng cách kết hợp doc_id và chunk_index
            chunk = Chunk(
                doc_id=doc.doc_id,
                chunk_id=f"{doc.doc_id}_chunk_{idx}",
                chunk_index=idx,

                content=text,
                source=doc.source,
                title=doc.title,

                metadata=doc.metadata.copy() #metadate của chunk lúc này gồm date, language, type của doc
            )

            chunks.append(chunk)

        return chunks