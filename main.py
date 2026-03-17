from pipeline import Pipeline
from cleaner import DocumentCleaner
from chunker import Chunker

def main():
    # Nguồn dữ liệu đầu vào
    input_source = "https://toanmath.com/chuyen-de-toan-12"

    # Khởi tạo các component
    cleaner = DocumentCleaner()
    chunker = Chunker(
        chunk_size=500,
        chunk_overlap=100
    )

    # Khởi tạo pipeline
    pipeline = Pipeline()

    # Chạy pipeline
    documents = pipeline.run(
        input_path_or_url=input_source,
        cleaner=cleaner,
        chunker=chunker,
        save_cleaned=True
    )

    # In kết quả
    print(f"\nTotal LangChain Documents: {len(documents)}\n")

    # Xem thử 3 document đầu
    for doc in documents[:3]:
        print("-----")
        print("Content preview:")
        print(doc.page_content[:200])
        print("Metadata:")
        print(doc.metadata)

if __name__ == "__main__":
    main()