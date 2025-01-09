from bs4 import BeautifulSoup

from extractors.element_selector import ElementSelector

class BS4Extractor:
    def __init__(self, html_file_path: str):
        if not isinstance(html_file_path, str) or not html_file_path.endswith('.html'):
            raise ValueError("HTML file path must be a string ending in .html")
        
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.url = html_file_path
        
    def extract_root(self, source: BeautifulSoup):
        return source.select(ElementSelector.CAROUSEL_ROOT)

    def start(self):
        pass