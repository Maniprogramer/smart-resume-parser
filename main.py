import os

from parser.extractor import PDFTextExtractor
from parser.fields import extract_basic_fields
from parser.utils import save_to_json


OUTPUT_DIR = "output"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    extractor = PDFTextExtractor()

    pdf_path = "resumes/resume-0.pdf"  # change if needed

    # 1️⃣ Extract raw text from PDF
    text = extractor.extract_text(pdf_path)

    # 2️⃣ Extract structured fields from text
    parsed_fields = extract_basic_fields(text)

    # 3️⃣ Save structured data to JSON
    json_output_path = os.path.join(OUTPUT_DIR, "resume-0.json")
    save_to_json([parsed_fields], json_output_path)

    # Optional: print for verification
    print("\n===== EXTRACTED TEXT START =====\n")
    print(text)
    print("\n===== EXTRACTED TEXT END =====\n")

    print("\n===== PARSED FIELDS =====\n")
    print(parsed_fields)


if __name__ == "__main__":
    main()
