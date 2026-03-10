import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from typing import List, Set
import uuid

from models.raw_document import RawDocument
# from loaders.pdf_loader import PDFLoader
# from loaders.text_loader import TextLoader
# from loaders.markdown_loader import MarkdownLoader

class WebLoader:
    def __init__(self, homepage_url: str, max_pages = 50):
        self.homepage_url = homepage_url
        self.max_pages = max_pages
        self.base_domain = urlparse(homepage_url).netloc
    
    def _is_internal_link(self, url: str) -> bool:
        # Kiểm tra xem URL có phải là link nội bộ (cùng domain) hay không
        domain = urlparse(url).netloc
        return domain == self.base_domain

    def _is_attachment(self, url: str) -> bool:
        # Xác định xem URL có phải là link tải về file đính kèm (pdf, txt, md) hay không
        url = url.lower()
        if url.endswith(".pdf"):
            return True
        if url.endswith(".txt"):
            return True
        if url.endswith(".md"):
            return True
        return False
    
    def _fetch_page(self, url: str) -> str:
        # Fetch nội dung HTML của trang web. Trả về None nếu có lỗi.
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            response.encoding = response.apparent_encoding

            return response.text

        except Exception as e:
            print(f"Fetch error {url}: {e}")
            return None
        
    def _extract_title(self, soup: BeautifulSoup) -> str:
        # Lấy title của trang web. Nếu không có title, trả về chuỗi rỗng.
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        return ""
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        # Lấy nội dung chính của trang web.
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        return text.strip()

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        # Lấy tất cả các link từ trang web, chuyển thành URL tuyệt đối, và chỉ giữ lại link nội bộ.
        links = []

        for a in soup.find_all("a", href=True):
            href = a["href"]                                                    # Lấy giá trị href từ thẻ a
            url = urljoin(base_url, href)                                       # Chuyển href thành URL tuyệt đối dựa trên base_url
            parsed = urlparse(url)                                              # Phân tích URL để lấy các thành phần như scheme, netloc, path
            clean_url = parsed.scheme + "://" + parsed.netloc + parsed.path
            links.append(clean_url)
        return links
    
    def _load_attachment(self, url: str) -> List[RawDocument]:
        # Load file đính kèm (pdf, txt, md) và trả về một RawDocument. Nếu có lỗi, trả về None.
        try:
            if url.endswith(".pdf"):
                loader = PDFLoader(url)
            elif url.endswith(".txt"):
                loader = TextLoader(url)
            elif url.endswith(".md"):
                loader = MarkdownLoader(url)
            else:
                return []
            return loader.load()
        
        except Exception as e:
            print(f"Attachment load error {url}: {e}")
            return []

    def load(self) -> List[RawDocument]:
        visited: Set[str] = set()
        queue = deque([self.homepage_url])
        documents: List[RawDocument] = []

        # BFS để crawl các trang nội bộ
        while queue and len(visited) < self.max_pages:
            url = queue.popleft()

            if url in visited:
                continue

            try:
                # Lấy nội dung HTML của trang web
                html = self._fetch_page(url)
                if html is None:
                    continue

                # Mark URL đã được truy cập
                visited.add(url)

                # Nếu là link tải về file đính kèm, load file đó và thêm vào documents
                if (self._is_attachment(url)):
                    docs = self._load_attachment(url)
                    documents.extend(docs)
                    continue

                soup = BeautifulSoup(html, "html.parser")
                title = self._extract_title(soup)
                content = self._extract_main_content(soup)

                # Một doc tương ứng 1 trang web
                if content.strip():
                    doc = RawDocument(
                        source=url,
                        title=title,
                        content=content,
                    )
                    documents.append(doc)

                # Tìm các link nội bộ mới để tiếp tục crawl
                links = self._extract_links(soup, url)
                for link in links:
                    if self._is_internal_link(link) and link not in visited:
                        queue.append(link)
                    
            except Exception as e:
                print(f"Error crawling {url}: {e}")

        return documents
    