<h1 align="center">🔥 PatternName - An Automated NF-e PDF Renamer</h1>

<p align="center">
  <strong>An automated Python tool to extract invoice numbers and recipient names from Brazilian Electronic Invoice (NF-e / DANFE) PDF files and rename them following a standardized naming convention.</strong>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.13-fbb22b?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/pypdf-6.18.1-c50505?style=for-the-badge&logo=pypdf&logoColor=white" alt="pypdf" />
    <img src="https://img.shields.io/badge/pytest-9.1.1-066c01?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest" />
    <img src="https://img.shields.io/badge/PyInstaller-6.22.3-2d7dd2?style=for-the-badge&logo=python&logoColor=white" alt="PyInstaller" />
</p>

---

## Features

- **Automated Text Extraction:** Uses `pypdf` to read PDF pages and extract invoice details.
- **Regex Pattern Matching:** Parses the invoice number (`Nº`) and recipient name (`Nome / Razão Social`).
- **Standardized Renaming:** Renames files to `NF-e {invoice_number} {recipient_name}.pdf`.
- **Robust Error Handling & Validation:**
  - Cleans input paths (trims whitespace and surrounding quotes).
  - Sanitizes invalid filesystem characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) from recipient names.
  - Skips corrupted or unreadable PDFs without breaking the execution loop.
  - Prevents accidental overwrites by checking for existing target files.
  - Prevents duplicate renaming on multi-page invoices.
- **Standalone Executable:** Build a self-contained binary using PyInstaller.
- **Unit Tested:** Comprehensive test suite with `pytest`.

---

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`:
  - `pypdf==6.18.1`
  - `pytest==9.1.1`
  - `pyinstaller==6.22.3`

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

1. Run the script:
   ```bash
   python main.py
   ```

2. Enter the folder path containing your NF-e PDF files when prompted (supports quoted paths):
   ```text
   Enter the path to the folder containing PDFs: /path/to/your/nfe/folder
   ```

### Output Naming Convention

Original files in the directory matching `*.pdf` will be renamed:
```text
input_file.pdf -> NF-e 000580 Joao Eduardo Mariano de Souza.pdf
```

---

## Building the Standalone Executable

To bundle the application into a single executable binary that can run without installing Python:

```bash
pyinstaller --onefile --name patternname main.py
```

The resulting binary will be created in the `dist/` folder:

- **macOS / Linux:**
  ```bash
  ./dist/patternname
  ```
- **Windows:**
  ```cmd
  dist\patternname.exe
  ```

---

## Running Tests

Execute the unit tests using `pytest`:

```bash
pytest -v -s
```