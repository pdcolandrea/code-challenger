import json

from extractors.bs4_extractor import BS4Extractor
from parse import ResultParser


def main(
    html_file_path="files/picasso-paintings.html",
    output_path="files/output/picasso-paintings-results.json",
):
    extractor = BS4Extractor(html_file_path)
    results = extractor.start()

    cleaned_results = ResultParser(html_file_path).parse(results)
    print(f"Found {len(cleaned_results)} results")

    # Save results to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_results, f, indent=2, ensure_ascii=False)

    print(f"Results saved to {output_path}")
    return cleaned_results


if __name__ == "__main__":
    # TODO: Add support for command line arguments
    main()
