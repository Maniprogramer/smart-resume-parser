import os

from parser.extractor import PDFTextExtractor
from parser.fields import extract_basic_fields
from parser.utils import save_to_json


RESUMES_DIR = "resumes"
OUTPUT_DIR = "output"

def main():
    extractor = PDFTextExtractor()

    for file_name in os.listdir(RESUMES_DIR):
        if not file_name.lower().endswith(".pdf"):
            continue

        resume_path = os.path.join(RESUMES_DIR, file_name)
        base_name = os.path.splitext(file_name)[0]

        json_output_path = os.path.join(OUTPUT_DIR, f"{base_name}.json")

        # ✅ Skip if already processed
        if os.path.exists(json_output_path):
            print(f"[SKIP] Already processed: {file_name}")
            continue

        print(f"[PROCESS] Extracting: {file_name}")

        try:
            text = extractor.extract_text(resume_path)

            if not text:
                print(f"[WARNING] No text extracted from {file_name}")
                continue

            parsed_fields = extract_basic_fields(text)
            data = [parsed_fields]

            save_to_json(data, json_output_path)

            print(f"[DONE] Saved JSON for {file_name}")

        except Exception as e:
            print(f"[ERROR] Failed processing {file_name}: {e}")


if __name__ == "__main__":
    main()
