import unittest
from pathlib import Path
import tempfile
from main import (
    extract_invoice_data,
    sanitize_filename,
    clean_folder_path,
    rename_pdf,
)


class TestInvoiceExtraction(unittest.TestCase):
    def test_extract_invoice_data_success(self):
        sample_text = """
        DANFE
        NF-e
        Nº 000580
        Série 1
        Destinatário/Remetente
        Nome / Razão Social
        Joao Eduardo Mariano de Souza
        CNPJ/CPF
        390.060.638-27
        """
        result = extract_invoice_data(sample_text)
        self.assertEqual(result["invoice_number"], "000580")
        self.assertEqual(result["recipient_name"], "Joao Eduardo Mariano de Souza")

    def test_extract_invoice_data_missing(self):
        sample_text = "Some random text without matching patterns."
        result = extract_invoice_data(sample_text)
        self.assertIsNone(result["invoice_number"])
        self.assertIsNone(result["recipient_name"])

    def test_sanitize_filename(self):
        raw_name = 'Empresa/Ltda: Teste * "XPTO" <123> | 456? \\ end'
        sanitized = sanitize_filename(raw_name)
        self.assertEqual(sanitized, "EmpresaLtda Teste  XPTO 123  456  end")

    def test_clean_folder_path_success(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            quoted_path = f"  '{temp_dir}'  "
            result = clean_folder_path(quoted_path)
            self.assertEqual(result, Path(temp_dir))

    def test_clean_folder_path_invalid(self):
        with self.assertRaises(FileNotFoundError):
            clean_folder_path("/invalid/path/that/does/not/exist")

    def test_rename_pdf_skips_missing_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            records = [{"file_name": "test.pdf", "invoice_number": None, "recipient_name": "Acme"}]
            renamed = rename_pdf(folder, records)
            self.assertEqual(len(renamed), 0)

    def test_rename_pdf_skips_existing_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            source_file = folder / "invoice.pdf"
            source_file.write_text("dummy")

            existing_target = folder / "NF-e 100 Acme.pdf"
            existing_target.write_text("existing")

            records = [{"file_name": "invoice.pdf", "invoice_number": "100", "recipient_name": "Acme"}]
            renamed = rename_pdf(folder, records)
            self.assertEqual(len(renamed), 0)
            self.assertTrue(source_file.exists())


if __name__ == "__main__":
    unittest.main()
