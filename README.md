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