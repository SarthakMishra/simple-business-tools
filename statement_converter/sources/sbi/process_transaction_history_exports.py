import pdfplumber
import pandas as pd
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


def parse_transactions(text):
    """
    Parse transaction details from extracted text.

    Args:
        text (str): Extracted text from the PDF.

    Returns:
        list: List of transactions, where each transaction is a list of [date, description, debit, credit].
    """
    transactions = []
    pattern = r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(Credit|Debit)\s+([\d,.]+)"
    matches = re.findall(pattern, text, re.MULTILINE)

    for match in matches:
        date, description, type_, amount = match
        amount = float(amount.replace(",", ""))
        debit = amount if type_ == "Debit" else 0
        credit = amount if type_ == "Credit" else 0
        transactions.append([date, description.strip(), debit, credit])

    return transactions


def process_transaction_history(uploaded_file):
    """
    Process the uploaded transaction history PDF file.

    Args:
        uploaded_file: A file-like object containing the PDF.

    Returns:
        pd.DataFrame or None: DataFrame containing transaction data if successful, None otherwise.
    """
    extracted_text = extract_all_text(uploaded_file)
    transactions = parse_transactions(extracted_text)

    if transactions:
        df = pd.DataFrame(
            transactions, columns=["Date", "Description", "Debit (Rs.)", "Credit (Rs.)"]
        )
        return df
    else:
        return None
