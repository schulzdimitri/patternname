import re
from pathlib import Path
import pypdf


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def extract_invoice_data(text: str) -> dict:
    nfe_match = re.search(r"N[ºo°]\s*(\d+)", text)
    name_match = re.search(r"Nome\s*/\s*Razão\s*Social\s*\n+([^\n]+)", text, re.IGNORECASE)

    return {
        "invoice_number": nfe_match.group(1) if nfe_match else None,
        "recipient_name": name_match.group(1).strip() if name_match else None,
    }


def clean_folder_path(raw_path: str) -> Path:
    cleaned = raw_path.strip().strip("'\"")
    path = Path(cleaned)
    if not path.is_dir():
        raise FileNotFoundError(f"Directory not found: '{cleaned}'")
    return path


def extract_text_from_pdf(folder_path: Path) -> list[dict]:
    extracted_records = []
    pdf_files = list(folder_path.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return extracted_records

    for pdf in pdf_files:
        try:
            reader = pypdf.PdfReader(pdf)
            invoice_data = None

            for index, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                data = extract_invoice_data(text)

                if data["invoice_number"] and data["recipient_name"]:
                    invoice_data = data
                    invoice_data["file_name"] = pdf.name
                    invoice_data["page"] = index + 1
                    break

            if invoice_data:
                extracted_records.append(invoice_data)
            else:
                print(f"Warning: Could not extract invoice details from '{pdf.name}'.")

        except pypdf.errors.PdfReadError:
            print(f"Error: Corrupted or unreadable PDF file '{pdf.name}'.")
        except Exception as error:
            print(f"Error reading '{pdf.name}': {error}")

    return extracted_records


def rename_pdf(folder_path: Path, extracted_records: list[dict]) -> list[dict]:
    renamed_files = []

    for record in extracted_records:
        invoice_number = record.get("invoice_number")
        recipient_name = record.get("recipient_name")
        file_name = record.get("file_name")

        if not invoice_number or not recipient_name:
            print(f"Skipping '{file_name}': Missing invoice number or recipient name.")
            continue

        sanitized_recipient = sanitize_filename(recipient_name)
        new_filename = f"NF-e {invoice_number} {sanitized_recipient}.pdf"

        old_file = folder_path / file_name
        new_file = folder_path / new_filename

        if not old_file.exists():
            print(f"Error: Source file '{file_name}' does not exist.")
            continue

        if old_file == new_file:
            print(f"File '{file_name}' is already properly named.")
            continue

        if new_file.exists():
            print(f"Warning: Target file '{new_filename}' already exists. Skipping to avoid overwrite.")
            continue

        try:
            old_file.rename(new_file)
            renamed_files.append({
                "old_name": file_name,
                "new_name": new_filename,
                "invoice_number": invoice_number,
                "recipient_name": sanitized_recipient,
            })
        except OSError as error:
            print(f"Error renaming '{file_name}' to '{new_filename}': {error}")

    return renamed_files


def main():
    user_input = input("Enter the path to the folder containing PDFs: ")
    try:
        folder_path = clean_folder_path(user_input)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return

    records = extract_text_from_pdf(folder_path)
    if not records:
        print("No valid invoice records were found to rename.")
        return

    renamed = rename_pdf(folder_path, records)
    for item in renamed:
        print(f"{item['old_name']} -> {item['new_name']}")

    print(f"Done! {len(renamed)} file(s) renamed.")


if __name__ == "__main__":
    main()
