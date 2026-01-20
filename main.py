import os
from parser.extractor import PDFTextExtractor
from parser.utils import save_to_json


OUTPUT_DIR = "output"

def main():
    extractor = PDFTextExtractor()

    pdf_path = "resumes/resume-0.pdf"  # change to your file
    text = extractor.extract_text(pdf_path)
    json_output_path = os.path.join(OUTPUT_DIR, f"test.json")
    save_to_json(text, json_output_path)

    print("\n===== EXTRACTED TEXT START =====\n")
    print(text)
    print("\n===== EXTRACTED TEXT END =====\n")


if __name__ == "__main__":
    main()
