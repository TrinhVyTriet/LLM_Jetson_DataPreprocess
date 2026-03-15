📚 RAG Data Pipeline (Data Collection & Preprocessing)

This module implements the data ingestion and preprocessing pipeline for a Retrieval-Augmented Generation (RAG) system deployed on NVIDIA Jetson.

The pipeline collects documents from multiple sources, cleans the text, splits it into chunks, and prepares the data for embedding and vector database indexing.

This repository contains the implementation of the first two stages of the RAG pipeline.

🧠 RAG System Architecture

The full system consists of three main phases:

OFFLINE PHASE (Build)
    1. Data Collection
    2. Preprocessing & Chunking
    3. Embedding + Vector DB

ONLINE PHASE (Serve)
    4. Retriever
    5. Prompt + LLM
    6. API + UI

QUALITY PHASE (Evaluation)
    7. Evaluation
    8. Feedback Loop

This repository implements:

Stage 1 → Data Collection
Stage 2 → Preprocessing & Chunking
🏗 Pipeline Flow

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
📂 Project Structure
project/
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
📥 Data Collection

The system supports multiple data sources.

Supported Inputs
Website (homepage URL)
PDF documents
TXT files
Markdown files

All sources are converted into a unified structure called:

RawDocument
📄 RawDocument Structure

Each document contains:

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
🌐 Web Crawler

The WebLoader implements a BFS crawler that extracts documents from a website.

Features

BFS crawling

Internal link filtering

Duplicate detection

HTML parsing

Main content extraction

Automatic attachment detection

Workflow
Homepage URL
     │
     ▼
Fetch HTML
     │
     ▼
Parse HTML (BeautifulSoup)
     │
     ▼
Extract Title + Content
     │
     ▼
Extract Internal Links
     │
     ▼
Add to BFS Queue

If the crawler encounters:

PDF
TXT
MD

it automatically delegates loading to the corresponding loader.

📑 File Loaders
PDFLoader

Extracts text from PDF files.

Workflow:

PDF
 → read pages
 → extract text
 → RawDocument
TextLoader

Loads .txt files.

read file
 → RawDocument
MarkdownLoader

Loads .md files.

read markdown
 → RawDocument
🧹 Text Cleaning

Before chunking, documents are cleaned using the Cleaner module.

Cleaning Steps
Unicode normalization
unicodedata.normalize("NFKC", text)
Remove HTML noise

Removes:

<script>
<style>
HTML tags
Normalize whitespace
multiple spaces → single space
✂️ Chunking

After cleaning, documents are split into smaller pieces using the Chunker.

Configuration

Example:

chunk_size = 500
chunk_overlap = 50
Chunk Structure
Chunk(
    doc_id
    chunk_id
    chunk_index
    content
    metadata
)

Chunks are converted into:

LangChain Document

which will later be used for embedding and retrieval.

🚀 Running the Pipeline

Run the pipeline using:

python main.py

Example usage:

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
📤 Output

The pipeline produces two outputs.

Raw crawl data
raw_documents.json

Example:

{
  "doc_id": "...",
  "source": "...",
  "title": "...",
  "content": "...",
  "metadata": {...}
}
Chunk documents

A list of LangChain Documents ready for:

Embedding
Vector Database
Retrieval
🧑‍💻 Responsibilities (SV1 – Data Engineer)

This module was implemented as part of a team project with the following role.

SV1 – Data Engineer + Jetson Setup

Responsibilities:

Data Collection

Implemented website crawler

Implemented loaders for:

Web

PDF

TXT

Markdown

Metadata extraction

Unified document format

Preprocessing

Unicode normalization

Text cleaning

Noise removal

Chunking

Document chunking

Chunk metadata management

LangChain document conversion

Pipeline

Implemented end-to-end pipeline:

Load → Clean → Chunk