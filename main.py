# Welcome to my personal finance tracker project!
import pymupdf
import re
import pandas as pd

def extract_text_from_pdfs(pdf_paths):
    # Extract text from each PDF in the given list, return a dictionary with PDF names as keys
    pdf_texts = {}
    for pdf_path in pdf_paths:
        with pymupdf.open(pdf_path) as pdf:
            text = chr(12).join([page.get_text() for page in pdf])
            pdf_texts[pdf_path] = text
    return pdf_texts

def parse_transactions(text):
    # Extract transactions from the text
    transactions = []
    pattern = re.compile(r"(\d{2}/\d{2})\s+(\d{2}/\d{2})\s+([A-Z\s#]+.*?)\s+(\d+)\s+(\d+)\s+(\d+\.\d{2})")

    for match in pattern.finditer(text):
        date = match.group(1)
        description = match.group(3)
        amount = match.group(6)
        transactions.append({
            "Transaction Date": date,
            "Transaction Description": description,
            "Transaction Amount": float(amount)
        })

    return transactions

def save_to_excel(parsed_data, excel_path):
    # Save parsed transactions to different sheets based on PDF names
    with pd.ExcelWriter(excel_path) as writer:
        for pdf_name, transactions in parsed_data.items():
            sheet_name = pdf_name.replace(".pdf", "")  # Use the PDF file name as the sheet name
            df = pd.DataFrame(transactions)
            df.to_excel(writer, sheet_name=sheet_name)

# Main function
if __name__ == "__main__":
    pdf_paths = ["Bofa09:24.pdf", "Bofa10:24.pdf"]  # List of multiple PDF file paths
    excel_path = "Excel Output.xlsx"

    # Step 1: Extract text from PDFs
    pdf_texts = extract_text_from_pdfs(pdf_paths)

    # Step 2: Parse transaction data for each PDF and store it in a dictionary
    parsed_data = {}
    for pdf_name, text in pdf_texts.items():
        transactions = parse_transactions(text)
        parsed_data[pdf_name] = transactions

    # Step 3: Save to Excel with each PDF’s transactions in a separate sheet
    save_to_excel(parsed_data, excel_path)
