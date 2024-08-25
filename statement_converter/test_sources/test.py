import argparse
import pdfplumber
import os


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() + "\n\n--- Page Break ---\n\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    return full_text


def save_text_to_file(text, output_path):
    """
    Save extracted text to a file.

    Args:
        text (str): Text to save.
        output_path (str): Path to save the text file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted text saved to: {output_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file for analysis."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output text file path (optional)")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"Error: The file {args.pdf_path} does not exist.")
        return

    extracted_text = extract_text_from_pdf(args.pdf_path)

    if extracted_text:
        if args.output:
            save_text_to_file(extracted_text, args.output)
        else:
            print("Extracted Text:")
            print("=" * 80)
            print(extracted_text)
            print("=" * 80)


if __name__ == "__main__":
    main()
