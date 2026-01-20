from parser.extractor import PDFTextExtractor

def main():
    extractor = PDFTextExtractor()

    pdf_path = "resumes/resume-0.pdf"  # change to your file
    text = extractor.extract_text(pdf_path)

    print("\n===== EXTRACTED TEXT START =====\n")
    print(text)
    print("\n===== EXTRACTED TEXT END =====\n")


if __name__ == "__main__":
    main()
