import pdfplumber
import pandas as pd
from datetime import datetime
import re


def extract_all_text(pdf_file):
    """
    Extract all text from a PDF file.

    Args:
        pdf_file: A file-like object containing the PDF.

    Returns:
        str: Extracted text from all pages of the PDF.
    """
    full_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text


def parse_monthly_statement(text):
    """
    Parse transaction details from extracted text of a monthly statement.

    Args:
        text (str): Extracted text from the PDF.

    Returns:
        list: List of transactions, where each transaction is a list of [date, description, debit, credit].
    """
    transactions = []
    lines = text.split("\n")

    single_line_pattern = r"^(\d{2}\s+[A-Za-z]{3}\s+\d{2})\s+(.+?)\s+([\d,.]+)\s+(C|D)$"
    multi_line_pattern = r"^(\d{2}\s+[A-Za-z]{3}\s+\d{2})\s+([\d,.]+)\s+(C|D)$"

    i = 0
    while i < len(lines):
        match = re.match(single_line_pattern, lines[i])
        multi_line_match = re.match(multi_line_pattern, lines[i])

        if match:
            date_str, description, amount_str, type_ = match.groups()
            date = datetime.strptime(date_str, "%d %b %y").strftime("%d/%m/%Y")
            amount = float(amount_str.replace(",", ""))
            debit = amount if type_ == "D" else 0
            credit = amount if type_ == "C" else 0

            transactions.append([date, description.strip(), debit, credit])

        elif multi_line_match:
            date_str, amount_str, type_ = multi_line_match.groups()
            date = datetime.strptime(date_str, "%d %b %y").strftime("%d/%m/%Y")
            amount = float(amount_str.replace(",", ""))
            debit = amount if type_ == "D" else 0
            credit = amount if type_ == "C" else 0

            # Get the previous line for the first part of the description
            description_part1 = lines[i - 1].strip() if i > 0 else ""

            # Get the next line for the second part of the description
            description_part2 = lines[i + 1].strip() if i + 1 < len(lines) else ""

            # Combine the description parts
            description = f"{description_part1} {description_part2}".strip()

            transactions.append([date, description, debit, credit])
            i += 1  # Skip the next line as we've incorporated it

        i += 1

    return transactions


def process_monthly_statements(uploaded_files):
    """
    Process multiple uploaded monthly statement PDF files.

    Args:
        uploaded_files (list): List of file-like objects containing the PDFs.

    Returns:
        pd.DataFrame: DataFrame containing transaction data from all processed PDFs.
    """
    all_transactions = []
    for uploaded_file in uploaded_files:
        extracted_text = extract_all_text(uploaded_file)
        transactions = parse_monthly_statement(extracted_text)
        all_transactions.extend(transactions)

    df = pd.DataFrame(
        all_transactions, columns=["Date", "Description", "Debit (Rs.)", "Credit (Rs.)"]
    )
    return df
