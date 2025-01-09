
import json
from bs4 import BeautifulSoup

from extractors.bs4_extractor import BS4Extractor
from parse import ResultParser

def main():
    html_file_path = "files/van-gogh-paintings.html"

    extractor = BS4Extractor(html_file_path)
    results = extractor.start()

    cleaned_results = ResultParser(html_file_path).parse(results)
    print(f'Found {len(cleaned_results)} results')
    print(cleaned_results[0])


if __name__ == "__main__":
    main()
