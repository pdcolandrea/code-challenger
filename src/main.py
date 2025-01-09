import json
import argparse
import os
from typing import Optional
from extractors.bs4_extractor import BS4Extractor
from parse import ResultParser


def main(
    html_file_path: str,
    output_path: Optional[str] = None,
):
    if output_path is None:
        # Construct output path from input filename
        base_name = os.path.basename(html_file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_path = f"files/output/{name_without_ext}-results.json"

    extractor = BS4Extractor(html_file_path)
    results = extractor.start()

    cleaned_results = ResultParser(html_file_path).parse(results)
    print(f"Found {len(cleaned_results)} results")

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save results to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_results, f, indent=2, ensure_ascii=False)

    print(f"Results saved to {output_path}")
    return cleaned_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract painting information from HTML files")
    parser.add_argument("--input", 
                       default="files/picasso-paintings.html",
                       help="Path to the HTML file to process (default: files/picasso-paintings.html)")
    
    args = parser.parse_args()
    
    main(html_file_path=args.input)
