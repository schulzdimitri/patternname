
<h1 align="center">🔥 PatternName - An Automated NF-e PDF Renamer</h1>

<p align="center">
  <strong>An automated Python tool to extract invoice numbers and recipient names from Brazilian Electronic Invoice (NF-e / DANFE) PDF files and rename them following a standardized naming convention.</strong>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.12.4-fbb22b?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/pypdf-6.18.1-c50505?style=for-the-badge&logo=pypdf&logoColor=white" alt="pypdf" />
    <img src="https://img.shields.io/badge/pytest-9.1.1-066c01?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest" />
</p>

---

## Features

- **Automated Text Extraction:** Uses `pypdf` to read PDF pages and extract invoice details.
- **Regex Pattern Matching:** Parses the invoice number (`Nº`) and recipient name (`Nome / Razão Social`).
- **Standardized Renaming:** Renames files to the format `NF-e {invoice_number} {recipient_name}.pdf`.
- **Unit Tested:** Includes a test suite using `pytest` to ensure accurate regex extraction.

---

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`:
  - `pypdf==6.18.1`
  - `pytest==9.1.1`

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/schulzdimitri/patternname.git
   cd patternname
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Open `main.py` and configure your target folder containing the NF-e PDF files:
   ```python
   PDF_FOLDER = "/path/to/your/nfe/folder"
   ```

2. Execute the script:
   ```bash
   python main.py
   ```

### Output Naming Convention

Original files in the directory matching `*.pdf` will be renamed:
```text
input_file.pdf -> NF-e 000580 Joao Eduardo Mariano de Souza.pdf
```

---

## Running Tests

Execute the unit tests using `pytest`:

```bash
python -m pytest
```

---

## Project Structure

```text
patternname/
├── main.py                     # Extraction logic and file renaming script
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── tests/
    └── test_pdf_extraction.py  # Unit tests for invoice data extraction
```
