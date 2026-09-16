import pypdf
from pathlib import Path
import re

def extract_invoice_data(text: str) -> dict:
    nfe_match = re.search(r"N[ºo°]\s*(\d+)", text)
    name_match = re.search(r"Nome\s*/\s*Razão\s*Social\s*\n+([^\n]+)", text, re.IGNORECASE)

    return {
        "invoice_number": nfe_match.group(1) if nfe_match else None,
        "recipient_name": name_match.group(1).strip() if name_match else None,
    }


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    folder = Path(pdf_path)
    extracted_records = []

    for pdf in folder.glob("*.pdf"):
        reader = pypdf.PdfReader(pdf)
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            data = extract_invoice_data(text)
            data["file_name"] = pdf.name
            data["page"] = index + 1
            extracted_records.append(data)

    return extracted_records
            
def rename_pdf(pdf_path: str, list_nfe_names: list[dict]):
    """Rename the PDF files to the format: NF-e invoice_number recipient_name.pdf"""
    folder = Path(pdf_path)
    extracted_records = []

    for pdf in folder.glob("*.pdf"):
        reader = pypdf.PdfReader(pdf)
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            data = extract_invoice_data(text)
            data["file_name"] = pdf.name
            data["page"] = index + 1
            extracted_records.append(data)

    return extracted_records

def rename_pdf(pdf_path: str, extracted_records: list[dict]) -> list[dict]:
    """Rename the PDF files to the format: NF-e invoice_number recipient_name.pdf"""
    
    for record in extracted_records:
        old_name = Path(pdf_path) / record["file_name"]
        new_name = Path(pdf_path) / f"NF-e {record['invoice_number']} {record['recipient_name']}.pdf"
        old_name.rename(new_name)

    return extracted_records

def main():
    PDF_FOLDER = str(input("Insira o caminho da pasta com os PDFs: "))
    extracted_records = extract_text_from_pdf(PDF_FOLDER)
    extracted_records = rename_pdf(PDF_FOLDER, extracted_records)
    print("Done!")


if __name__ == "__main__":
    main()
