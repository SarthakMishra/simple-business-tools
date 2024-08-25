# SBI Card Statement Converter

This tool converts credit card statements from PDF to CSV format. It currently supports SBI Credit Card statements, extracting transaction details and providing a downloadable CSV file along with basic transaction statistics.

## Features

- Support for multiple banks (currently SBI, with easy extensibility for other banks)
- For SBI, two modes of operation:
  1. Transaction History Export: Convert exported transaction history PDFs
  2. Monthly Statements: Process one or more monthly statement PDFs
- Extract transactions from credit card statement PDFs
- Sort transactions by date
- Generate downloadable CSV files with a date range in the filename
- Display transaction summary and statistics
- User-friendly interface built with Streamlit

## Live App

You can use the live version of this tool at: [SBT Statement Converter](https://sbt-statement-converter.streamlit.app/)

## Usage

Run the Streamlit app:

```bash
streamlit run statement_converter.py
```

Then follow these steps:

1. Select your bank from the dropdown menu (currently only SBI is available).
2. Choose between "Transaction History Export" or "Monthly Statements" tabs.
3. Upload your PDF file(s) as instructed.
4. The app will process the PDF(s) and display a summary of extracted transactions.
5. You can download the CSV file using the "Download Statement as CSV" button.
6. View transaction statistics at the bottom of the page.

## Project Structure

- `statement_converter.py`: Main Streamlit app
- `sources/`: Directory containing bank-specific modules
  - `sbi/`: SBI-specific modules
    - `sbi_tabs.py`: Defines the UI and logic for SBI statement processing
    - `process_transaction_history_exports.py`: Processes transaction history exports
    - `process_monthly_statements.py`: Processes monthly statements
    - `utils.py`: Utility functions for SBI statement processing
