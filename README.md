![Python](https://img.shields.io/badge/python-3.10-blue)
![RAG](https://img.shields.io/badge/AI-RAG-green)
![Jetson](https://img.shields.io/badge/NVIDIA-Jetson-orange)

# 📚 RAG Data Pipeline (Data Collection & Preprocessing)
---
    This module implements the data ingestion and preprocessing pipeline for a Retrieval-Augmented Generation (RAG) system deployed on NVIDIA Jetson.

    The pipeline collects documents from multiple sources, cleans the text, splits it into chunks, and prepares the data for embedding and vector database indexing.

    This repository contains the implementation of the first two stages of the RAG pipeline.

# 🧠 RAG System Architecture
---
The full system consists of three main phases:
| Phase | Components |
|------|------|
| **OFFLINE PHASE (Build)** | Data Collection → Preprocessing → Embedding + Vector DB |
| **ONLINE PHASE (Serve)** | Retriever → Prompt + LLM → API + UI |
| **QUALITY PHASE (Evaluation)** | Evaluation → Feedback Loop |

This repository implements:
    Stage 1 → Data Collection
    Stage 2 → Preprocessing & Chunking

# 🏗 Pipeline Flow
---
The implemented pipeline works as follows:
Input Source
     │
     ▼
Loader / Crawler
(WebLoader / PDFLoader / TextLoader / MarkdownLoader)
     │
     ▼
RawDocument
     │
     ▼
Cleaner
(Text normalization & cleaning)
     │
     ▼
Chunker
(Text splitting)
     │
     ▼
Chunk Objects
     │
     ▼
LangChain Document
(Ready for embedding)

# 📂 Project Structure
---
    LLM_JETSON/
    │
    ├── loaders/
    │   ├── web_loader.py
    │   ├── pdf_loader.py
    │   ├── text_loader.py
    │   └── markdown_loader.py
    │
    ├── models/
    │   ├── raw_document.py
    │   └── chunk.py
    │
    ├── cleaner.py
    ├── chunker.py
    ├── pipeline.py
    ├── main.py
    │
    ├── raw_documents.json
    └── README.md

# 📥 Data Collection
---
    The system supports multiple data sources for building the knowledge base.

    Supported Inputs:
        Website (homepage URL)
        PDF documents
        TXT files
        Markdown files

    All input sources are converted into a unified internal structure called RawDocument.

# 📄 RawDocument Structure
---
    Each document is stored in the following format:
        {
            "doc_id": "...",
            "source": "...",
            "title": "...",
            "content": "...",
            "metadata": {
                "date": "...",
                "language": "...",
                "type": "web/pdf/text/markdown"
            }
        }

# 🌐 Web Crawler
---
    The WebLoader implements a Breadth-First Search (BFS) crawler to extract documents from a website.

    Features
        BFS crawling strategy
        Internal link filtering
        Duplicate URL detection
        HTML parsing
        Main content extraction
        Automatic attachment detection

    If the crawler encounters file links such as PDF, TXT or Markdown it will automatically delegate the loading process to the corresponding file loader.

# 📑 File Loaders
---
    PDFLoader
    TextLoader
    MarkdownLoader
    -> Extract content and output RawDocument object

# 🧹 Text Cleaning
---
    Before the chunking stage, all documents are cleaned using the Cleaner module.

    Cleaning Steps:
        1. Unicode Normalization
        2. Remove HTML Noise
        3. Whitespace Normalization

# ✂️ Chunking
---
    After cleaning, documents are split into smaller segments using the Chunker.

    Example Configuration:
        chunk_size = 500
        chunk_overlap = 50

    Chunk Structure:
        Chunk (
            doc_id
            chunk_id
            chunk_index
            content
            metadata
        )

    Each chunk is then converted into a LangChain Document object.

# 🚀 Running the Pipeline
---
    The entire pipeline can be executed with:
        python main.py

    Example Usage:
        from pipeline import Pipeline
        from cleaner import Cleaner
        from chunker import Chunker

        pipeline = Pipeline()

        documents = pipeline.run(
            input_path_or_url="https://example.com",
            cleaner=Cleaner(),
            chunker=Chunker()
        )

        print(len(documents))

# 📤 Output
---
    The pipeline produces two types of outputs:

    1. Cleaned Crawl Data (Saved as cleaned_documents.json):
        {
            "doc_id": "...",
            "source": "...",
            "title": "...",
            "content": "...",
            "metadata": {...}
        }

    2. Chunk Documents
        A list of LangChain Documents, ready for:
            Embedding
            Vector Database indexing
            Information Retrieval