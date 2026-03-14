import json
from typing import List
from langchain_core.documents import Document

from loaders.web_loader import WebLoader
from loaders.pdf_loader import PDFLoader
from loaders.text_loader import TextLoader
from loaders.markdown_loader import MarkdownLoader

class Pipeline:
    def get_loader(self, source: str):
        # Chọn loader phù hợp dựa trên loại nguồn dữ liệu.
        if source.startswith("http"):
            if source.endswith(".pdf"):
                return PDFLoader(source)
            if source.endswith(".txt"):
                return TextLoader(source)
            if source.endswith(".md"):
                return MarkdownLoader(source)
            # default web page
            return WebLoader(source)  
        else:
            if source.endswith(".pdf"):
                return PDFLoader(source)
            if source.endswith(".txt"):
                return TextLoader(source)
            if source.endswith(".md"):
                return MarkdownLoader(source)

        raise ValueError(f"Unsupported source: {source}")
    
    def save_cleaned_docs(self, clean_docs, path="cleaned_documents.json"):
        data = [doc.to_json_serializable() for doc in clean_docs]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def run(self, input_path_or_url, cleaner, chunker, save_cleaned=True) -> List[Document]:
        # Chạy toàn bộ pipeline cho 1 source đầu vào
        # Load
        loader = self.get_loader(input_path_or_url)
        raw_docs = loader.load() # List[RawDocument] vì 1 source có thể tạo ra nhiều doc (ví dụ web loader có thể crawl nhiều trang)

        # Clean
        clean_docs = cleaner.clean(raw_docs)

        # Save cleaned data
        if save_cleaned:
            self.save_cleaned_docs(clean_docs)

        # Chunk
        all_chunks = []

        for doc in clean_docs:
            chunks = chunker.chunk_document(doc)
            all_chunks.extend(chunks)

        # Convert to LangChain Document
        documents = [chunk.to_langchain_document() for chunk in all_chunks]

        return documents