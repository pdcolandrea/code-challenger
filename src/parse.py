import re
from bs4 import BeautifulSoup

class ResultParser:
    def __init__(self, html_file_path: str):
        # self.root_html_content = root.prettify()
        self.GOOGLE_URL = "https://www.google.com"

        with open(html_file_path, "r", encoding="utf-8") as f:
            self.root_html_content = f.read()

    def parse(self, results: list[dict]) -> list[dict]:
        result = []
        for item in results:
            features = {}

            features['title'] = self.clean_text(item['title'])
            features['extensions'] = [item['date']]

            if not item['link'].startswith('https://'):
                features['link'] = f"{self.GOOGLE_URL}{item['link']}"
            else:
                features['link'] = item['link']

            image = item.get('thumbnail')
            if image:
                features['image'] =  self.extract_content(image)
            else:
                features['image'] = item.get('preload_thumbnail')

            result.append(features)
        return result
    
    @staticmethod
    def clean_text(text: str) -> str:
        return ' '.join(text.split())
    
    def extract_content(self, search_string: str) -> str:
        # Find the occurrence of the search string with exact format
        search_match = re.search(f'"{search_string}"', self.root_html_content)
        
        if search_match:
            # Look for the var s declaration before this match
            start_pos = self.root_html_content[:search_match.start()].rfind('var s')
            if start_pos != -1:
                # Find the first quote after var s
                quote_pos = self.root_html_content[start_pos:].find('"') + start_pos
                if quote_pos != -1:
                    # Find the closing quote
                    end_pos = self.root_html_content[quote_pos + 1:].find('"') + quote_pos + 1
                    if end_pos != -1:
                        return self.root_html_content[quote_pos + 1:end_pos]
        
        return None